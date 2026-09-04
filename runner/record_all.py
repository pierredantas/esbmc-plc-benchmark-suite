#!/usr/bin/env python3
"""Record a run for every benchmark variant ESBMC can read.

The catalog is only as useful as the evidence attached to it, and a task page that
says nothing about what a tool did with the program is a page nobody needs. This
walks the suite and drives record.py once per runnable variant.

    record_all.py --tool v8.4=PATH --tool master=PATH [--timeout 30]
    record_all.py --route via-c --tool master=PATH

The ladder route runs PLCopen XML, plus the plain-text LD DSL that
tools/ld_text_to_xml.py can convert to XML first: ESBMC picks its LD front end from
the file extension and XML-parses whatever it finds, so a source that is genuinely
neither (a .st program, or a plain-text .ld rung using a stateful block the converter
does not handle) is skipped rather than reported as a failure. A termination property
is not accepted by --ld-props at all; those variants go through the scan watchdog
instead.

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

sys.path.insert(0, str(ROOT / "tools"))
from ld_text_to_xml import ParseError, translate  # noqa: E402


def is_termination(props_path):
    """Whether a property file asks about termination rather than safety."""
    props = yaml.safe_load(props_path.read_text(encoding="utf-8"))
    return any(p.get("kind") == "termination" for p in props.get("properties", []))


def is_text_ld(path):
    """A .ld file is the plain-text OTE/XIC/XIO DSL, not PLCopen XML with a forced
    extension, when its content does not start with an XML declaration."""
    return not path.read_text(encoding="utf-8").lstrip().startswith("<?xml")


def variants(route):
    """Every (benchmark, variant) pair this route can attempt.

    Every plain-text .ld file is included here regardless of whether it will
    actually convert; a stateful block (TON, CTU, ...) that tools/ld_text_to_xml.py
    cannot handle surfaces as a printed SKIP line from record(), not a silent
    absence from the catalog.
    """
    for meta_path in sorted((ROOT / "benchmarks").glob("*/*/benchmark.yml")):
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        folder = meta_path.parent
        props = (folder / meta["properties_file"]).resolve()
        for var in meta.get("variants", []):
            program = folder / var["file"]
            if not props.exists():
                continue
            if program.suffix == ".xml" or (route == "ld" and program.suffix == ".ld"
                                             and is_text_ld(program)):
                yield {"name": f'{meta["id"]}__{program.stem}', "program": program,
                       "props": props, "expected": var["expected_verdict"],
                       "text_ld": program.suffix == ".ld"}
            elif route == "via-c" and program.suffix in (".xml", ".st", ".il"):
                yield {"name": f'{meta["id"]}__{program.stem}', "program": program,
                       "props": props, "expected": var["expected_verdict"],
                       "text_ld": False}


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
    """One record, written against a .ld copy so ESBMC selects the LD front end.

    A plain-text .ld source is already `.ld`-suffixed, so `with_suffix(".ld")` would
    name the source itself; it is converted to PLCopen XML into a sibling temp file
    instead, and record.py is told so it prints an honest replay command rather than
    a `cp` of a file ESBMC cannot parse.
    """
    program, props = task["program"], task["props"]
    converted = task["text_ld"]
    if converted:
        copy = program.with_name(program.stem + "__xml.ld")
        try:
            xml = translate(program.stem, program.read_text(encoding="utf-8"))
        except ParseError as e:
            return f'SKIP {task["name"]}: {e}'
        copy.write_text(xml, encoding="utf-8")
    else:
        copy = program.with_suffix(".ld")
        shutil.copyfile(program, copy)
    args = [sys.executable, str(ROOT / "runner" / "record.py"), str(copy), str(props),
            "true" if task["expected"] else "false", "--timeout", str(timeout),
            "--source", str(program)]
    if converted:
        args.append("--converted-from-text-ld")
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
