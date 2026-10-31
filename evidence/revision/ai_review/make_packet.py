"""Build the blind review packet for the semantics record (R1.1).

For each of the 117 core benchmarks the packet holds the raw text of its first variant, its language, and its
properties, and nothing from our semantics record, descriptor tags, or verdicts. A reviewer fills in
answers_template.csv from the definitions in PROMPT.md; compare_ai_review.py then diffs the answers against
semantics.yml.

    make_packet.py SUITE_BENCHMARKS_DIR
"""
import csv
import glob
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
suite = sys.argv[1]
BATCH = 8

rows = {}
for v in csv.DictReader(open(HERE.parent / "variants_302.csv")):
    if v["core_suite"] == "yes":
        rows.setdefault(v["id"], v)

out_dir = HERE / "programs"
out_dir.mkdir(exist_ok=True)
for old in out_dir.glob("batch_*.md"):
    old.unlink()

ids = sorted(rows)
fence = {"ST": "iecst", "IL": "text", "LD-textual": "text", "LD-graphical": "xml", "FBD": "xml", "SFC": "xml"}
for n in range(0, len(ids), BATCH):
    chunk = ids[n:n + BATCH]
    parts = [f"# Batch {n // BATCH + 1}: benchmarks {', '.join(chunk)}\n"]
    for bid in chunk:
        v = rows[bid]
        d = pathlib.Path(glob.glob(f"{suite}/*/{bid}")[0])
        pf = yaml.safe_load(open(d / "benchmark.yml")).get("properties_file", "props.yaml")
        props = yaml.safe_load(open(d / pf))["properties"]
        prop_txt = "\n".join(f"- {p['id']} ({p['kind']}): {p.get('expression') or p.get('variables')}" for p in props)
        src = (d / v["file"]).read_text(errors="replace")
        parts.append(f"## {bid}\n\n- Language: {v['lang']}\n- File: {v['file']}\n- Properties:\n{prop_txt}\n\n"
                     f"```{fence.get(v['lang'], 'text')}\n{src.rstrip()}\n```\n")
    (out_dir / f"batch_{n // BATCH + 1:02d}.md").write_text("\n".join(parts))

header = ["benchmark", "language", "scan_order", "retained_state", "timers_or_counters", "overflow_possible",
          "setreset_coils", "verdict_scope", "confidence", "reasoning"]
with open(HERE / "answers_template.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    for bid in ids:
        w.writerow([bid, rows[bid]["lang"]] + [""] * (len(header) - 2))
print(len(ids), "benchmarks in", len(list(out_dir.glob("batch_*.md"))), "batches")
