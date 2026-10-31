"""Is each surviving mutant observably different from its program? (R2.4)

For every surviving mutant, run the original program and the mutant through Beremiz and MATIEC C with the same random
input sequences (a clock stepped 10 ms per scan) and compare every scalar variable after every scan. A mutant that
never differs is behaviorally equivalent to the original over the sequences tried, so it cannot be a fault that the
clause requires the properties to catch. Located I/O addresses are removed and located inputs are driven as ordinary
variables, as in the other differential tests.

    mutant_equivalence.py SUITE_ROOT VIAC_SUITE MUTANT_DIR OUT.json [SEQUENCES]
"""
import glob
import json
import pathlib
import random
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
suite, viac, mut_dir, out = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4]
NSEQ = int(sys.argv[5]) if len(sys.argv) > 5 else 200
SCANS = 10
sys.path[:0] = [str(viac / "runner"), str(viac / "tools")]
import record_via_c as rvc  # noqa: E402

SDK = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
LIB = str(rvc.TOOLS / "matiec" / "lib" / "C")
mut = json.load(open(HERE.parent / "mutation_results.json"))


def program_parts(st):
    st = re.sub(r"\(\*.*?\*\)", "", st, flags=re.S).split("CONFIGURATION", 1)[0]
    m = re.search(r"PROGRAM\s+(\w+)(.*?)END_PROGRAM", st, re.S)
    return st, m.group(1), m.group(2)


def inputs_of(body):
    ins = []
    for kind, block in re.findall(r"(VAR\w*)\s(.*?)END_VAR", body, re.S):
        for ln in block.splitlines():
            m = re.match(r"\s*(\w+)\s*(AT\s+%(\w)\S*)?\s*:\s*(\w+)", ln)
            if m and (kind == "VAR_INPUT" or (m.group(3) or "").upper() == "I"):
                ins.append((m.group(1).upper(), m.group(4).upper()))
    if not ins:
        decl = re.findall(r"^\s*(\w+)\s*(?:AT\s+%\S+)?\s*:\s*(BOOL|INT|DINT)", body, re.M)
        code = body[body.rfind("END_VAR") + 7:]
        assigned = set(re.findall(r"\b(\w+)\s*:=", code))
        ins = [(n.upper(), t.upper()) for n, t in decl if n not in assigned]
    return [(n, t) for n, t in ins if n not in ("EN", "ENO")]


def build(path):
    work = pathlib.Path(tempfile.mkdtemp())
    st = rvc.to_st(path, work)
    st_full, pname, body = program_parts(st)
    ins = inputs_of(body)
    (work / "prog.st").write_text(re.sub(r"\s+AT\s+%\S+", "", st_full))
    (work / "c").mkdir()
    code, o = rvc.run([str(rvc.TOOLS / "matiec" / "iec2c"), "-I", str(rvc.TOOLS / "matiec" / "lib"), "-T", str(work / "c"), str(work / "prog.st")])
    if code:
        raise RuntimeError("iec2c: " + o[-80:])
    header = (work / "c" / "POUS.h").read_text()
    struct = pname.upper() + "_data__"
    end = header.find("} " + struct + ";")
    own = header[header.rfind("typedef struct", 0, end):end]
    names = {n for n, _ in ins}
    fields = [n for _k, t, n in rvc.declared_vars(own) if t.upper() in ("BOOL", "INT", "DINT", "SINT", "UINT", "UDINT", "USINT", "WORD", "BYTE")
              and n.upper() not in ("EN", "ENO")]
    return work, struct, pname.upper(), ins, [n for n in fields if n.upper() not in names]


def run(prog, ins, seqs):
    work, struct, pou, my_ins, state = prog
    body = ""
    for k, seq in enumerate(seqs):
        body += f"  d = ({struct}){{0}}; {pou}_init__(&d,0); __CURRENT_TIME.tv_sec=0; __CURRENT_TIME.tv_nsec=0;\n"
        for s in range(SCANS):
            for n, _t in ins:
                body += f"  __SET_VAR(d., {n}, , {seq[s][n]});\n"
            body += f"  {pou}_body__(&d); __CURRENT_TIME.tv_nsec += 10000000;\n"
            body += f'  printf("{k} {s}' + "".join(" %d" for _ in state) + '\\n"' + "".join(f", (int)__GET_VAR(d.{n},)" for n in state) + ");\n"
    c = (f'#include <stdio.h>\n#include "iec_std_lib.h"\n#include "POUS.h"\n#include "POUS.c"\nTIME __CURRENT_TIME;\n'
         f"int main(void) {{\n  {struct} d;\n{body}  return 0;\n}}\n")
    (work / "c" / "h.c").write_text(c)
    r = subprocess.run(["clang", "-w", "-isysroot", SDK, "-I", LIB, "-I", str(work / "c"), str(work / "c" / "h.c"), "-o", str(work / "h")], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("compile: " + " | ".join(l.split("error:", 1)[1].strip()[:60] for l in r.stderr.splitlines() if "error:" in l)[:200])
    lines = subprocess.run([str(work / "h")], capture_output=True, text=True, timeout=180).stdout.split("\n")
    return {tuple(p[:2]): p[2:] for p in (ln.split() for ln in lines) if len(p) == 2 + len(state)}


results = {}
for bid, rec in mut.items():
    d = pathlib.Path(glob.glob(f"{suite}/benchmarks/*/{bid}")[0])
    base = d / rec["base"]
    try:
        bp = build(base)
    except Exception as e:  # noqa: BLE001
        results[bid] = {"error": "base: " + str(e)[:100]}
        print(bid, results[bid], flush=True)
        continue
    ins = bp[3]
    rng = random.Random(5)
    seqs = [[{n: (rng.randint(0, 1) if t == "BOOL" else rng.randint(-4, 6)) for n, t in ins} for _ in range(SCANS)] for _ in range(NSEQ)]
    base_trace = run(bp, ins, seqs)
    for i, s in enumerate(rec["survivors"], 1):
        f = mut_dir / f"{bid}_S{i}{base.suffix}"
        key = f"{bid}:S{i}"
        try:
            mp = build(f)
            tr = run(mp, ins, seqs)
            names = bp[4]
            diff = sorted({names[j] for k, v in base_trace.items() for j in range(len(names)) if tr.get(k, [None] * len(names))[j] != v[j]})
            results[key] = {"mutant": s["mutant"], "equivalent": not diff, "variables_that_differ": diff[:6]}
        except Exception as e:  # noqa: BLE001
            results[key] = {"mutant": s["mutant"], "error": str(e)[:120]}
        print(key, {k: v for k, v in results[key].items() if k != "mutant"}, flush=True)
json.dump(results, open(out, "w"), indent=1)
print("FINISHED", flush=True)
