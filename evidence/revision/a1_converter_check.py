"""A1: independent evaluator of the .ld DSL vs an evaluator of the converter's PLCopen XML.
Block semantics (TON/TOF/TP/CTU/CTD) are shared; the check targets the converter's wiring."""
import sys, re, random, glob, xml.etree.ElementTree as ET
sys.path.insert(0, "/Users/user/Claude/suite-v120-run")
from tools.ld_text_to_xml import translate

# ---- shared block semantics (IEC 61131-3 standard function blocks, one call per scan)
CONV = False   # True: MATIEC's conventions (real-time TON/TOF and CTD, counter starting at 0) instead of the scan-counting ones


def blk_matiec(kind, st, a, b, c, pv):
    if kind == "TON":
        st["et"] = st.get("et", -1) + 1 if a else -1
        return a and st["et"] >= pv
    if kind == "TOF":
        if a:
            st["q"], st["et"] = True, -1
        elif st.get("q"):
            st["et"] = st.get("et", -1) + 1
            st["q"] = st["et"] < pv
        return st.get("q", False)
    if kind == "CTD":
        cv = st.get("cv", 0)
        if b: cv = pv
        elif a and not st.get("prev", False) and cv > 0: cv -= 1
        st["prev"], st["cv"] = a, cv
        return cv <= 0
    return None


def blk(kind, st, a, b, c, pv):
    if CONV:
        r = blk_matiec(kind, st, a, b, c, pv)
        if r is not None:
            return r
    if kind == "TON":
        st["et"] = min(st.get("et", 0) + 1, pv) if a else 0
        return a and st["et"] >= pv
    if kind == "TOF":
        if a: st["et"] = 0; return True
        st["et"] = min(st.get("et", pv) + 1, pv)
        return st["et"] < pv
    if kind == "TP":
        if st.get("run"):
            st["et"] += 1
            if st["et"] >= pv: st["run"] = False
        elif a and not st.get("prev", False): st["run"] = True; st["et"] = 0
        st["prev"] = a
        return st.get("run", False)
    if kind == "CTU":
        cv = st.get("cv", 0)
        if b: cv = 0
        elif a and not st.get("prev", False) and cv < pv: cv += 1
        st["prev"], st["cv"] = a, cv; return cv >= pv
    if kind == "CTD":
        cv = st.get("cv", pv)
        if b: cv = pv
        elif a and not st.get("prev", False) and cv > 0: cv -= 1
        st["prev"], st["cv"] = a, cv; return cv <= 0

# ---- evaluator 1: direct interpretation of the DSL text (own tokenizer, no tools.* code)
TOK = re.compile(r"\s*(XIC|XIO|TRUE|FALSE|[A-Za-z_]\w*|\d+|\(|\)|\*|\+|,|:=|;)")
def toks(s):
    out, p = [], 0
    s = re.sub(r"//[^\n]*", "", s)
    while p < len(s.rstrip()):
        m = TOK.match(s, p); assert m, s[p:p+20]; out.append(m.group(1)); p = m.end()
    return out
def pexpr(t):
    def orx():
        l = [andx()]
        while t and t[0] == "+": t.pop(0); l.append(andx())
        return ("or", l)
    def andx():
        l = [fac()]
        while t and t[0] == "*": t.pop(0); l.append(fac())
        return ("and", l)
    def fac():
        x = t.pop(0)
        if x in ("XIC", "XIO"):
            t.pop(0); v = t.pop(0); t.pop(0); return ("var", v, x == "XIO")
        if x == "TRUE": return ("lit", True)
        if x == "FALSE": return ("lit", False)
        assert x == "("; e = orx(); assert t.pop(0) == ")"; return e
    return orx()
def ev(e, env):
    k = e[0]
    if k == "var": return env.get(e[1], False) != e[2]
    if k == "lit": return e[1]
    f = all if k == "and" else any
    return f(ev(x, env) for x in e[1])
def parse_dsl(text):
    rungs = []
    for stmt in toks(text) and " ".join(toks(text)).split(" ; "):
        t = stmt.replace(" ;", "").split()
        if not t: continue
        op = t[0]; t = t[1:]
        if op in ("OTE", "OTL", "OTU"):
            assert t.pop(0) == "("; c = t.pop(0); t.pop(0); t.pop(0)
            rungs.append((op, c, pexpr(t)))
        else:
            assert t.pop(0) == "("; q = t.pop(0); t.pop(0); n = int(t.pop(0)); t.pop(0)
            a = pexpr(t); b = None
            if t and t[0] == ",": t.pop(0); b = pexpr(t)
            rungs.append((op, q, n, a, b))
    return rungs
def run_dsl(rungs, ins, seq):
    env, sts, trace = {}, {}, []
    for step in seq:
        env.update(step)
        for i, r in enumerate(rungs):
            if r[0] == "OTE": env[r[1]] = ev(r[2], env)
            elif r[0] == "OTL":
                if ev(r[2], env): env[r[1]] = True
            elif r[0] == "OTU":
                if ev(r[2], env): env[r[1]] = False
            else:
                a = ev(r[3], env); b = ev(r[4], env) if r[4] is not None else False
                env[r[1]] = bool(blk(r[0], sts.setdefault(i, {}), a, b, None, r[2]))
        trace.append(dict(env))
    return trace

