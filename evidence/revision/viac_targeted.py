"""Run the Beremiz, MATIEC, ESBMC C route on the variants that no NuSMV or PLCverif run confirms (R1.1, R2.6).

    viac_targeted.py SUITE ESBMC OUT [--timeout 120] [--scans 8]
"""
import csv, glob, json, os, pathlib, subprocess, sys

suite, esbmc, out = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
timeout = sys.argv[sys.argv.index("--timeout") + 1] if "--timeout" in sys.argv else "120"
scans = sys.argv[sys.argv.index("--scans") + 1] if "--scans" in sys.argv else "8"
here = pathlib.Path(__file__).resolve().parent
confirmed = set(json.load(open(here / "plcverif_st" / "cost.json")))
out.mkdir(parents=True, exist_ok=True)
rows = [v for v in csv.DictReader(open(here / "variants_302.csv")) if v["core_suite"] == "yes"]
todo = [v for v in rows if f"{v['id']}__{v['file'].split('.')[0]}" not in confirmed]
print(len(todo), "variants", flush=True)
for v in todo:
    name = f"{v['id']}__{v['file'].split('.')[0]}"
    d = next((suite / "benchmarks").glob(f"*/{v['id']}"))
    prog = d / v["file"]
    if v["lang"] == "LD-textual":
        print(name, "skipped: textual ladder (all confirmed elsewhere)"); continue
    dest = out / f"{name}.json"
    if dest.exists():
        continue
    r = subprocess.run([sys.executable, "runner/record_via_c.py", str(prog.relative_to(suite)),
                        str((d / "props.yaml").relative_to(suite)), "true" if v["exp"] == "SAFE" else "false",
                        "--tool", f"v8.6={esbmc}", "--timeout", timeout, "--scans", scans, "-o", str(dest)],
                       cwd=suite, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(name, v["exp"], "->", last[-90:], flush=True)
print("FINISHED", flush=True)
