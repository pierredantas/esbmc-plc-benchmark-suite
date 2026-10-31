"""Objective test of retained state: does a program's output depend on history? (R1.1)

For each core benchmark (first variant), compile the program to C with Beremiz and MATIEC, then in many trials run it
from a fresh state through two different random input histories and give both the same final input vector. If any
non-input variable differs after the final scan, the program retains state between scans. Located I/O addresses are
removed and the located inputs are driven as ordinary variables, the harness adjustment used for the other
differential tests. Time advances by 10 ms per scan.

    history_dependence.py SUITE_BENCHMARKS VIAC_SUITE OUT.json [TRIALS]
"""
import csv
import glob
import json
import pathlib
import random
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
suite, viac, out = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
TRIALS = int(sys.argv[4]) if len(sys.argv) > 4 else 150
H = 6
sys.path[:0] = [str(viac / "runner"), str(viac / "tools")]
import record_via_c as rvc  # noqa: E402
from ld_text_to_xml import translate  # noqa: E402

SDK = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
LIB = str(rvc.TOOLS / "matiec" / "lib" / "C")
rows = {}
for v in csv.DictReader(open(HERE.parent / "variants_302.csv")):
    if v["core_suite"] == "yes":
        rows.setdefault(v["id"], v)


def program_text(st):
    """The PROGRAM block of the generated ST, without its configuration."""
    st = re.sub(r"\(\*.*?\*\)", "", st, flags=re.S)
    st = st.split("CONFIGURATION", 1)[0]
    m = re.search(r"PROGRAM\s+(\w+)(.*?)END_PROGRAM", st, re.S)
    return st, m.group(1), m.group(2)


def split_inputs(body):
    """Input names (VAR_INPUT or located %I) of a PROGRAM body."""
    ins = []
    for kind, block in re.findall(r"(VAR\w*)\s(.*?)END_VAR", body, re.S):
        for ln in block.splitlines():
            m = re.match(r"\s*(\w+)\s*(AT\s+%(\w)\S*)?\s*:\s*(\w+)", ln)
            if not m:
                continue
            if kind == "VAR_INPUT" or (m.group(3) or "").upper() == "I":
                ins.append((m.group(1).upper(), m.group(4).upper()))
    return ins


results = {}
for bid, v in sorted(rows.items()):
    d = pathlib.Path(glob.glob(f"{suite}/*/{bid}")[0])
    f = d / v["file"]
    work = pathlib.Path(tempfile.mkdtemp())
    try:
        if v["lang"] == "LD-textual":
            xf = work / "p.xml"
            xf.write_text(translate("p", f.read_text(), sorted(set(re.findall(r"X(?:IC|IO)\((\w+)\)", f.read_text())))))
            st = rvc.to_st(xf, work)
        else:
            st = rvc.to_st(f, work)
        st_full, pname, body = program_text(st)
        ins = split_inputs(body)
        if not ins:   # every variable declared local: inputs are the scalar variables that the body never assigns
            decl = re.findall(r"^\s*(\w+)\s*(?:AT\s+%\S+)?\s*:\s*(BOOL|INT|DINT)", body, re.M)
            code_part = body[body.rfind("END_VAR") + 7:]
            assigned = set(re.findall(r"^\s*(\w+)\s*:=", code_part, re.M)) | set(re.findall(r"\b(\w+)\s*:=", code_part))
            ins = [(n.upper(), t.upper()) for n, t in decl if n not in assigned]
        st_clean = re.sub(r"\s+AT\s+%\S+", "", st_full)
        (work / "prog.st").write_text(st_clean)
        (work / "c").mkdir()
        code, o = rvc.run([str(rvc.TOOLS / "matiec" / "iec2c"), "-I", str(rvc.TOOLS / "matiec" / "lib"), "-T", str(work / "c"), str(work / "prog.st")])
        if code:
            raise RuntimeError("iec2c: " + o[-70:])
        header = (work / "c" / "POUS.h").read_text()
        struct = pname.upper() + "_data__"
        end = header.find("} " + struct + ";")
        own_text = header[header.rfind("typedef struct", 0, end):end] if end > 0 else header
        fields = [n for _k, t, n in rvc.declared_vars(own_text) if t.upper() in ("BOOL", "INT", "DINT", "SINT", "UINT", "UDINT", "USINT", "WORD", "BYTE")]
        ins = [(n, t) for n, t in ins if n not in ("EN", "ENO")]
        in_names = {n for n, _ in ins}
        state_vars = [n for n in fields if n.upper() not in in_names and n.upper() not in ("EN", "ENO") and re.search(rf"\b{n}\b", header)]
        pou = pname.upper()
        rng = random.Random(11)
        def val(t):
            return rng.randint(0, 1) if t == "BOOL" else rng.randint(-4, 6)
        body_c = ""
        for k in range(TRIALS):
            fin = {n: val(t) for n, t in ins}
            for run in "AB":
                body_c += f"  d = ({struct}){{0}}; {pou}_init__(&d,0); __CURRENT_TIME.tv_sec=0; __CURRENT_TIME.tv_nsec=0;\n"
                for s in range(H + 1):
                    for n, t in ins:
                        x = fin[n] if s == H else val(t)
                        body_c += f"  __SET_VAR(d., {n}, , {x});\n"
                    body_c += f"  {pou}_body__(&d); __CURRENT_TIME.tv_nsec += 10000000;\n"
                body_c += f'  printf("{k} {run}' + "".join(" %d" for _ in state_vars) + '\\n"' + "".join(f", (int)__GET_VAR(d.{n},)" for n in state_vars) + ");\n"
        c = (f'#include <stdio.h>\n#include "iec_std_lib.h"\n#include "POUS.h"\n#include "POUS.c"\nTIME __CURRENT_TIME;\n'
             f"int main(void) {{\n  {struct} d;\n{body_c}  return 0;\n}}\n")
        (work / "c" / "h.c").write_text(c)
        r = subprocess.run(["clang", "-w", "-isysroot", SDK, "-I", LIB, "-I", str(work / "c"), str(work / "c" / "h.c"), "-o", str(work / "h")], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("compile: " + " | ".join(l.split("error:",1)[1].strip()[:70] for l in r.stderr.splitlines() if "error:" in l)[:230])
        lines = subprocess.run([str(work / "h")], capture_output=True, text=True, timeout=120).stdout.split("\n")
        seen = {}
        for ln in lines:
            p = ln.split()
            if len(p) == 2 + len(state_vars):
                seen[(p[0], p[1])] = p[2:]
        differ = sorted({state_vars[i] for k in range(TRIALS) for i in range(len(state_vars)) if seen.get((str(k), "A"), [None] * len(state_vars))[i] != seen.get((str(k), "B"), [None] * len(state_vars))[i]})
        results[bid] = {"status": "ok", "history_dependent": bool(differ), "variables_that_differ": differ[:8], "inputs": len(ins), "state_candidates": len(state_vars)}
    except Exception as e:  # noqa: BLE001
        results[bid] = {"status": "failed", "reason": str(e)[:90]}
    print(bid, results[bid], flush=True)
json.dump(results, open(out, "w"), indent=1)
print("FINISHED", flush=True)
