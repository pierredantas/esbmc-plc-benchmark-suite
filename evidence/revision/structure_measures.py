"""Nesting depth and coupling of the 73 ladder benchmarks of the core suite (R2.4).

Per benchmark, on its first variant: the rung expressions are trees of AND (series) and OR (parallel branches).
Nesting is the depth of the flattened AND/OR tree (a plain series of contacts has depth 1, one parallel branch inside it depth 2); coupling is the number of rungs that read a
coil written by another rung, as a count of such rung pairs. Graphical programs are read from the PLCopen XML.
"""
import csv, glob, json, os, re, statistics as st, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a1_converter_check import parse_dsl  # noqa: E402  (module guards main() below)

S = sys.argv[1]
Q = lambda t: "{*}" + t
core = {}
for v in csv.DictReader(open(os.path.join(os.path.dirname(__file__), "variants_302.csv"))):
    if v["core_suite"] == "yes" and v["lang"].startswith("LD"):
        core.setdefault(v["id"], v)


def flat(e):
    """Drop literal TRUE inputs and single-child nodes, and merge nested nodes of the same operator."""
    if e[0] in ("var", "lit"):
        return e
    kids = []
    for x in map(flat, e[1]):
        if x == ("lit", True) and e[0] == "and":
            continue
        kids += x[1] if x[0] == e[0] else [x]
    return kids[0] if len(kids) == 1 else (e[0], kids)


def depth(e):
    e = flat(e)
    return 0 if e[0] in ("var", "lit") else 1 + max(depth(x) for x in e[1])


def reads(e):
    if e[0] == "var":
        return {e[1]}
    return set() if e[0] == "lit" else set().union(*[reads(x) for x in e[1]]) if e[1] else set()


def textual(path):
    rungs = parse_dsl(open(path).read())
    exprs = [(r[1], r[2] if r[0] in ("OTE", "OTL", "OTU") else r[3]) for r in rungs]
    return exprs


def graphical(path):
    ld = ET.parse(path).getroot().find(".//" + Q("body") + "/" + Q("LD"))
    nodes = {int(e.get("localId")): e for e in ld}
    def tree(i, seen=()):
        e = nodes[i]; tag = e.tag.split("}")[1]
        if tag == "leftPowerRail" or i in seen:
            return ("lit", True)
        srcs = [int(c.get("refLocalId")) for c in e.iter() if c.tag.split("}")[-1] == "connection"]
        inc = ("or", [tree(s, seen + (i,)) for s in srcs]) if srcs else ("lit", False)
        if tag == "contact":
            return ("and", [inc, ("var", e.findtext(Q("variable")))])
        return inc
    return [(e.findtext(Q("variable")), tree(int(e.get("localId")))) for e in ld if e.tag.split("}")[1] == "coil"]


rows = []
for bid, v in sorted(core.items()):
    g = glob.glob(f"{S}/benchmarks/*/{bid}/{v['file']}")
    if not g:
        print("missing file", bid, v["file"]); continue
    f = g[0]
    try:
        exprs = textual(f) if v["lang"] == "LD-textual" else graphical(f)
    except Exception as ex:
        print("skip", bid, ex); continue
    coils = {c for c, _ in exprs}
    nest = max((depth(e) for _, e in exprs), default=0)
    coupling = sum(1 for c, e in exprs if (reads(e) & coils) - {c})
    rows.append(dict(id=bid, lang=v["lang"], rungs=len(exprs), nesting=nest, coupling=coupling))
json.dump(rows, open(os.path.join(os.path.dirname(__file__), "structure_measures.json"), "w"), indent=1)
n = [r["nesting"] for r in rows]; c = [r["coupling"] for r in rows]
print(len(rows), "benchmarks; nesting median", st.median(n), "max", max(n), "| coupling median", st.median(c), "max", max(c))
print("coupling 0 in", sum(1 for x in c if x == 0), "; nesting <=1 in", sum(1 for x in n if x <= 1))
