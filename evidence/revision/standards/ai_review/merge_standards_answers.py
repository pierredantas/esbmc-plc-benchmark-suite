"""Merge and validate the reviewer's replies for the 12 standard-anchored programs (R2.4).

    merge_standards_answers.py REPLIES_DIR OUT_PREFIX

REPLIES_DIR holds one text file per batch (a copy of the reply; code fences, prose, a repeated header, and the
separator line are tolerated). A row starting with a benchmark id is a program row when its second field is a
language and a mutant row when it is an id such as S3. Writes OUT_PREFIX_programs.csv and OUT_PREFIX_survivors.csv in
the order of the templates, checks values, coverage, and duplicates, prints a summary, and lists the mutants judged
required_by_clause. Exit status 1 when anything is wrong.
"""
import collections
import csv
import io
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
replies, prefix = pathlib.Path(sys.argv[1]), sys.argv[2]

prog_t = list(csv.DictReader(open(HERE / "answers_programs_template.csv")))
surv_t = list(csv.DictReader(open(HERE / "answers_survivors_template.csv")))
prog_h, surv_h = list(prog_t[0]), list(surv_t[0])
ids = {r["benchmark"] for r in prog_t}
want_surv = {(r["benchmark"], r["mutant_id"]): r for r in surv_t}
ALLOWED = {"implements_cited_requirement": {"yes", "partly", "no"}, "confidence": {"high", "medium", "low"},
           "classification": {"required_by_clause", "harmless", "unclear"}}

progs, survs, problems = {}, {}, []
for f in sorted(replies.glob("*")):
    if not f.is_file():
        continue
    for line in f.read_text(errors="replace").splitlines():
        line = line.strip().strip("`")
        first = line.split(",", 1)[0].strip().strip('"')
        if first not in ids:
            continue
        try:
            row = next(csv.reader(io.StringIO(line), skipinitialspace=True))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{f.name}: {first}: unreadable row ({e})")
            continue
        is_mut = len(row) > 1 and re.fullmatch(r"S\d+", row[1].strip() or "") is not None
        header = surv_h if is_mut else prog_h
        if len(row) > len(header):
            row = row[:len(header) - 1] + [",".join(row[len(header) - 1:])]
        if len(row) != len(header):
            problems.append(f"{f.name}: {first}: {len(row)} columns, expected {len(header)}")
            continue
        rec = dict(zip(header, [x.strip() for x in row]))
        for k, allowed in ALLOWED.items():
            if k in rec:
                rec[k] = rec[k].lower()
                if rec[k] not in allowed:
                    problems.append(f"{f.name}: {first}: {k} = {rec[k]!r}, allowed {sorted(allowed)}")
        if is_mut:
            key = (rec["benchmark"], rec["mutant_id"])
            if key not in want_surv:
                problems.append(f"{f.name}: {key}: not a listed mutant")
            elif key in survs:
                problems.append(f"{f.name}: {key}: answered twice (kept the first)")
            else:
                rec["mutant"] = want_surv[key]["mutant"]
                survs[key] = rec
        else:
            if first in progs:
                problems.append(f"{f.name}: {first}: answered twice (kept the first)")
            else:
                progs[first] = rec

missing_p = sorted(ids - set(progs))
missing_s = sorted(k for k in want_surv if k not in survs)
if missing_p:
    problems.append(f"{len(missing_p)} programs unanswered: {', '.join(missing_p)}")
if missing_s:
    problems.append(f"{len(missing_s)} mutants unanswered, first: {missing_s[:6]}")

with open(f"{prefix}_programs.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=prog_h)
    w.writeheader()
    for r in prog_t:
        w.writerow(progs.get(r["benchmark"], r))
with open(f"{prefix}_survivors.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=surv_h)
    w.writeheader()
    for r in surv_t:
        w.writerow(survs.get((r["benchmark"], r["mutant_id"]), r))

print(f"{len(progs)} of {len(ids)} programs and {len(survs)} of {len(want_surv)} mutants answered; {len(problems)} problems")
print("implements the cited requirement:", dict(collections.Counter(p["implements_cited_requirement"] for p in progs.values())))
print("surviving mutants:", dict(collections.Counter(s["classification"] for s in survs.values())))
req = [s for s in survs.values() if s["classification"] == "required_by_clause"]
print(f"{len(req)} mutants judged required by the clause (candidate property gaps):")
for s in req:
    print(f"  {s['benchmark']} {s['mutant_id']}: {s['mutant']} | {s['reasoning'][:110]}")
for p in problems:
    print(" -", p)
sys.exit(1 if problems else 0)
