#!/usr/bin/env python3
"""Validate every benchmark: schema-check benchmark.yml + props.yaml, confirm
referenced program files exist and (for XML) are well-formed. Exit non-zero on any error.

Usage:  python3 runner/validate.py            # validate whole suite
        python3 runner/validate.py <dir>...   # validate specific benchmark dirs
"""
import sys, os, glob, json
import xml.etree.ElementTree as ET

try:
    import yaml
    import jsonschema
except ImportError as e:
    sys.exit(f"missing dependency: {e}. Run: pip3 install pyyaml jsonschema")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH_SCHEMA = json.load(open(os.path.join(ROOT, "schema", "benchmark.schema.json")))
PROP_SCHEMA = json.load(open(os.path.join(ROOT, "schema", "properties.schema.json")))


def validate_benchmark(bench_dir):
    errors = []
    bpath = os.path.join(bench_dir, "benchmark.yml")
    if not os.path.isfile(bpath):
        return [f"{bench_dir}: no benchmark.yml"]
    bench = yaml.safe_load(open(bpath))
    try:
        jsonschema.validate(bench, BENCH_SCHEMA)
    except jsonschema.ValidationError as e:
        errors.append(f"{bpath}: schema: {e.message}")

    # properties file (may be shared/inherited via a relative path)
    props_rel = bench.get("properties_file", "props.yaml")
    props_path = os.path.normpath(os.path.join(bench_dir, props_rel))
    if not os.path.isfile(props_path):
        errors.append(f"{bpath}: properties_file not found: {props_path}")
    else:
        props = yaml.safe_load(open(props_path))
        try:
            jsonschema.validate(props, PROP_SCHEMA)
        except jsonschema.ValidationError as e:
            errors.append(f"{props_path}: schema: {e.message}")
        prop_ids = {p["id"] for p in props.get("properties", [])}
        # every violated_properties id must exist
        for v in bench.get("variants", []):
            for pid in v.get("violated_properties", []):
                if pid not in prop_ids:
                    errors.append(f"{bpath}: variant {v['file']} cites unknown property {pid}")

    # program variant files exist and XML is well-formed
    for v in bench.get("variants", []):
        f = os.path.join(bench_dir, v["file"])
        if not os.path.isfile(f):
            errors.append(f"{bpath}: variant file missing: {v['file']}")
        elif f.endswith(".xml"):
            try:
                ET.parse(f)
            except ET.ParseError as e:
                errors.append(f"{f}: malformed XML: {e}")
    return errors


def main():
    dirs = sys.argv[1:] or [os.path.dirname(p) for p in
                            glob.glob(os.path.join(ROOT, "benchmarks", "**", "benchmark.yml"), recursive=True)]
    all_errors, n = [], 0
    for d in sorted(dirs):
        n += 1
        errs = validate_benchmark(d)
        rel = os.path.relpath(d, ROOT)
        print(f"{'OK  ' if not errs else 'FAIL'} {rel}")
        all_errors += errs
    print(f"\n{n} benchmark(s) checked, {len(all_errors)} error(s).")
    for e in all_errors:
        print("  -", e)
    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
