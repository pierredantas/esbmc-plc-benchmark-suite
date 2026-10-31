"""Merge and validate the reviewer's per-batch replies into answers.csv (R1.1).

    merge_answers.py REPLIES_DIR ANSWERS.csv

REPLIES_DIR holds one text file per batch, each a copy of the reviewer's reply (code fences, prose, and a repeated
header line are tolerated). A row is any line that starts with a benchmark id of the suite. The script checks that
every row has the ten columns and allowed values, lists duplicates and missing benchmarks, and writes ANSWERS.csv in
the order of answers_template.csv. Exit status 1 when anything is wrong, so fix the named rows and rerun.
"""
import csv
import io
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
replies_dir, out_path = pathlib.Path(sys.argv[1]), sys.argv[2]

template = list(csv.DictReader(open(HERE / "answers_template.csv")))
header = list(template[0])
ids = [r["benchmark"] for r in template]
lang = {r["benchmark"]: r["language"] for r in template}

ALLOWED = {
    "scan_order": {"rung", "statement", "tool-defined"},
    "retained_state": {"yes", "no"},
    "timers_or_counters": {"yes", "no"},
    "overflow_possible": {"yes", "no"},
    "setreset_coils": {"yes", "no"},
    "verdict_scope": {"holds-under-stated-order", "semantics-dependent"},
    "confidence": {"high", "medium", "low"},
}

found, problems = {}, []
for f in sorted(replies_dir.glob("*")):
    if not f.is_file():
        continue
    for line in f.read_text(errors="replace").splitlines():
        line = line.strip().strip("`")
        first = line.split(",", 1)[0].strip().strip('"')
        if first not in lang:
            continue
        try:
            row = next(csv.reader(io.StringIO(line), skipinitialspace=True))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{f.name}: {first}: unreadable row ({e})")
            continue
        if len(row) > len(header):  # a comma inside the reasoning: keep the tail as one field
            row = row[:len(header) - 1] + [",".join(row[len(header) - 1:])]
        if len(row) != len(header):
            problems.append(f"{f.name}: {first}: {len(row)} columns, expected {len(header)}")
            continue
        rec = dict(zip(header, [x.strip() for x in row]))
        for k, allowed in ALLOWED.items():
            rec[k] = rec[k].lower()
            if rec[k] not in allowed:
                problems.append(f"{f.name}: {first}: {k} = {rec[k]!r}, allowed {sorted(allowed)}")
        if first in found:
            problems.append(f"{f.name}: {first}: answered twice (kept the first)")
            continue
        rec["language"] = lang[first]
        found[first] = rec

missing = [i for i in ids if i not in found]
if missing:
    problems.append(f"{len(missing)} benchmarks unanswered: {', '.join(missing[:12])}{' ...' if len(missing) > 12 else ''}")

with open(out_path, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=header)
    w.writeheader()
    for i in ids:
        w.writerow(found.get(i, {**{k: "" for k in header}, "benchmark": i, "language": lang[i]}))
print(f"{len(found)} of {len(ids)} benchmarks answered; {len(problems)} problems")
for p in problems:
    print(" -", p)
sys.exit(1 if problems else 0)
