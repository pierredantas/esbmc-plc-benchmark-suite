#!/usr/bin/env python3
"""Record a run for every benchmark variant ESBMC can read.

The catalog is only as useful as the evidence attached to it, and a task page that
says nothing about what a tool did with the program is a page nobody needs. This
walks the suite and drives record.py once per runnable variant.

    record_all.py --tool v8.4=PATH --tool master=PATH [--timeout 30]
    record_all.py --route via-c --tool master=PATH

The ladder route runs PLCopen XML only: ESBMC picks its LD front end from the file
extension and XML-parses whatever it finds, so the textual .ld DSL and the .st
programs are skipped rather than reported as failures. A termination property is not
accepted by --ld-props at all; those variants go through the scan watchdog instead.

The via-c route reaches ST, IL, FBD and SFC as well, by way of Beremiz and MatIEC. Its
harness runs a fixed number of scans, so a bomb on a long fuse is invisible at a small
count; a variant expected to fail that comes back SAFE is retried once, deeper, before
the answer is believed.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORDS = ROOT / "results" / "records"
DEEP = 64  # scans to retry at when a fused bomb hides below the default depth


def is_termination(props_path):
    """Whether a property file asks about termination rather than safety."""
    props = yaml.safe_load(props_path.read_text(encoding="utf-8"))
    return any(p.get("kind") == "termination" for p in props.get("properties", []))


def variants(route):
    """Every (benchmark, variant) pair this route can attempt."""
    for meta_path in sorted((ROOT / "benchmarks").glob("*/*/benchmark.yml")):
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        folder = meta_path.parent
        props = (folder / meta["properties_file"]).resolve()
        for var in meta.get("variants", []):
            program = folder / var["file"]
            runnable = ((".xml",) if route == "ld" else (".xml", ".st", ".il"))
            if program.suffix in runnable and props.exists():
                yield {"name": f'{meta["id"]}__{program.stem}', "program": program,
                       "props": props, "expected": var["expected_verdict"]}


def record_via_c(task, tools, timeout, scans):
    """One via-c record. A long fuse needs a deep harness, so a miss is retried."""
    args = [sys.executable, str(ROOT / "runner" / "record_via_c.py"), str(task["program"]),
            str(task["props"]), "true" if task["expected"] else "false",
            "--timeout", str(timeout), "--scans", str(scans)]
    for tool in tools:
        args += ["--tool", tool]
    out_path = RECORDS / f'{task["name"]}__viac.json'
    result = subprocess.run(args + ["-o", str(out_path)], capture_output=True,
                            text=True, check=False)
    if result.returncode != 0:
        reason = result.stderr.strip().splitlines()[-1] if result.stderr else "failed"
        return f'SKIP {task["name"]}: {reason[:96]}'
    if not task["expected"] and out_path.exists():
        verdicts = json.loads(out_path.read_text(encoding="utf-8"))["runs"]
        if all(run["verdict"] == "SAFE" for run in verdicts.values()) and scans < DEEP:
            return record_via_c(task, tools, timeout * 3, DEEP)
    return result.stdout.strip()


def record(task, tools, timeout):
    """One record, written against a .ld copy so ESBMC selects the LD front end."""
    program, props = task["program"], task["props"]
    copy = program.with_suffix(".ld")
    shutil.copyfile(program, copy)
    args = [sys.executable, str(ROOT / "runner" / "record.py"), str(copy), str(props),
            "true" if task["expected"] else "false", "--timeout", str(timeout),
            "--source", str(program)]
    if is_termination(props):
        args.append("--watchdog-only")
    for tool in tools:
        args += ["--tool", tool]
    args += ["-o", str(RECORDS / f'{task["name"]}.json')]
    try:
        out = subprocess.run(args, capture_output=True, text=True, check=False)
    finally:
        copy.unlink(missing_ok=True)
    return out.stdout.strip() or out.stderr.strip()[:120]


def main():
    """Record everything, reporting one line per variant."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", action="append", required=True, metavar="LABEL=PATH")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--route", choices=["ld", "via-c"], default="ld")
    ap.add_argument("--scans", type=int, default=8)
    args = ap.parse_args()

    RECORDS.mkdir(parents=True, exist_ok=True)
    done = 0
    for task in variants(args.route):
        if args.route == "via-c":
            print(record_via_c(task, args.tool, args.timeout, args.scans))
        else:
            print(record(task, args.tool, args.timeout))
        done += 1
    print(f"\n{done} variant(s) recorded into {RECORDS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
