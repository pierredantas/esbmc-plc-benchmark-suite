"""Emit a PLCopen XML ladder program from a rung description.

Hand-writing PLCopen XML is where authoring errors hide: a mistyped refLocalId
produces a well-formed file that draws a different rung than you meant, and the
schema will not catch it. This builds the XML from the rung structure instead.

A rung is {coil, branches, tail}: the coil is driven by the OR of the branches,
each branch a series of contacts, with an optional common series tail after the
junction. That covers every contact-and-coil program in this suite, latches
included. Blocks (TON, counters, user-defined function blocks) are not emitted;
those files are still written by hand.

A rung can instead be {coil, literal}: the coil is driven directly by the
constant TRUE/FALSE (a bare `OTE(x) := TRUE ;`/`FALSE ;` rung has no contact to
draw). The left rail powers the coil every scan: a plain coil for TRUE, a reset
coil for FALSE, which is `x := FALSE` each scan. An <inVariable> literal would
carry no power flow, and ESBMC refuses a coil it cannot drive. Mixing `literal`
with `branches`/`tail` on the same rung is not meaningful and is rejected.

    from ld_from_rungs import build
    T, F = True, False
    xml = build("g_seal_in", ["Start", "Stop"], ["Run"], [
        dict(coil="Run",
             branches=[[("Run", F)], [("Start", F)]],
             tail=[("Stop", T)]),
    ])

Emitted files must still pass runner/validate.py and runner/schema_check.py,
and the rung order in the file is not the order ESBMC executes them (see
lesson 1.5).
"""
import sys

HEAD = '''<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="{name}"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="{name}" pouType="program">
    <interface><inputVars>{ins}</inputVars><outputVars>{outs}</outputVars>{locals}</interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      {body}
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="{name}" /></task></resource></configuration></configurations></instances>
</project>
'''
VAR = '<variable name="{0}"><type><BOOL /></type></variable>'


def build(name, ins, outs, rungs):
    nid, elems, y = 3, [], 10

    def contact(var, neg, x, y, srcs):
        nonlocal nid
        conns = "".join(f'<connection refLocalId="{s}" />' for s in srcs)
        elems.append(f'<contact localId="{nid}" negated="{str(neg).lower()}" storage="none" '
                     f'edge="none"><position x="{x}" y="{y}" /><connectionPointIn>{conns}'
                     f'</connectionPointIn><connectionPointOut /><variable>{var}</variable></contact>')
        nid += 1
        return nid - 1

    def network(branches, tail=()):
        """Contact chains from the rail, OR'd; the ends that carry their power."""
        nonlocal y
        ends, top = [], y
        for branch in branches:
            src, x = [0], 20
            for var, neg in branch:
                src, x = [contact(var, neg, x, y, src)], x + 20
            ends += src
            y += 10
        x = 20 + 20 * max((len(b) for b in branches), default=0)
        for var, neg in tail:
            ends, x = [contact(var, neg, x, top, ends)], x + 20
        return ends, x

    def coil(var, storage, x, top, conns):
        nonlocal nid
        elems.append(f'<coil localId="{nid}" negated="false" storage="{storage}">'
                     f'<position x="{x}" y="{top}" /><connectionPointIn>{conns}'
                     f'</connectionPointIn><connectionPointOut /><variable>{var}</variable></coil>')
        nid += 1

    def literal(text, x, top):
        nonlocal nid
        elems.append(f'<inVariable localId="{nid}" height="20" width="40"><position x="{x}" '
                     f'y="{top}" /><connectionPointOut><relPosition x="40" y="10" />'
                     f'</connectionPointOut><expression>{text}</expression></inVariable>')
        nid += 1
        return nid - 1

    def block(rung):
        """A timer or counter: its power pins fed by contact networks, its preset
        by a literal, and Q driving a coil on `q`. The wire from Q names the pin
        and carries its starting point, which Beremiz needs to resolve it."""
        nonlocal nid, y
        top, pins = y, []
        for pin, branches in rung["pins"]:
            ends, _ = network(branches)
            pins.append((pin, ends))
        preset = literal(rung["preset"], 20, y)
        y += 20
        bx, bid = 20 + 20 * max(max((len(b) for b in br), default=0) for _, br in rung["pins"]), nid
        rows = [(pin, "".join(f'<connection refLocalId="{e}" />' for e in ends))
                for pin, ends in pins]
        rows.append(("PT" if rung["block"] in ("TON", "TOF", "TP") else "PV",
                     f'<connection refLocalId="{preset}" />'))
        ins_xml = "".join(f'<variable formalParameter="{pin}"><connectionPointIn><relPosition '
                          f'x="0" y="{20 * (i + 1)}" />{c}</connectionPointIn></variable>'
                          for i, (pin, c) in enumerate(rows))
        outs = ["Q", "ET"] if rung["block"] in ("TON", "TOF", "TP") else ["Q", "CV"]
        outs_xml = "".join(f'<variable formalParameter="{o}"><connectionPointOut><relPosition '
                           f'x="80" y="{20 * (i + 1)}" /></connectionPointOut></variable>'
                           for i, o in enumerate(outs))
        elems.append(f'<block localId="{bid}" width="80" height="{20 * (len(rows) + 1)}" '
                      f'typeName="{rung["block"]}" instanceName="{rung["inst"]}"><position '
                      f'x="{bx}" y="{top}" /><inputVariables>{ins_xml}</inputVariables>'
                      f'<inOutVariables /><outputVariables>{outs_xml}</outputVariables></block>')
        nid += 1
        coil(rung["q"], "none", bx + 120, top,
             f'<connection refLocalId="{bid}" formalParameter="Q"><position x="{bx + 80}" '
             f'y="{top + 20}" /></connection>')

    locals_ = []
    for rung in rungs:
        top = y
        if "block" in rung:
            block(rung)
            locals_.append((rung["inst"], rung["block"]))
        elif "literal" in rung:
            if rung.get("branches") or rung.get("tail"):
                raise ValueError(f"rung {rung['coil']!r}: literal cannot be combined "
                                  "with branches/tail")
            coil(rung["coil"], "reset" if rung["literal"] is False else "none", 20, top,
                 '<connection refLocalId="0" />')
        else:
            ends, x = network(rung["branches"], rung.get("tail", []))
            coil(rung["coil"], rung.get("storage", "none"), x, top,
                 "".join(f'<connection refLocalId="{e}" />' for e in ends))
        y += 20
    return HEAD.format(name=name, body="".join(elems),
                       locals=("<localVars>" + "".join(
                           f'<variable name="{n}"><type><derived name="{t}" /></type></variable>'
                           for n, t in locals_) + "</localVars>") if locals_ else "",
                       ins="".join(VAR.format(v) for v in ins),
                       outs="".join(VAR.format(v) for v in outs))
