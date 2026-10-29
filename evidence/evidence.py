import sys, os, glob, json, re, subprocess, collections, tempfile, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xml2smv as X
SUITE, NUSMV, OUT = sys.argv[1:4]
sys.path.insert(0, SUITE + "/tools"); sys.path.insert(0, SUITE + "/runner")
from ld_text_to_xml import translate as t2x
rows = []
rec = {}
for f in glob.glob(SUITE + "/results/records/*.json"):
    d = json.load(open(f)); rec[os.path.basename(f)[:-5]] = d
for bp in sorted(glob.glob(SUITE + "/benchmarks/*/*/benchmark.yml")):
    b = yaml.safe_load(open(bp)); d = os.path.dirname(bp)
    props = yaml.safe_load(open(os.path.join(d, b.get("properties_file", "props.yaml"))))
    pvars = sorted({v for p in props["properties"] for v in re.findall(r"[A-Za-z_]\w*", p.get("expression", "") + " " + " ".join(p.get("variables", []))) if v not in ("AND", "OR", "NOT", "true", "false")})
    for v in b["variants"]:
        f = v["file"]; exp = "SAFE" if v["expected_verdict"] else "VIOLATION"
        name = f.rsplit(".", 1)[0]; key = "%s__%s" % (b["id"], name)
        r = rec.get(key) or rec.get(b["id"] + "__" + ("clean" if v["expected_verdict"] else "bomb")) or {}
        e84 = (r.get("runs", {}).get("v8.4") or {}); e86 = (r.get("runs", {}).get("v8.6") or {})
        nv = "-"
        src = os.path.join(d, f)
        try:
            if f.endswith(".xml"): xmlp = src
            elif f.endswith(".ld"):
                xmlp = os.path.join(OUT, "tmp_%s.xml" % key)
                open(xmlp, "w").write(t2x(name, open(src).read(), [x for x in pvars]))
            else: xmlp = None
            if xmlp:
                text = X.smv_text(xmlp, os.path.join(d, b.get("properties_file", "props.yaml")))
                sp = os.path.join(OUT, "ev_%s.smv" % key); open(sp, "w").write(text)
                o = subprocess.run([NUSMV, sp], capture_output=True, text=True, timeout=120)
                nv = "SAFE" if "is true" in o.stdout and "is false" not in o.stdout else "VIOLATION" if "is false" in o.stdout else "err"
        except Exception as ex:
            nv = "-"
        rows.append(dict(id=b["id"], file=f, domain=b["domain"], lang=b["language"], origin=b["source"]["origin"],
                         status=b.get("validation_status"), method=v["ground_truth"]["method"], diff=b.get("difficulty"),
                         exp=exp, s84=e84.get("status", "-"), v84=e84.get("verdict", "-"), g84=(e84.get("encoding") or {}).get("gate", "-"),
                         s86=e86.get("status", "-"), v86=e86.get("verdict", "-"), g86=(e86.get("encoding") or {}).get("gate", "-"),
                         t84=e84.get("cpu_time_s"), t86=e86.get("cpu_time_s"), nusmv=nv))
json.dump(rows, open(OUT + "/evidence.json", "w"), indent=1)
print(len(rows), collections.Counter(r["nusmv"] for r in rows))
print("nusmv agree", sum(1 for r in rows if r["nusmv"] == r["exp"]), "disagree", sum(1 for r in rows if r["nusmv"] in ("SAFE", "VIOLATION") and r["nusmv"] != r["exp"]))
for r in rows:
    if r["nusmv"] in ("SAFE", "VIOLATION") and r["nusmv"] != r["exp"]: print(r["id"], r["file"], r["exp"], r["nusmv"], r["status"])