# ---- evaluator 2: interpretation of the converter's PLCopen XML
Q = lambda t: "{http://www.plcopen.org/xml/tc6_0200}" + t
def run_xml(xml, ins, seq):
    ld = ET.fromstring(xml).find(".//" + Q("body") + "/" + Q("LD"))
    nodes = {}
    for e in ld:
        tag = e.tag.split("}")[1]
        if tag in ("leftPowerRail", "rightPowerRail"): nodes[int(e.get("localId"))] = (tag, e); continue
        nodes[int(e.get("localId"))] = (tag, e)
    order = [int(e.get("localId")) for e in ld if e.tag.split("}")[1] in ("coil", "block")]
    env, sts, trace = {}, {}, []
    def src_of(e):
        return [(int(c.get("refLocalId")), c.get("formalParameter")) for c in e.iter(Q("connection"))]
    for step in seq:
        env.update(step); val = {}
        def out(i, pin=None):
            tag, e = nodes[i]
            if (i, pin) in val: return val[(i, pin)]
            if tag == "leftPowerRail": r = True
            elif tag == "inVariable": r = e.findtext(Q("expression"))
            elif tag == "contact":
                inc = any(out(s, p) for s, p in src_of(e)) if src_of(e) else False
                v = env.get(e.findtext(Q("variable")), False)
                r = inc and (v != (e.get("negated") == "true"))
            elif tag == "coil": r = any(out(s, p) for s, p in src_of(e))
            else: raise ValueError(tag)
            val[(i, pin)] = r; return r
        for i in order:
            tag, e = nodes[i]
            if tag == "block":
                pins = {v.get("formalParameter"): [(int(c.get("refLocalId")), c.get("formalParameter")) for c in v.iter(Q("connection"))]
                        for v in e.find(Q("inputVariables"))}
                def pv(name):
                    return any(out(s, p) for s, p in pins.get(name, [])) if name in pins else False
                kind = e.get("typeName")
                preset = [out(s, p) for s, p in pins.get("PT" if kind in ("TON","TOF","TP") else "PV", [])]
                n = preset[0] if preset else None
                n = int(re.match(r"T#(\d+)ms", n).group(1)) // 10 if kind in ("TON","TOF","TP") else int(n)
                a = pv("IN" if n is not None and kind in ("TON","TOF","TP") else ("CU" if kind == "CTU" else "CD"))
                b = pv("R" if kind == "CTU" else "LD") if kind in ("CTU","CTD") else False
                r = bool(blk(kind, sts.setdefault(i, {}), a, b, None, n)); val[(i, "Q")] = r; val[(i, None)] = r
            else:
                r = out(i); st = e.get("storage", "none"); var = e.findtext(Q("variable"))
                if e.get("negated") == "true": r = not r
                if st == "set":
                    if r: env[var] = True
                elif st == "reset":
                    if r: env[var] = False
                else: env[var] = r
                val[(i, None)] = r
            if tag == "block":
                for s in e.iter(Q("variable")):
                    pass
        # block Q is wired to its coil; coil already handled in `order` after block
        trace.append(dict(env))
    return trace

def mutate(xml, how):
    if how == "neg": return xml.replace('negated="false" storage="none" edge="none"', 'negated="true" storage="none" edge="none"', 1)
    if how == "rung": return xml.replace("</contact>", "</contact>", 1)
    return xml

def main(files):
    if files and files[0] == "--mutate":
        files = files[1:]; random.seed(2); caught = 0
        for f in files:
            text = open(f).read(); rungs = parse_dsl(text); coils = {r[1] for r in rungs}
            ins = sorted(set(re.findall(r"X(?:IC|IO)\((\w+)\)", text)) - coils)
            xml = mutate(translate("p", text), "neg")
            if xml == translate("p", text): continue
            m = 0
            for _ in range(1500):
                seq = [{v: random.random() < .5 for v in ins} for _ in range(6)]
                t1 = run_dsl(rungs, ins, seq); t2 = run_xml(xml, ins, seq)
                m += any(a.get(c) != b.get(c) for a, b in zip(t1, t2) for c in coils)
            caught += m > 0
        print("mutated (first contact negated) programs flagged:", caught, "of", len(files)); return
    random.seed(1); bad = 0
    for f in files:
        text = open(f).read(); name = f.split("/")[-2] + "/" + f.split("/")[-1]
        rungs = parse_dsl(text)
        coils = {r[1] for r in rungs}
        reads = set(re.findall(r"X(?:IC|IO)\((\w+)\)", text)); ins = sorted(reads - coils)
        xml = translate("p", text)
        mism = 0; nseq = 3000
        for _ in range(nseq):
            p = random.choice([0.2, 0.5, 0.8])
            seq = [{v: random.random() < p for v in ins} for _ in range(random.choice([1, 2, 4, 12]))]
            t1 = run_dsl(rungs, ins, seq); t2 = run_xml(xml, ins, seq)
            if any(a.get(c) != b.get(c) for a, b in zip(t1, t2) for c in coils): mism += 1
        print(f"{name:55s} inputs={len(ins)} rungs={len(rungs)} mismatches={mism}/{nseq}"); bad += mism > 0
    print("programs with a mismatch:", bad, "of", len(files))
if __name__ == "__main__":
    main(sys.argv[1:])
