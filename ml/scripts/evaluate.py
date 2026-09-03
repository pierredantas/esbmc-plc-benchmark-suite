#!/usr/bin/env python3
"""Evaluate base vs fine-tuned model on held-out props.yaml generation.

For each test example, generates a completion from the prompt and scores it:
  - yaml_valid: parses as YAML
  - schema_valid: validates against schema/properties.schema.json
  - kind_recall: fraction of expected property `kind`s (multiset) present in output
  - id_format_ok: every emitted property id matches ^P[0-9]+$
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schema" / "properties.schema.json"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def extract_yaml(text: str) -> str:
    m = re.search(r"```(?:yaml)?\s*\n(.*?)```", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def score_output(raw_output: str, expected_text: str, schema) -> dict:
    result = {
        "yaml_valid": False,
        "schema_valid": False,
        "id_format_ok": False,
        "kind_recall": 0.0,
        "kind_precision": 0.0,
    }
    candidate = extract_yaml(raw_output)
    try:
        obj = yaml.safe_load(candidate)
    except yaml.YAMLError:
        return result
    if not isinstance(obj, dict):
        return result
    result["yaml_valid"] = True

    try:
        validate(instance=obj, schema=schema)
        result["schema_valid"] = True
    except ValidationError:
        pass

    props = obj.get("properties", []) if isinstance(obj.get("properties"), list) else []
    ids = [p.get("id", "") for p in props if isinstance(p, dict)]
    result["id_format_ok"] = bool(ids) and all(re.match(r"^P[0-9]+$", i) for i in ids)

    got_kinds = Counter(p.get("kind") for p in props if isinstance(p, dict))
    expected_obj = yaml.safe_load(expected_text)
    expected_kinds = Counter(p.get("kind") for p in expected_obj.get("properties", []))

    overlap = sum((got_kinds & expected_kinds).values())
    result["kind_recall"] = overlap / max(1, sum(expected_kinds.values()))
    result["kind_precision"] = overlap / max(1, sum(got_kinds.values())) if got_kinds else 0.0
    return result


def run_eval(model_path, adapter_path, test_records, schema, max_tokens=512):
    if adapter_path:
        model, tokenizer = load(model_path, adapter_path=adapter_path)
    else:
        model, tokenizer = load(model_path)

    # Qwen2.5's chat template ends turns with <|im_end|>, but the tokenizer's
    # eos_token_ids only has <|endoftext|>; without this the model runs on
    # past the turn boundary and generate() never stops at the right spot.
    im_end_ids = tokenizer.encode("<|im_end|>", add_special_tokens=False)
    tokenizer.eos_token_ids = set(tokenizer.eos_token_ids) | set(im_end_ids)

    sampler = make_sampler(temp=0.0)
    per_example = []
    for rec in test_records:
        messages = rec["messages"][:2]  # system + user, model produces assistant turn
        prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
        output = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, sampler=sampler, verbose=False)
        expected = rec["messages"][2]["content"]
        scores = score_output(output, expected, schema)
        scores["task_id"] = rec.get("task_id", "?")
        per_example.append(scores)

    del model
    return per_example


def aggregate(per_example):
    n = len(per_example)
    if n == 0:
        return {}
    keys = ["yaml_valid", "schema_valid", "id_format_ok", "kind_recall", "kind_precision"]
    return {k: sum(e[k] for e in per_example) / n for k in keys}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit")
    ap.add_argument("--adapter-path", default=None, help="omit to eval the base model")
    ap.add_argument("--test-file", default=str(REPO_ROOT / "ml" / "data" / "test.jsonl"))
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    schema = load_schema()
    test_records = []
    with open(args.test_file) as f:
        for line in f:
            rec = json.loads(line)
            test_records.append(rec)

    per_example = run_eval(args.model, args.adapter_path, test_records, schema, args.max_tokens)
    agg = aggregate(per_example)

    label = "fine-tuned" if args.adapter_path else "base"
    print(f"\n=== {label} model — {len(per_example)} test examples ===")
    for k, v in agg.items():
        print(f"  {k}: {v:.3f}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump({"label": label, "aggregate": agg, "per_example": per_example}, f, indent=2)


if __name__ == "__main__":
    main()
