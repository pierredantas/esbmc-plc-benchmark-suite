#!/usr/bin/env python3
"""Re-record the LD-route runs that record_all.py does not name.

record_all.py derives an output name from the benchmark and its variant. A page that
wants "the seal-in latch" or "the weakened reactor property" refers to a record by
meaning instead, and those records are driven from runner/custom_records.yml. They are
easy to forget: a route-wide regeneration that skips them leaves a handful of records
describing an older toolchain than everything around them.

    record_custom.py --tool v8.4=PATH --tool master=PATH [--timeout 30]
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORDS = ROOT / "results" / "records"
MANIFEST = ROOT / "runner" / "custom_records.yml"


def one(entry, tools, timeout):
    """Record one entry, copying to .ld first when ESBMC needs the extension."""
    program = ROOT / entry["program"]
    copy = program.with_suffix(".ld")
    made = copy != program and not copy.exists()
    if made:
        shutil.copyfile(program, copy)
    args = [sys.executable, str(ROOT / "runner" / "record.py"), str(copy),
            str(ROOT / entry["props"]), entry["expected"],
            "--timeout", str(timeout), "--source", str(program)]
    if entry.get("mode") == "watchdog":
        args.append("--watchdog-only")
    elif entry.get("mode"):
        args += ["--mode", entry["mode"]]
    for tool in tools:
        args += ["--tool", tool]
    args += ["-o", str(RECORDS / f'{entry["name"]}.json')]
    try:
        out = subprocess.run(args, capture_output=True, text=True, check=False)
    finally:
        if made:
            copy.unlink(missing_ok=True)
    return out.stdout.strip() or out.stderr.strip()[:160]


def main():
    """Refresh every record named in the manifest."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", action="append", required=True, metavar="LABEL=PATH")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()
    entries = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))["records"]
    for entry in entries:
        print(one(entry, args.tool, args.timeout))
    print(f"\n{len(entries)} custom record(s) refreshed in {RECORDS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
