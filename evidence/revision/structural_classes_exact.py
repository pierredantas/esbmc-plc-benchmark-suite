"""Structural classes of the 117 core benchmarks, ignoring identifier names (R2.4).

Ladder programs: each rung is a tree of series (AND) and parallel (OR) contacts and function blocks; trees are
flattened and sorted, and variable names are replaced by a colour from iterated refinement (WL), so renaming
variables or reordering branches does not change the signature. Other languages: a token or element signature
without identifiers. Variants: the first variant of each benchmark.

    structural_classes_exact.py SUITE
"""
import collections, csv, glob, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a1_converter_check import parse_dsl  # noqa: E402

SUITE = sys.argv[1]
core = {}
for v in csv.DictReader(open(os.path.join(HERE, "variants_302.csv"))):
    if v["core_suite"] == "yes":
        core.setdefault(v["id"], v)
St = {r["id"]: r for r in json.load(open(os.path.join(HERE, "structural.json")))}
St["g_ppu_evolution_1"]["cls"] = "authored domain"


def flat(e):
    if e[0] in ("var", "lit", "blk"):
        if e[0] == "blk":
            return ("blk", e[1], e[2], tuple((p, flat(t)) for p, t in e[3]))
        return e
    kids = []
    for x in map(flat, e[1]):
        if x == ("lit", True) and e[0] == "and":
            continue
        kids += list(x[1]) if x[0] == e[0] else [x]
    return kids[0] if len(kids) == 1 else (e[0], tuple(kids))


def shape(e, col):
    k = e[0]
    if k == "var":
        return "~" + col.get(e[1], "?") if e[2] else col.get(e[1], "?")
    if k == "lit":
        return "T" if e[1] else "F"
    if k == "blk":
        return f"{e[1]}[{e[2]}]({','.join(p + ':' + shape(t, col) for p, t in e[3])})"
    return k + "(" + ",".join(sorted(shape(x, col) for x in e[1])) + ")"


def variables(e):
    if e[0] == "var":
        return {e[1]}
    if e[0] == "lit":
        return set()
    if e[0] == "blk":
        return set().union(*[variables(t) for _, t in e[3]]) if e[3] else set()
    return set().union(*[variables(x) for x in e[1]])


def dsl_rungs(path):
    out = []
    def conv(e):
        if e[0] == "var": return ("var", e[1], bool(e[2]))
        if e[0] == "lit": return e
        return (e[0], [conv(x) for x in e[1]])
    for r in parse_dsl(open(path).read()):
        if r[0] in ("OTE", "OTL", "OTU"):
            out.append((r[1], r[0], flat(conv(r[2]))))
        else:
            pins = [("IN", conv(r[3]))] + ([("R", conv(r[4]))] if r[4] is not None else [])
            out.append((r[1], r[0], ("blk", r[0], r[2], tuple((p, flat(t)) for p, t in pins))))
    return out


def xml_rungs(path):
    ld = ET.parse(path).getroot().find(".//{*}body/{*}LD")
    nodes = {int(e.get("localId")): e for e in ld.iter() if e.get("localId")}
    nm = lambda e: e.tag.split("}")[-1]
    def srcs(e): return [(int(c.get("refLocalId")), c.get("formalParameter")) for c in e.iter() if nm(c) == "connection"]
    def tree(i, pin=None, seen=()):
        if i not in nodes:
            return ("lit", "missing")
        e = nodes[i]; t = nm(e)
        if t == "leftPowerRail" or i in seen: return ("lit", True)
        if t == "inVariable": return ("lit", e.findtext("{*}expression"))
        if t == "block":
            ins = []
            for v in e.find("{*}inputVariables"):
                ins.append((v.get("formalParameter"), flat(("or", [tree(s, p, seen + (i,)) for s, p in srcs(v)]) if srcs(v) else ("lit", False))))
            pt = next((str(x[1][1]) for x in ins if x[0] in ("PT", "PV") and x[1][0] == "lit"), "")
            return ("blk", e.get("typeName"), pt, tuple(sorted(x for x in ins if x[0] not in ("PT", "PV"))))
        inc = ("or", [tree(s, p, seen + (i,)) for s, p in srcs(e)]) if srcs(e) else ("lit", False)
        if t == "contact":
            return ("and", [inc, ("var", e.findtext("{*}variable"), e.get("negated") == "true")])
        return inc
    rungs = [(c.findtext("{*}variable"), c.get("storage", "none"), flat(tree(int(c.get("localId")))))
             for c in ld.iter() if nm(c) == "coil" and c.get("localId")]
    for o in ld.iter():
        if nm(o) == "outVariable":
            rungs.append((o.findtext("{*}expression"), "assign", flat(("or", [tree(s, p) for s, p in srcs(o)]) if srcs(o) else ("lit", False))))
    return rungs


