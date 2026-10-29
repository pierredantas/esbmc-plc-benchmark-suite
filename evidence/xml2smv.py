#!/usr/bin/env python3
"""Independent PLCopen-XML (combinational LD) -> NuSMV translator and cross-check."""
import sys, re, glob, os, itertools, subprocess, xml.etree.ElementTree as ET, yaml
NS = {"p": "http://www.plcopen.org/xml/tc6_0200"}
q = lambda t: "{%s}%s" % (NS["p"], t)

def parse(path):
    ld = ET.parse(path).getroot().find(".//p:body/p:LD", NS)
    nodes = {}
    for e in ld:
        tag = e.tag.split("}")[1]
        if tag in ("leftPowerRail", "contact", "coil"):
            var = e.findtext(q("variable"))
            src = [int(c.get("refLocalId")) for c in e.iter(q("connection"))]
            nodes[int(e.get("localId"))] = dict(tag=tag, var=var, neg=e.get("negated") == "true",
                                                 store=e.get("storage", "none"), edge=e.get("edge", "none"), src=src)
        elif tag != "rightPowerRail":
            raise ValueError("unsupported element " + tag)
    return nodes

def expr(nodes, i, memo):
    if i in memo: return memo[i]
    n = nodes[i]
    if n["tag"] == "leftPowerRail": r = "TRUE"
    else:
        if n["store"] != "none" or n["edge"] != "none":
            raise ValueError("stateful element at %d" % i)
        inc = " | ".join("(%s)" % expr(nodes, s, memo) for s in n["src"]) or "FALSE"
        if n["tag"] == "contact":
            lit = ("!%s" % n["var"]) if n["neg"] else n["var"]
            r = "(%s) & %s" % (inc, lit)
        else: r = inc
    memo[i] = r; return r

def translate(path):
    """Sequential scan order = document order of coils: a contact reads the current-scan
    value of a coil whose rung precedes the reader's, else the previous-scan value."""
    nodes = parse(path)
    order = {}
    for i, n in nodes.items():
        if n["tag"] == "coil": order.setdefault(n["var"], len(order))
    prev = set()
    def expr2(i, owner):
        n = nodes[i]
        if n["tag"] == "leftPowerRail": return "TRUE"
        if n["store"] != "none" or n["edge"] != "none":
            raise ValueError("stateful element at %d" % i)
        inc = " | ".join("(%s)" % expr2(s_, owner) for s_ in n["src"]) or "FALSE"
        if n["tag"] == "contact":
            var = n["var"]
            if var in order and order[var] >= order[owner]:
                prev.add(var); var = var + "_prev"
            return "(%s) & %s" % (inc, ("!%s" % var) if n["neg"] else var)
        return inc
    coils = {}
    for i, n in nodes.items():
        if n["tag"] == "coil": coils.setdefault(n["var"], []).append("(%s)" % expr2(i, n["var"]))
    ins = []
    for n in nodes.values():
        if n["tag"] == "contact" and n["var"] not in order and n["var"] not in ins: ins.append(n["var"])
    return ins, {c: " | ".join(v) for c, v in coils.items()}, sorted(prev)


def prop_smv(props_yaml):
    out = []
    for p in yaml.safe_load(open(props_yaml))["properties"]:
        if p["kind"] == "invariant":
            e = re.sub(r"\bAND\b", "&", p["expression"]); e = re.sub(r"\bOR\b", "|", e)
            e = e.replace("&&", "&").replace("||", "|"); e = re.sub(r"\bNOT\s+", "!", e)
            e = re.sub(r"(\w+)\s*->\s*(\w+)", r"(\1 -> \2)", e) if "->" in e and "(" not in e else e
            out.append("INVARSPEC " + e + ";")
        elif p["kind"] == "reachable":
            e = p["expression"].replace("&&", "&").replace("||", "|")
            out.append("CTLSPEC EF (" + e + ");")
        elif p["kind"] == "reachability":
            e = re.sub(r"\bAND\b", "&", p["expression"]); e = e.replace("&&", "&").replace("||", "|")
            out.append("INVARSPEC !(" + e + ");")
        elif p["kind"] == "mutual_exclusion":
            vs = p["variables"]
            out.append("INVARSPEC !(" + " & ".join(vs) + ");" if len(vs) == 2 else "INVARSPEC " + " & ".join("TRUE" for _ in vs) + ";")
    return out

