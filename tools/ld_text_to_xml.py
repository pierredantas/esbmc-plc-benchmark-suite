#!/usr/bin/env python3
"""Convert the suite's plain-text LD DSL (OTE/XIC/XIO rungs) to PLCopen XML.

The DSL used by benchmarks/**/*.ld is a small grammar:

    OTE|OTL|OTU(coil) := <expr> ;
    TON|TOF|TP(Q, PT, <expr IN>) ;
    CTU(Q, PV, <expr CU>, <expr R>) ;   CTD(Q, PV, <expr CD>, <expr LD>) ;
    <expr>    := <term> ('+' <term>)*
    <term>    := <factor> ('*' <factor>)*
    <factor>  := 'XIC' '(' IDENT ')' | 'XIO' '(' IDENT ')'
               | 'TRUE' | 'FALSE' | '(' <expr> ')'

XIC is a normally-open contact (var), XIO a normally-closed one (NOT var), '*' is
AND (series), '+' is OR (parallel branches). OTL/OTU are set/reset coils. A block's
Q drives a coil on the variable its first argument names; PT counts scans of the
10 ms task. Anything else (CTUD, SET, RST, R_TRIG, F_TRIG) raises rather than
silently mis-converting.

The expression is expanded into a flat sum of AND-terms (distributing '*' over
'+'), which is exactly the {coil, branches} shape tools/ld_from_rungs.py already
knows how to lay out as contacts and coils, plus a literal `TRUE`/`FALSE` term
rendered as an <inVariable> instead of a contact chain (ld_to_st.py already reads
<inVariable><expression> as a literal source, so this is not a new element type
for the suite's own XML consumer).

    python3 -m tools.ld_text_to_xml benchmarks/traffic/all_red_clearance_ds/clean.ld
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ld_from_rungs import build as build_xml

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
TOKEN_RE = re.compile(rf"""
    (?P<XIC>XIC)
  | (?P<XIO>XIO)
  | (?P<TRUE>TRUE\b)
  | (?P<FALSE>FALSE\b)
  | (?P<IDENT>{IDENT})
  | (?P<LPAREN>\()
  | (?P<RPAREN>\))
  | (?P<AND>\*)
  | (?P<OR>\+)
  | (?P<WS>\s+)