def ladder_signature(rungs):
    coils = {c for c, _, _ in rungs}
    allv = set().union(*[variables(t) | {c} for c, _, t in rungs]) if rungs else set()
    col = {v: ("o" if v in coils else "i") for v in allv}
    for _ in range(4):
        new = {}
        for v in allv:
            ctx = sorted(f"{int(c == v)}{s}:{shape(t, {**col, v: '@'})}" for c, s, t in rungs if v == c or v in variables(t))
            new[v] = hashlib.md5((col[v] + "|".join(ctx)).encode()).hexdigest()[:6]
        col = new
    return hashlib.md5("|".join(sorted(f"{s}:{int(c in coils)}:{shape(t, col)}" for c, s, t in rungs)).encode()).hexdigest()


KW = set("PROGRAM END_PROGRAM VAR VAR_INPUT VAR_OUTPUT END_VAR IF THEN ELSE ELSIF END_IF AND OR NOT XOR BOOL INT DINT REAL TIME TON TOF TP CTU CTD LD ST AND OR S R CASE OF END_CASE FOR TO DO END_FOR WHILE END_WHILE FUNCTION_BLOCK END_FUNCTION_BLOCK CONFIGURATION RESOURCE TASK".split())


def token_signature(path):
    t = open(path, errors="replace").read()
    if path.endswith(".xml"):
        r = ET.fromstring(t.replace("tc6_0200", "tc6_0201").encode())
        tags = collections.Counter(e.tag.split("}")[-1] + ":" + e.get("typeName", "") for e in r.iter()
                                   if e.tag.split("}")[-1] not in ("position", "relPosition", "connection", "connectionPointIn", "connectionPointOut"))
        return hashlib.md5(repr(sorted(tags.items())).encode()).hexdigest()
    t = re.sub(r"\(\*.*?\*\)", "", t, flags=re.S)
    toks = re.findall(r"[A-Za-z_]\w*|\d+|:=|<>|<=|>=|[^\s\w]", t)
    toks = [x if x.upper() in KW else ("N" if x.isdigit() else "ID" if re.match(r"[A-Za-z_]", x) else x) for x in toks]
    return hashlib.md5(" ".join(toks).encode()).hexdigest()


sig, kind = {}, {}
for bid, v in sorted(core.items()):
    g = glob.glob(f"{SUITE}/benchmarks/*/{bid}/{v['file']}")[0]
    if v["lang"] == "LD-textual":
        sig[bid] = ladder_signature(dsl_rungs(g)); kind[bid] = "ladder"
    elif v["lang"] == "LD-graphical":
        sig[bid] = ladder_signature(xml_rungs(g)); kind[bid] = "ladder"
    else:
        sig[bid] = token_signature(g); kind[bid] = "other"
classes = collections.defaultdict(list)
for b, s in sig.items():
    classes[(kind[b], s)].append(b)
sizes = sorted((len(v) for v in classes.values()), reverse=True)
multi = [v for v in classes.values() if len(v) > 1]
dom = {b: json.load(open(os.path.join(HERE, "structural.json"))) and None for b in []}
domain = {r["id"]: r["dom"] for r in json.load(open(os.path.join(HERE, "structural.json")))}
cross = [v for v in multi if len({domain[b] for b in v}) > 1]
res = dict(benchmarks=len(sig), classes=len(classes), singleton=sum(1 for s in sizes if s == 1), largest=sizes[0],
           multi=len(multi), multi_members=sum(len(v) for v in multi), cross_classes=len(cross),
           cross_members=sum(len(v) for v in cross), cross_benchmarks_any=sum(len(v) for v in cross))
print(res)
json.dump(dict(summary=res, classes=[sorted(v) for v in classes.values() if len(v) > 1]), open(os.path.join(HERE, "structural_classes_exact.json"), "w"), indent=1)
