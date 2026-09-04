#!/usr/bin/env python3
"""Convert the suite's plain-text LD DSL (OTE/XIC/XIO rungs) to PLCopen XML.

The DSL used by benchmarks/**/{clean,bomb}.ld is a small combinational grammar:

    OTE(coil) := <expr> ;
    <expr>    := <term> ('+' <term>)*
    <term>    := <factor> ('*' <factor>)*
    <factor>  := 'XIC' '(' IDENT ')' | 'XIO' '(' IDENT ')'
               | 'TRUE' | 'FALSE' | '(' <expr> ')'

XIC is a normally-open contact (var), XIO a normally-closed one (NOT var), '*' is
AND (series), '+' is OR (parallel branches). This covers every rung actually
written in the corpus (confirmed by survey: no TON/TOF/TP/CTU/CTD/OTL/OTU/SET/RST
appear in any of the plain-text .ld files this module targets); a file that uses
one of those raises rather than silently mis-converting it.

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

UNSUPPORTED = re.compile(r"\b(TON|TOF|TP|CTU|CTD|CTUD|OTL|OTU|SET|RST|R_TRIG|F_TRIG)\b")


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


RUNG_RE = re.compile(rf"OTE\((?P<coil>{IDENT})\)\s*:=\s*(?P<rhs>.+?)\s*;\s*$")


def parse_program(text):
    """Every OTE rung in a .ld source, as (coil, sum_of_products) pairs, in file order."""
    unsupported = UNSUPPORTED.search(text)
    if unsupported:
        raise ParseError(f"unsupported block {unsupported.group(0)!r}: this converter "
                          "only handles combinational OTE/XIC/XIO rungs; stateful "
                          "function blocks need a hand-written PLCopen XML body")
    rungs = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("(*"):
            continue
        m = RUNG_RE.match(line)
        if not m:
            raise ParseError(f"line does not match 'OTE(coil) := <expr> ;': {line!r}")
        terms = Parser(tokenize(m.group("rhs")), line).parse()
        rungs.append((m.group("coil"), terms))
    return rungs


def variables(rungs):
    """(inputs, outputs) as they first appear: outputs are every OTE target, inputs
    everything else read on a right-hand side. A variable can be both (a latch
    coil fed back into its own rung); it counts as an output only."""
    outs, ins = [], []
    seen_out, seen_in = set(), set()
    for coil, terms in rungs:
        if coil not in seen_out:
            seen_out.add(coil)
            outs.append(coil)
    for coil, terms in rungs:
        for term in terms:
            for var, _ in term:
                if var is None or var in seen_out or var in seen_in:
                    continue
                seen_in.add(var)
                ins.append(var)
    return ins, outs


def to_rung_dicts(rungs):
    """sum-of-products -> tools.ld_from_rungs' {coil, branches} shape.

    A literal term (var is None) has no contacts at all; ld_from_rungs.build()
    does not model that, so literal-only coils are reported separately by the
    caller instead of forcing an empty branch through the contact-chain builder.
    """
    out = []
    for coil, terms in rungs:
        if any(var is None for term in terms for var, _ in term):
            raise ParseError(f"coil {coil!r} is driven by a TRUE/FALSE literal; "
                              "emit it as a literal coil, not via to_rung_dicts")
        out.append(dict(coil=coil, branches=[list(term) for term in terms]))
    return out


def to_xml_rungs(rungs):
    """sum-of-products -> tools.ld_from_rungs' rung dicts, literal coils included."""
    out = []
    for coil, terms in rungs:
        if terms == [[(None, False)]]:
            out.append(dict(coil=coil, literal=True))
        elif terms == [[(None, True)]]:
            out.append(dict(coil=coil, literal=False))
        elif any(var is None for term in terms for var, _ in term):
            raise ParseError(f"coil {coil!r} mixes a TRUE/FALSE literal with contacts; "
                              "not representable as a single rung")
        else:
            out.append(dict(coil=coil, branches=[list(term) for term in terms]))
    return out


def translate(name, text):
    """The PLCopen XML rendering of one .ld source's full program."""
    rungs = parse_program(text)
    ins, outs = variables(rungs)
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
