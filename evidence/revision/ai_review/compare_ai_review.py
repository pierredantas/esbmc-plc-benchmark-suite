"""Compare a reviewer's blind answers with the semantics record (R1.1).

    compare_ai_review.py ANSWERS.csv [OUT_PREFIX]

Writes OUT_PREFIX_disagreements.csv (one row per field that differs, with the reviewer's reasoning and the record's
value) and prints agreement per field. The record is ../semantics.yml, restricted to the core benchmarks.
"""
import collections
import csv
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
answers_path = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else "review"

core = {v["id"] for v in csv.DictReader(open(HERE.parent / "variants_302.csv")) if v["core_suite"] == "yes"}
record = {k: v for k, v in yaml.safe_load(open(HERE.parent / "semantics.yml")).items() if k in core}

SCAN = {"sequential rung order within one scan": "rung", "sequential statement order": "statement",
        "tool-defined": "tool-defined"}


def from_record(e):
    sem_dep = e["verdict_scope"] == "semantics-dependent"
    timers = "timer_counter_model" in e
    over = "arithmetic" in e
    return {
        "scan_order": SCAN[e["scan_order"]],
        "retained_state": "yes" if "retained_state" in e else "no",
        "timers_or_counters": "yes" if timers else "no",
        "overflow_possible": "yes" if over else "no",
        "setreset_coils": "yes" if sem_dep and not timers and not over else "no",
        "verdict_scope": "semantics-dependent" if sem_dep else "holds-under-stated-order",
    }


expected = collections.defaultdict(set)
for v in csv.DictReader(open(HERE.parent / "variants_302.csv")):
    if v["core_suite"] == "yes":
        expected[v["id"]].add(v["exp"])

rows = {r["benchmark"]: r for r in csv.DictReader(open(answers_path))}
missing = sorted(core - {b for b, r in rows.items() if r["scan_order"].strip()})
if missing:
    print(f"{len(missing)} benchmarks unanswered, first: {missing[:5]}")

fields = ["scan_order", "retained_state", "timers_or_counters", "overflow_possible", "setreset_coils", "verdict_scope"]
agree = collections.Counter()
seen = collections.Counter()
dis = []
for bid in sorted(core):
    r = rows.get(bid)
    if not r or not r["scan_order"].strip():
        continue
    rec = from_record(record[bid])
    for f in fields:
        seen[f] += 1
        a = r[f].strip().lower()
        if a == rec[f]:
            agree[f] += 1
        else:
            dis.append([bid, r["language"], f, a, rec[f], r["confidence"], r["reasoning"], "/".join(sorted(expected[bid]))])

for f in fields:
    print(f"{f:20s} agree {agree[f]:3d} of {seen[f]:3d}")
print("disagreements:", len(dis), "on", len({d[0] for d in dis}), "benchmarks")
with open(f"{prefix}_disagreements.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["benchmark", "language", "field", "reviewer_answer", "record_value", "reviewer_confidence",
                "reviewer_reasoning", "expected_verdicts", "adjudication (reviewer right / record right / both defensible)", "adjudicator_comment"])
    w.writerows([d + ["", ""] for d in dis])
