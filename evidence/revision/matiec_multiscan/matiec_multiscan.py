"""Multi-scan differential test against MATIEC's own C (R2.6).

For every ladder variant that the two evaluators of a1_converter_check.py can read, drive (a) the evaluator and
(b) the C that Beremiz and MATIEC (written by others) generate from the same program, with the same random input
sequence over 12 scans and a clock stepped by 10 ms per scan, and compare every shared output after every scan.

    matiec_multiscan.py SUITE VIAC_SUITE OUT [SEEDS]
"""
import csv, glob, json, os, pathlib, random, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import a1_converter_check as a  # noqa: E402

suite, viac, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 20
a.CONV = "--matiec-conventions" in sys.argv
NUSMV = next((x.split("=", 1)[1] for x in sys.argv if x.startswith("--nusmv=")), None)
if NUSMV:
    import xml2smv  # noqa: E402  (the suite's NuSMV translator, in the parent folder)
only = {x for x in sys.argv[5:] if not x.startswith("--")}
sys.path[:0] = [str(viac / "runner"), str(viac / "tools")]
import record_via_c as rvc  # noqa: E402
from ld_text_to_xml import translate  # noqa: E402
SDK = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
LIB = str(rvc.TOOLS / "matiec" / "lib" / "C")
SCANS = 12
out.mkdir(parents=True, exist_ok=True)
rows = [v for v in csv.DictReader(open(HERE.parent / "variants_302.csv")) if v["core_suite"] == "yes" and v["lang"].startswith("LD")]
results = {}
for v in rows:
    name = f"{v['id']}__{v['file'].split('.')[0]}"
    if only and name not in only:
        continue
    f = glob.glob(f"{suite}/benchmarks/*/{v['id']}/{v['file']}")[0]
    text = open(f).read()
    try:
        if v["lang"] == "LD-textual":
            rungs = a.parse_dsl(text)
            coils = {r[1] for r in rungs}
            ins = sorted(set(re.findall(r"X(?:IC|IO)\((\w+)\)", text)) - coils)
            xml = translate("p", text, ins)
            ev = lambda seq: a.run_dsl(rungs, ins, seq)
            timers = bool(re.search(r"\b(TON|TOF|TP)\(", text))
        else:
            xml = text
            if "tc6_0200" not in xml:
                raise ValueError("namespace")
            coils = set(re.findall(r"<coil[^>]*>.*?<variable>([^<]*)</variable>", xml, re.S))
            reads = set(re.findall(r"<contact[^>]*>.*?<variable>([^<]*)</variable>", xml, re.S))
            ins = sorted(reads - coils)
            ev = lambda seq: a.run_xml(xml, ins, seq)
            timers = bool(re.search(r'typeName="(TON|TOF|TP)"', xml))
        rng = random.Random(7)
        seqs = [[{x: rng.random() < 0.5 for x in ins} for _ in range(SCANS)] for _ in range(seeds)]
        evals = [ev(s) for s in seqs]
    except Exception as e:
        results[name] = {"status": "skipped", "reason": str(e)[:60]}; continue
    work = pathlib.Path(tempfile.mkdtemp()); xf = work / "p.xml"; xf.write_text(xml)
    try:
        st = rvc.to_st(xf, work); (work / "prog.st").write_text(st)
        (work / "c").mkdir()
        code, o = rvc.run([str(rvc.TOOLS / "matiec" / "iec2c"), "-I", str(rvc.TOOLS / "matiec" / "lib"), "-T", str(work / "c"), str(work / "prog.st")])
        if code:
            raise RuntimeError("iec2c: " + o[-80:])
        header = (work / "c" / "POUS.h").read_text()
        struct = rvc.entry_struct(xf, header); pou = struct[:-len("_data__")]
    except Exception as e:
        results[name] = {"status": "skipped", "reason": "toolchain: " + str(e)[:60]}; continue
    shared = sorted(c for c in coils if re.search(rf"\b{c.upper()}\b", header))
    body = ""
    for k, s in enumerate(seqs):
        body += "  d = (" + struct + "){0}; " + pou + "_init__(&d,0); __CURRENT_TIME.tv_sec=0; __CURRENT_TIME.tv_nsec=0;\n"
        body += "  for (int s=0; s<%d; s++) {\n" % SCANS
        for x in ins:
            arr = ",".join("1" if st_[x] else "0" for st_ in s)
            body += f"    {{ static const int a_{x}[{SCANS}] = {{{arr}}}; if (strstr(HDR, \"{x.upper()}\")) __SET_VAR(d., {x.upper()}, , a_{x}[s]); }}\n"
        body += f"    {pou}_body__(&d);\n    printf(\"{k} %d\"" + "".join(", (int)__GET_VAR(d.%s,)" % c.upper() for c in shared) + ", s);\n"
        body = body.replace('printf("%d %d' , 'printf("%d %d')
        body += "    printf(\"\\n\"); __CURRENT_TIME.tv_nsec += 10000000;\n  }\n"
    fmt = "".join(" %d" for _ in shared)
    body = body.replace('printf("%d"' + "".join(", (int)__GET_VAR(d.%s,)" % c.upper() for c in shared) + ", s);", 'printf("%d' + fmt + '\\n", 0' + ")", 0)
    # simpler, explicit printing: rebuild the body without the templating above
    body = ""
    for k, s in enumerate(seqs):
        body += f"  d = ({struct}){{0}}; {pou}_init__(&d,0); __CURRENT_TIME.tv_sec=0; __CURRENT_TIME.tv_nsec=0;\n  for (int s=0; s<{SCANS}; s++) {{\n"
        for x in ins:
            arr = ",".join("1" if st_[x] else "0" for st_ in s)
            body += f"    {{ static const int a_{k}_{x}[{SCANS}] = {{{arr}}}; __SET_VAR(d., {x.upper()}, , a_{k}_{x}[s]); }}\n"
        body += f"    {pou}_body__(&d);\n    printf(\"{k} %d" + fmt + "\\n\", s" + "".join(f", (int)__GET_VAR(d.{c.upper()},)" for c in shared) + ");\n    __CURRENT_TIME.tv_nsec += 10000000;\n  }\n"
    c = (f'#include <stdio.h>\n#include "iec_std_lib.h"\n#include "POUS.h"\n#include "POUS.c"\nTIME __CURRENT_TIME;\n'
         f"int main(void) {{\n  {struct} d;\n{body}  return 0;\n}}\n")
    (work / "c" / "h.c").write_text(c)
    r = subprocess.run(["clang", "-w", "-isysroot", SDK, "-I", LIB, "-I", str(work / "c"), str(work / "c" / "h.c"), "-o", str(work / "h")], capture_output=True, text=True)
    if r.returncode:
        results[name] = {"status": "skipped", "reason": "compile: " + r.stderr[-80:]}; continue
    o = subprocess.run([str(work / "h")], capture_output=True, text=True, timeout=60).stdout.split("\n")
    got = {}
    for line in o:
        p = line.split()
        if len(p) == 2 + len(shared):
            got[(int(p[0]), int(p[1]))] = {c_: bool(int(x)) for c_, x in zip(shared, p[2:])}
    bad = 0; first = None
    for k, tr in enumerate(evals):
        for s_, env in enumerate(tr):
            g = got.get((k, s_))
            if g is None or any(bool(env.get(c_)) != g[c_] for c_ in shared):
                bad += 1
                first = first or (k, s_)
    flip_saved = [False]
    nusmv_res = None
    if NUSMV:
        try:
            ins_s, defs_s, cyc_s = xml2smv.translate(str(xf))
        except Exception as e:
            nusmv_res = "not translatable: " + str(e)[:40]
        else:
            check = [c_ for c_ in shared if c_ in defs_s]
            K = min(len(seqs), 20)
            def smv_text(flip):
                nl = chr(10)
                src = []
                for x in ins_s:
                    arms = "".join(f"k={k_} & t={t_} : {'TRUE' if seqs[k_][t_].get(x) else 'FALSE'}; " for k_ in range(K) for t_ in range(SCANS))
                    src.append(f"  {x} := case {arms}TRUE : FALSE; esac;")
                body = "".join(f"  {c_} := {e_};{nl}" for c_, e_ in defs_s.items())
                terms = []
                for k_ in range(K):
                    for t_ in range(SCANS):
                        for c_ in check:
                            val = got[(k_, t_)][c_]
                            if flip and (k_, t_, c_) == (0, 0, check[0]):
                                val = not val
                            terms.append(f"(k={k_} & t={t_} -> {c_} = {'TRUE' if val else 'FALSE'})")
                raw = ("MODULE main" + nl + "FROZENVAR" + nl + f"  k : 0..{K - 1};" + nl + "VAR" + nl + f"  t : 0..{SCANS};" + nl
                       + "".join(f"  {c_}_prev : boolean;" + nl for c_ in cyc_s) + "DEFINE" + nl + nl.join(src) + nl + body + "ASSIGN" + nl
                       + f"  init(t) := 0;{nl}  next(t) := case t < {SCANS} : t + 1; TRUE : {SCANS}; esac;{nl}"
                       + "".join(f"  init({c_}_prev) := FALSE;{nl}  next({c_}_prev) := {c_};{nl}" for c_ in cyc_s)
                       + ("-- CONTROLFLAG" + nl if flip else "") + "INVARSPEC " + " & ".join(terms) + ";" + nl)
                names = set(ins_s) | set(defs_s) | {c_ + "_prev" for c_ in cyc_s}
                return xml2smv.mangle(raw, names)
            def run_smv(text):
                f_ = work / "m.smv"; f_.write_text(text)
                kind_ = "control" if "CONTROLFLAG" in text else "match"
                (out / (name + "." + kind_ + ".smv")).write_text(text)
                o_ = subprocess.run([NUSMV, "-dcx", str(f_)], capture_output=True, text=True).stdout
                return "true" if "is true" in o_ and "is false" not in o_ else "false" if "is false" in o_ else "unknown"
            if not check or any(g is None for g in got.values()):
                nusmv_res = "nothing to compare"
            else:
                nusmv_res = {"match": run_smv(smv_text(False)), "control": run_smv(smv_text(True)), "outputs": len(check)}
    results[name] = {"status": "run", "timers": timers, "shared": len(shared), "mismatching_scans": bad, "total_scans": seeds * SCANS, "first": first, "nusmv": nusmv_res}
    print(name, results[name], flush=True)
json.dump(results, open(out / "results.json", "w"), indent=1)
print("FINISHED", flush=True)
