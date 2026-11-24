#!/usr/bin/env python3
"""Build the expert-audit package: a stratified sample, a review sheet, and a review pack.

Run from the repository root: python3 evidence/expert_audit/build_sample.py
The selection is deterministic (fixed seed), so the package can be rebuilt from the descriptors.
"""
import csv, glob, os, random, yaml

SEED = 20261123
OUT = os.path.join("evidence", "expert_audit")
V = {(r["id"], r["file"]): r for r in csv.DictReader(open("evidence/variants_302.csv"))}

def pexpr(p):
    return p.get("expression") or ("at most one of " + ", ".join(p["variables"]) if "variables" in p else "every scan cycle terminates within the iteration budget")

B = {}
for p in glob.glob("benchmarks/*/*/benchmark.yml"):
    d = yaml.safe_load(open(p)); d["_dir"] = os.path.dirname(p); B[d["id"]] = d

timer = sorted(i for i, d in B.items() if "timer_counter_model" in d["semantics"])
counter = sorted(i for i, d in B.items() if any(f in d.get("features", []) for f in ("ctu", "ctd", "counter", "counter_ctu")) and i not in timer)
latch = sorted(i for i, d in B.items() if "latch" in d.get("features", []) or "seal_in" in d.get("features", []))
overflow = sorted(i for i, d in B.items() if "arithmetic" in d["semantics"])
control = sorted(i for i, d in B.items() if d["semantics"]["verdict_scope"] == "holds under the stated scan order"
                 and i not in timer + counter + latch + overflow and d["validation_status"] == "validated")

rng = random.Random(SEED)
strata = [
    ("timer or counter model", rng.sample(timer + counter, 12)),
    ("latch or seal-in", rng.sample([i for i in latch if i not in timer + counter + overflow], 8)),
    ("integer overflow (H1)", rng.sample(overflow, 6)),
    ("control (no timer, counter, latch or overflow dependence)", rng.sample(control, 4)),
]

rows, sheet = [], []
for name, ids in strata:
    for i in sorted(ids):
        d = B[i]; s = d["semantics"]
        props = yaml.safe_load(open(os.path.join(d["_dir"], d["properties_file"])))["properties"]
        for v in d["variants"]:
            e = V.get((i, v["file"]), {})
            rows.append(dict(stratum=name, benchmark=i, domain=d["domain"], language=d["language"], origin=d["source"]["origin"],
                             validation_status=d["validation_status"], variant=v["file"],
                             expected_verdict="SAFE" if v["expected_verdict"] else "VIOLATION", method=v["verdict_basis"]["method"],
                             scan_order=s["scan_order"], retained_state=s.get("retained_state", ""),
                             timer_counter_model=s.get("timer_counter_model", ""), arithmetic=s.get("arithmetic", ""),
                             verdict_scope=s["verdict_scope"], esbmc86=e.get("s86", ""), nusmv=e.get("nusmv", ""),
                             program_path=os.path.join(d["_dir"], v["file"])))
            sheet.append(dict(benchmark=i, variant=v["file"], properties="; ".join("%s: %s" % (p["id"], pexpr(p)) for p in props),
                              expected_verdict="SAFE" if v["expected_verdict"] else "VIOLATION",
                              reviewer_verdict="", reviewer_agrees_with_semantics="", comment=""))

def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
write(os.path.join(OUT, "sample.csv"), rows)
write(os.path.join(OUT, "review_sheet.csv"), sheet)

with open(os.path.join(OUT, "review_pack.md"), "w", encoding="utf-8") as f:
    f.write("# Review pack\n\nEach entry gives the program, the property, the expected verdict, and the assumptions under which the verdict holds. See README.md for the questions.\n")
    for name, ids in strata:
        f.write("\n## Stratum: %s\n" % name)
        for i in sorted(ids):
            d = B[i]; s = d["semantics"]
            props = yaml.safe_load(open(os.path.join(d["_dir"], d["properties_file"])))["properties"]
            f.write("\n### %s (%s, %s)\n\n" % (i, d["language"], d["validation_status"]))
            f.write("Semantics: " + "; ".join("%s = %s" % (k, v) for k, v in s.items()) + "\n\n")
            f.write("Properties:\n" + "".join("- %s (%s): `%s`. %s\n" % (p["id"], p["kind"], pexpr(p), p.get("justification", "")) for p in props))
            for v in d["variants"]:
                path = os.path.join(d["_dir"], v["file"]); text = open(path, encoding="utf-8").read()
                f.write("\nVariant `%s`, expected verdict %s (%s):\n\n" % (v["file"], "SAFE" if v["expected_verdict"] else "VIOLATION", v["verdict_basis"]["method"]))
                if text.count("\n") <= 60:
                    f.write("```\n%s\n```\n" % text.rstrip())
                else:
                    f.write("Program has %d lines; open `%s`.\n" % (text.count("\n"), path))
print("benchmarks:", sum(len(x) for _, x in strata), "variants:", len(rows))
for n, x in strata: print(" ", n, len(x))
