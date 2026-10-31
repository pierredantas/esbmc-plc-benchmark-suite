"""Build the review sheet for the 12 standard-anchored programs (R2.4).

Reads mutation_results.json (from mutation_check.py) and the benchmark descriptors of the suite, and writes
review_sheet.csv and review_sheet.md next to this file. The two reviewer columns are left empty.

    make_review_sheet.py SUITE_BENCHMARKS_DIR
"""
import csv
import glob
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
suite = sys.argv[1]
mut = json.load(open(HERE / "mutation_results.json"))

header = ["benchmark", "language", "clause_cited", "safety_intent", "property", "justification", "discriminator",
          "mutants", "killed_by_property", "killed_only_by_discriminator", "surviving", "surviving_mutants",
          "reviewer_faithful (yes/no/partly)", "reviewer_comment"]
rows = []
md = ["# Review sheet: 12 programs anchored to a standard\n",
      "For each program: the clause it cites, our property, and the mutants that no property kills. "
      "A surviving mutant may be harmless, or may be a behavior that the clause requires and that no property checks.\n"]

for bid, m in mut.items():
    d = pathlib.Path(glob.glob(f"{suite}/*/{bid}")[0])
    b = yaml.safe_load(open(d / "benchmark.yml"))
    props = yaml.safe_load(open(d / "props.yaml"))["properties"]
    discs = {p.name: yaml.safe_load(open(p))["properties"] for p in sorted(d.glob("*.props.yaml"))}
    prop_txt = "; ".join(f"{q['id']}: {q.get('expression') or q.get('variables')}" for q in props)
    just = " / ".join(q.get("justification", "") for q in props)
    disc_txt = " | ".join(
        f"{n}: " + ", ".join(f"{q['id']} {q.get('expression')}" for q in ps) + f" (base {m['base_disc'].get(n)})"
        for n, ps in discs.items())
    survivors = [s["mutant"] for s in m["survivors"]]
    rows.append([bid, b["language"], b["source"]["reference"], b.get("safety_intent", ""), prop_txt, just, disc_txt,
                 m["mutants"], m["killed_main"], m["killed_disc_only"], len(survivors), "; ".join(survivors), "", ""])
    md.append(f"## {bid} ({b['language']})\n")
    md.append(f"- **Clause cited:** {b['source']['reference']}")
    md.append(f"- **Safety intent:** {b.get('safety_intent', '')}")
    md.append(f"- **Property:** {prop_txt}")
    if disc_txt:
        md.append(f"- **Discriminator:** {disc_txt}")
    md.append(f"- **Mutants:** {m['mutants']}; killed by the property {m['killed_main']}; "
              f"killed only by the discriminator {m['killed_disc_only']}; surviving {len(survivors)}")
    md += [f"  - {s}" for s in survivors]
    md.append("- **Reviewer: does the program implement the clause? (yes / no / partly):** ____")
    md.append("- **Comment:** ____\n")

with open(HERE / "review_sheet.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)
(HERE / "review_sheet.md").write_text("\n".join(md))
print(len(rows), "programs")