def mangle(text, names):
    for n in sorted(names, key=len, reverse=True):
        text = re.sub(r"\b%s\b" % re.escape(n), "v_" + n, text)
    return text

def smv_text(path, props):
    ins, defs, cyc = translate(path)
    for q_ in yaml.safe_load(open(props))["properties"]:
        text_ = q_.get("expression", "") + " " + " ".join(q_.get("variables", []))
        for v_ in re.findall(r"[A-Za-z_]\w*", text_):
            if v_ not in ("AND", "OR", "NOT", "true", "false", "TRUE", "FALSE") and v_ not in ins and v_ not in defs:
                ins.append(v_)
    names = set(ins) | set(defs) | {c + '_prev' for c in cyc}
    return mangle(smv_text_raw(ins, defs, props, cyc), names)

def smv_text_raw(ins, defs, props, cyc):
    nl = chr(10)
    var = "".join("  %s : boolean;" % v + nl for v in ins + [c + "_prev" for c in cyc])
    asg = ""
    if cyc:
        asg = "ASSIGN" + nl + "".join("  init(%s_prev) := FALSE;" % c + nl + "  next(%s_prev) := %s;" % (c, c) + nl for c in cyc)
    body = "".join("  %s := %s;" % (c, e) + nl for c, e in defs.items())
    return "MODULE main" + nl + "VAR" + nl + var + "DEFINE" + nl + body + asg + nl.join(prop_smv(props)) + nl

def truth(ins, defs, text_defs=None):
    py = lambda s: s.replace("!", " not ").replace("&", " and ").replace("|", " or ")
    res = {}
    defs = {c: e.replace("TRUE", "True").replace("FALSE", "False") for c, e in defs.items()}
    for vals in itertools.product([False, True], repeat=len(ins)):
        env = dict(zip(ins, vals)); changed = True
        local = dict(env)
        for _ in range(len(defs) + 1):
            for c, e in defs.items(): local[c] = bool(eval(py(e), {}, local)) if all(k in local or k in defs or k in ("True", "False") for k in re.findall(r"[A-Za-z_]\w*", e)) else local.get(c, False)
        res[vals] = {c: local[c] for c in defs}
    return res

def parse_existing(smv):
    ins = re.findall(r"^\s+(\w+)\s*:\s*boolean", smv, re.M)
    block = re.search(r"DEFINE(.*?)(?:ASSIGN|INVARSPEC)", smv, re.S).group(1)
    defs = dict(re.findall(r"(\w+)\s*:=\s*([^;]+);", block))
    return ins, defs

if __name__ == "__main__":
    suite, models, nusmv, out = sys.argv[1:5]
    rows = []
    for xml in sorted(glob.glob(suite + "/benchmarks/*/g_*/*.xml")):
        d = os.path.dirname(xml); bid = os.path.basename(d); var = os.path.basename(xml)[:-4]
        b = yaml.safe_load(open(d + "/benchmark.yml"))
        vm = {v["file"][:-4]: v["expected_verdict"] for v in b["variants"]}
        try: text = smv_text(xml, d + "/props.yaml")
        except Exception as e: continue
        ins, defs, cyc = translate(xml)
        tmp = os.path.join(out, "%s__%s.smv" % (bid, var)); open(tmp, "w").write(text)
        o = subprocess.run([nusmv, "-dcx", tmp], capture_output=True, text=True).stdout
        v = "SAFE" if "is true" in o and "is false" not in o else "VIOLATION" if "is false" in o else "unknown"
        exp = "SAFE" if vm.get(var) else "VIOLATION"
        ex = os.path.join(models, "%s__%s.smv" % (bid, var))
        eq = "n/a"
        if os.path.exists(ex):
            i2, d2 = parse_existing(open(ex).read())
            allin = sorted(set(ins) | set(i2))
            t1 = truth(allin, defs); t2 = truth(allin, d2)
            shared = set(defs) & set(d2)
            eq = "equal" if shared and all(t1[k][c] == t2[k][c] for k in t1 for c in shared) else "DIFFERENT"
        rows.append((bid, var, exp, v, "OK" if v == exp else "DIFF", eq))
    open(out + "/translation_check.tsv", "w").write("\n".join("\t".join(r) for r in rows) + "\n")
    import collections; print(len(rows), collections.Counter(r[4] for r in rows), collections.Counter(r[5] for r in rows))
    for r in rows:
        if r[4] != "OK" or r[5] == "DIFFERENT": print(r)
