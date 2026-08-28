"""Emit a PLCopen XML ladder program from a rung description.

Hand-writing PLCopen XML is where authoring errors hide: a mistyped refLocalId
produces a well-formed file that draws a different rung than you meant, and the
schema will not catch it. This builds the XML from the rung structure instead.

A rung is {coil, branches, tail}: the coil is driven by the OR of the branches,
each branch a series of contacts, with an optional common series tail after the
junction. That covers every contact-and-coil program in this suite, latches
included. Blocks (TON, counters, user-defined function blocks) are not emitted;
those files are still written by hand.

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
    <interface><inputVars>{ins}</inputVars><outputVars>{outs}</outputVars></interface>
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

    for rung in rungs:
        ends, top = [], y
        for branch in rung["branches"]:
            src, x = [0], 20
            for var, neg in branch:
                src, x = [contact(var, neg, x, y, src)], x + 20
            ends += src
            y += 10
        x = 20 + 20 * max(len(b) for b in rung["branches"])
        for var, neg in rung.get("tail", []):
            ends, x = [contact(var, neg, x, top, ends)], x + 20
        conns = "".join(f'<connection refLocalId="{e}" />' for e in ends)
        elems.append(f'<coil localId="{nid}" negated="false" storage="none">'
                     f'<position x="{x}" y="{top}" /><connectionPointIn>{conns}'
                     f'</connectionPointIn><connectionPointOut /><variable>{rung["coil"]}</variable></coil>')
        nid += 1
        y += 20
    return HEAD.format(name=name, body="".join(elems),
                       ins="".join(VAR.format(v) for v in ins),
                       outs="".join(VAR.format(v) for v in outs))