""", re.VERBOSE)

UNSUPPORTED = re.compile(r"\b(CTUD|SET|RST|R_TRIG|F_TRIG)\b")


class ParseError(ValueError):
    pass


def tokenize(text):
    pos, out = 0, []
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise ParseError(f"unexpected character {text[pos]!r} at {pos}")
        kind = m.lastgroup
        if kind != "WS":
            out.append((kind, m.group()))
        pos = m.end()
    return out


class Parser:
    """Recursive-descent parser producing a sum-of-products: list[list[(var, negated)]].

    A `TRUE`/`FALSE` literal term is represented as a one-element AND-term
    `[(None, negated)]`, `var=None` marking it as a literal rather than a contact;
    `negated=False` means TRUE, `negated=True` means FALSE (`NOT TRUE` reads the
    same as bare FALSE, and the emitter only ever asks "is this term the constant
    true/false", not "was it spelled with a NOT").
    """

    def __init__(self, tokens, source):
        self.tokens = tokens
        self.i = 0
        self.source = source

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else (None, None)

    def expect(self, kind):
        k, v = self.peek()
        if k != kind:
            raise ParseError(f"expected {kind}, got {k or 'EOF'} ({v!r}) in {self.source!r}")
        self.i += 1
        return v

    def parse_expr(self):
        """<expr> := <term> ('+' <term>)*  ->  list of AND-terms (OR'd)."""
        terms = self.parse_term()
        while self.peek()[0] == "OR":
            self.i += 1
            terms = terms + self.parse_term()
        return terms

    def parse_term(self):
        """<term> := <factor> ('*' <factor>)*  ->  a single sum-of-products list.

        Each side of '*' is itself a sum-of-products (a factor can be a
        parenthesised <expr>), so multiplying them distributes: every AND-term on
        the left is combined with every AND-term on the right.
        """
        left = self.parse_factor()
        while self.peek()[0] == "AND":
            self.i += 1
            right = self.parse_factor()
            left = [l + r for l in left for r in right]
        return left

    def parse_factor(self):
        """<factor> := XIC(id) | XIO(id) | TRUE | FALSE | '(' <expr> ')'  ->  sum-of-products."""
        kind, _ = self.peek()
        if kind in ("XIC", "XIO"):
            self.i += 1
            self.expect("LPAREN")
            var = self.expect("IDENT")
            self.expect("RPAREN")
            return [[(var, kind == "XIO")]]
        if kind == "TRUE":
            self.i += 1
            return [[(None, False)]]
        if kind == "FALSE":
            self.i += 1
            return [[(None, True)]]
        if kind == "LPAREN":
            self.i += 1
            inner = self.parse_expr()
            self.expect("RPAREN")
            return inner
        raise ParseError(f"expected a factor, got {kind or 'EOF'} in {self.source!r}")

    def parse(self):
        terms = self.parse_expr()
        if self.i != len(self.tokens):
            raise ParseError(f"trailing tokens after expression in {self.source!r}")
        return terms


RUNG_RE = re.compile(rf"(?P<op>OTE|OTL|OTU)\((?P<coil>{IDENT})\)\s*:=\s*(?P<rhs>.+?)\s*;\s*$")
# TON|TOF|TP(Q, PT, IN) and CTU(Q, PV, CU, R) / CTD(Q, PV, CD, LD); presets count
# scans, as the LD front end reads a plain integer preset.
BLOCK_RE = re.compile(rf"(?P<fb>TON|TOF|TP|CTU|CTD)\((?P<args>.*)\)\s*;\s*$")
PINS = {"TON": ["IN"], "TOF": ["IN"], "TP": ["IN"], "CTU": ["CU", "R"], "CTD": ["CD", "LD"]}


def split_args(text):
    """Top-level comma-separated arguments; commas inside parentheses stay put."""
    out, depth, cur = [], 0, ""
    for ch in text:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return out + [cur.strip()]


def parse_line(line):
    """One rung: {coil, op, terms} or {block, q, preset, pins}."""
    m = RUNG_RE.match(line)
    if m:
        return dict(op=m.group("op"), coil=m.group("coil"),
                    terms=Parser(tokenize(m.group("rhs")), line).parse())
    m = BLOCK_RE.match(line)
    if not m:
        raise ParseError(f"line is neither 'OTE|OTL|OTU(coil) := <expr> ;' nor a "
                          f"TON/TOF/TP/CTU/CTD block: {line!r}")
    fb, args = m.group("fb"), split_args(m.group("args"))
    if len(args) != 2 + len(PINS[fb]) or not re.fullmatch(IDENT, args[0]) \
            or not args[1].isdigit():
        raise ParseError(f"{fb} takes (Q, preset, {', '.join(PINS[fb])}): {line!r}")
    return dict(block=fb, q=args[0], preset=int(args[1]),
                pins=[(pin, Parser(tokenize(a), line).parse())
                      for pin, a in zip(PINS[fb], args[2:])])


def parse_program(text):
    """Every rung in a .ld source, in file order."""
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("//") and not ln.startswith("(*")]
    unsupported = UNSUPPORTED.search("\n".join(lines))
    if unsupported:
        raise ParseError(f"unsupported block {unsupported.group(0)!r}: this converter "
                          "handles OTE/OTL/OTU rungs and TON/TOF/TP/CTU/CTD blocks; "
                          "anything else needs a hand-written PLCopen XML body")
    return [parse_line(ln) for ln in lines]


def targets(rung):
    return rung["q"] if "block" in rung else rung["coil"]


def reads(rung):
    groups = [t for _, t in rung["pins"]] if "block" in rung else [rung["terms"]]
    return [var for terms in groups for term in terms for var, _ in term if var]


def variables(rungs):
    """(inputs, outputs) as they first appear: outputs are every coil target and
    block output, inputs everything else a rung reads. A variable can be both (a
    latch coil fed back into its own rung); it counts as an output only."""
    outs = list(dict.fromkeys(targets(r) for r in rungs))
    ins = list(dict.fromkeys(v for r in rungs for v in reads(r) if v not in outs))
    return ins, outs


STORAGE = {"OTE": "none", "OTL": "set", "OTU": "reset"}
TICK_MS = 10  # the task interval tools/ld_from_rungs.py writes


def to_xml_rungs(rungs):
    """Parsed rungs -> tools.ld_from_rungs' rung dicts."""
    out = []
    for rung in rungs:
        if "block" in rung:
            groups = [t for _, t in rung["pins"]]
            if any(var is None for terms in groups for term in terms for var, _ in term):
                raise ParseError(f"{rung['block']} {rung['q']!r}: a TRUE/FALSE literal on "
                                  "a block pin is not representable")
            q = rung["q"]
            timer = rung["block"] in ("TON", "TOF", "TP")
            out.append(dict(block=rung["block"], q=q,
                            inst=q[:-2] if q.endswith("_Q") else q + "_FB",
                            preset=f"T#{rung['preset'] * TICK_MS}ms" if timer
                            else str(rung["preset"]),
                            pins=[(pin, [list(term) for term in terms])
                                  for pin, terms in rung["pins"]]))
            continue
        coil, terms = rung["coil"], rung["terms"]
        if terms in ([[(None, False)]], [[(None, True)]]):
            if rung["op"] != "OTE":
                raise ParseError(f"{rung['op']}({coil}) driven by a literal")
            out.append(dict(coil=coil, literal=terms == [[(None, False)]]))
        elif any(var is None for term in terms for var, _ in term):
            raise ParseError(f"coil {coil!r} mixes a TRUE/FALSE literal with contacts; "
                              "not representable as a single rung")
        else:
            out.append(dict(coil=coil, storage=STORAGE[rung["op"]],
                            branches=[list(term) for term in terms]))
    return out


def translate(name, text, inputs=()):
    """The PLCopen XML rendering of one .ld source's full program.

    The DSL declares nothing, so a variable named in `inputs` but not in any rung
    (a sensor a bomb variant stopped reading) is declared as an input here.
    """
    rungs = parse_program(text)
    ins, outs = variables(rungs)
    ins += [v for v in inputs if v not in ins and v not in outs]
    return build_xml(name, ins, outs, to_xml_rungs(rungs))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)
    path = sys.argv[1]
    name = os.path.splitext(os.path.basename(path))[0]
    print(translate(name, open(path, encoding="utf-8").read()))


if __name__ == "__main__":
    main()
