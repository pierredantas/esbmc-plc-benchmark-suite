#!/usr/bin/env python3
"""Build a small eval slice for an explicit list of task ids.

Unlike build_dataset.py's stratified train/valid/test split, this pulls exactly
the tasks named, once each (their .ld/.xml variant, not clean+bomb+ST-augmented
copies), so a handful of newly authored benchmarks can be scored as a held-out
probe without waiting for the next full dataset rebuild to route them into
test.jsonl by chance.

    python3 ml/scripts/build_task_slice.py --out ml/data/test_new_ladder_3.jsonl \
        chemical_batch/dual_valve_containment_gm \
        motor_control/vfd_bypass_interlock \
        packaging/capper_torque_stop_ds
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "ml" / "scripts"))
from build_dataset import collect_records, load_schema  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks", nargs="+",
                     help="domain/task_id pairs, e.g. chemical_batch/dual_valve_containment_gm")
    ap.add_argument("--variant", default="clean",
                     help="substring the variant filename must contain (default: clean)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    targets = set()
    for t in args.tasks:
        domain, task_id = t.split("/", 1)
        targets.add((domain, task_id))

    schema = load_schema()
    records, skipped = collect_records(schema, augment_st=False)

    seen, selected = set(), []
    for r in records:
        key = (r["domain"], r["task_id"])
        if key in targets and args.variant in r["variant_file"] and key not in seen:
            selected.append(r)
            seen.add(key)

    missing = targets - seen
    if missing:
        sys.exit(f"no matching '{args.variant}' variant found for: {sorted(missing)}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for r in selected:
            f.write(json.dumps({
                "task_id": r["task_id"],
                "domain": r["domain"],
                "variant_file": r["variant_file"],
                "language": r["language"],
                "messages": r["messages"],
            }) + "\n")

    print(f"wrote {len(selected)} record(s) to {out_path}")
    for r in selected:
        print(f"  {r['domain']}/{r['task_id']}  ({r['variant_file']}, {r['language']})")


if __name__ == "__main__":
    main()
