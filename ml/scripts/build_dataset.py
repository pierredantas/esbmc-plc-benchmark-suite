#!/usr/bin/env python3
"""Build (program, props.yaml) fine-tuning pairs from benchmarks/.

Walks benchmarks/<domain>/<id>/, reads benchmark.yml for the variant file
list and props.yaml for the target, and emits one JSONL record per variant
in MLX chat-format (messages: system/user/assistant).

Split is by task id (not by variant), domain-stratified, so that clean/bomb
variants of the same task never straddle train and test.
"""
import argparse
import json
import random
import sys
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
SCHEMA_PATH = REPO_ROOT / "schema" / "properties.schema.json"

sys.path.insert(0, str(REPO_ROOT))
from runner.ld_to_st import translate as ld_to_st_translate  # noqa: E402

SYSTEM_PROMPT = (
    "You are a formal-verification assistant for IEC 61131-3 PLC programs. "
    "Given the source of one program variant, emit its safety properties as "
    "a props.yaml document: format_version, then a properties list where each "
    "item has id (P1, P2, ...), kind (invariant | mutual_exclusion | absence | "
    "reachability | assertion | termination), an expression or variables list "
    "as the kind requires, and a one-sentence justification grounded in the "
    "program's physical/safety intent. Output only the YAML, no commentary."
)


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def build_user_prompt(language: str, domain: str, source: str) -> str:
    return (
        f"Domain: {domain}\n"
        f"Language: {language}\n"
        f"Program:\n```\n{source}\n```\n\n"
        "Emit the props.yaml safety properties for this program."
    )


def collect_records(schema, augment_st=False):
    records = []
    skipped = []
    for bench_yml in sorted(BENCHMARKS_DIR.glob("*/*/benchmark.yml")):
        task_dir = bench_yml.parent
        domain = task_dir.parent.name
        task_id = task_dir.name

        with open(bench_yml) as f:
            meta = yaml.safe_load(f)

        props_file = task_dir / meta.get("properties_file", "props.yaml")
        if not props_file.exists():
            skipped.append((task_id, "no props.yaml"))
            continue

        with open(props_file) as f:
            props_text = f.read()
        try:
            props_obj = yaml.safe_load(props_text)
            validate(instance=props_obj, schema=schema)
        except (yaml.YAMLError, ValidationError) as e:
            skipped.append((task_id, f"props.yaml invalid: {e}"))
            continue

        language = meta.get("language", "unknown")
        variants = meta.get("variants", [])
        if not variants:
            skipped.append((task_id, "no variants"))
            continue

        for variant in variants:
            src_file = task_dir / variant["file"]
            if not src_file.exists():
                skipped.append((f"{task_id}/{variant['file']}", "source missing"))
                continue
            source = src_file.read_text(errors="replace")

            records.append({
                "task_id": task_id,
                "domain": domain,
                "variant_file": variant["file"],
                "language": language,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(language, domain, source)},
                    {"role": "assistant", "content": props_text.strip()},
                ],
            })

            # Same ground truth, different concrete syntax: runner/ld_to_st.py
            # reconstructs ST from a PLCopen LD body, so an XML-bodied variant
            # (LD-graphical/FBD/SFC) yields a second, free training pair.
            if augment_st and src_file.suffix == ".xml":
                try:
                    st_source = ld_to_st_translate(str(src_file))
                except Exception as e:
                    st_source = ""
                    skipped.append((f"{task_id}/{variant['file']}", f"ld_to_st failed: {e}"))
                if st_source.strip():
                    records.append({
                        "task_id": task_id,
                        "domain": domain,
                        "variant_file": variant["file"] + " (ST-translated)",
                        "language": "ST",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": build_user_prompt("ST", domain, st_source)},
                            {"role": "assistant", "content": props_text.strip()},
                        ],
                    })

    return records, skipped


def stratified_split(records, val_frac, test_frac, seed, force_train=()):
    """force_train pins specific task ids into the training split regardless
    of the random draw — for a newly authored task whose pattern (e.g. a kind
    or variable-count combination) doesn't exist anywhere else in the corpus,
    landing it in valid/test by chance means the model never sees the pattern
    it was added to teach."""
    by_task = {}
    for r in records:
        by_task.setdefault((r["domain"], r["task_id"]), []).append(r)

    tasks_by_domain = {}
    for (domain, task_id) in by_task:
        tasks_by_domain.setdefault(domain, []).append(task_id)

    rng = random.Random(seed)
    train_ids, val_ids, test_ids = set(), set(), set()
    for domain, task_ids in tasks_by_domain.items():
        task_ids = sorted(set(task_ids))
        rng.shuffle(task_ids)
        eligible = [t for t in task_ids if t not in force_train]
        n = len(eligible)
        n_test = max(1, round(n * test_frac)) if n >= 3 else (1 if n > 1 else 0)
        n_val = max(1, round(n * val_frac)) if n >= 3 else 0
        test_ids.update(eligible[:n_test])
        val_ids.update(eligible[n_test:n_test + n_val])
        train_ids.update(eligible[n_test + n_val:])
        train_ids.update(t for t in task_ids if t in force_train)

    train, val, test = [], [], []
    for (domain, task_id), recs in by_task.items():
        if task_id in force_train:
            train.extend(recs)
        elif task_id in test_ids:
            test.extend(recs)
        elif task_id in val_ids:
            val.extend(recs)
        else:
            train.extend(recs)
    return train, val, test


def write_jsonl(path: Path, records):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps({"messages": r["messages"]}) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(REPO_ROOT / "ml" / "data"))
    ap.add_argument("--val-frac", type=float, default=0.15)
    ap.add_argument("--test-frac", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--augment-st", action="store_true",
                     help="add an ld_to_st.py ST-translation record for every XML-bodied variant (same ground truth, new syntax)")
    ap.add_argument("--force-train", default="",
                     help="comma-separated task ids to pin into the training split regardless of the random draw "
                          "(e.g. a newly authored task covering a pattern absent elsewhere in the corpus)")
    args = ap.parse_args()

    schema = load_schema()
    records, skipped = collect_records(schema, augment_st=args.augment_st)

    if skipped:
        print(f"Skipped {len(skipped)} entries:", file=sys.stderr)
        for name, reason in skipped:
            print(f"  {name}: {reason}", file=sys.stderr)

    force_train = {t.strip() for t in args.force_train.split(",") if t.strip()}
    train, val, test = stratified_split(records, args.val_frac, args.test_frac, args.seed, force_train)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_dir / "train.jsonl", train)
    write_jsonl(out_dir / "valid.jsonl", val)
    write_jsonl(out_dir / "test.jsonl", test)

    with open(out_dir / "manifest.json", "w") as f:
        json.dump({
            "total_records": len(records),
            "train": len(train), "valid": len(val), "test": len(test),
            "skipped": len(skipped),
            "domains": sorted({r["domain"] for r in records}),
            "languages": sorted({r["language"] for r in records}),
        }, f, indent=2)

    print(f"records: {len(records)}  train: {len(train)}  valid: {len(val)}  test: {len(test)}  skipped: {len(skipped)}")


if __name__ == "__main__":
    main()
