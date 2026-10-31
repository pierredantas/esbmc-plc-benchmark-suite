"""Do the graphical re-encodings of the K-LD programs compute what their textual sources compute? (R2.4)

For each g_X with a textual twin ld_X, evaluate the textual source with the DSL evaluator and the graphical
program with the XML evaluator of a1_converter_check.py, on random input sequences, and compare every coil.
    twin_check.py SUITE
"""
import glob, json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a1_converter_check as a

S = sys.argv[1]
random.seed(3)
ok = bad = 0
for g in sorted(glob.glob(f"{S}/benchmarks/*/g_*/")):
    gid = os.path.basename(g.rstrip("/"))
    t = glob.glob(f"{S}/benchmarks/*/ld_{gid[2:]}/*.ld")
    x = glob.glob(g + "*.xml")
    if not t or not x:
        continue
    text = open(t[0]).read(); xml = open(x[0]).read()
    rungs = a.parse_dsl(text); src_coils = {r[1] for r in rungs}
    ins = sorted(set(re.findall(r"X(?:IC|IO)\((\w+)\)", text)) - src_coils)
    xml_coils = set(re.findall(r"<coil[^>]*>.*?<variable>([^<]*)</variable>", xml, re.S))
    coils = src_coils & xml_coils
    mism = 0
    for _ in range(1500):
        p = random.choice([0.2, 0.5, 0.8])
        seq = [{v: random.random() < p for v in ins} for _ in range(random.choice([1, 2, 4, 12]))]
        try:
            t1 = a.run_dsl(rungs, ins, seq); t2 = a.run_xml(xml, ins, seq)
        except Exception as e:
            mism = -1; err = repr(e)[:80]; break
        if any(p1.get(c) != p2.get(c) for p1, p2 in zip(t1, t2) for c in coils): mism += 1
    print(f"{gid:22s} vs ld_{gid[2:]:20s} compared coils={sorted(coils)} mismatches={mism}" + (f" {err}" if mism < 0 else ""))
    ok += mism == 0; bad += mism != 0
print("twins equal:", ok, "differ or unreadable:", bad)
