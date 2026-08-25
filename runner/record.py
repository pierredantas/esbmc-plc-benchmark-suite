#!/usr/bin/env python3
"""Capture a reproducible run record for one (program, property) pair.

One record carries what the ingestion gate needs and what the educational portal
renders, because they are the same data: the command, what ESBMC actually encoded,
and the verdict it reached.

  record.py <program.ld> <props.yaml> <expected:true|false> [-o out.json]

Exit status is 1 when the ingestion gate rejects the record, so this doubles as a
CI check.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import yaml

ESBMC = os.environ.get("ESBMC", os.path.expanduser(
    "~/esbmc-toolchain/src/esbmc-src/build/src/esbmc/esbmc"))
WATCHDOG = ["--ld-scan-watchdog", "--ld-scan-budget", "8"]
IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
KEYWORDS = {"true", "false", "TRUE", "FALSE", "AND", "OR", "NOT"}


def run_esbmc(args):
    """Invoke ESBMC and return its combined output."""
    out = subprocess.run([ESBMC, *args], capture_output=True, text=True, check=False)
    return (out.stdout or "") + (out.stderr or "")


def tool_info():
    """Version and platform of the binary under ESBMC."""
    raw = run_esbmc(["--version"]).strip()
    m = re.search(r"ESBMC version (\S+) .*?(\S+ \S+)$", raw)
    return {"name": "esbmc-plc", "raw": raw,
            "version": m.group(1) if m else None,
            "platform": m.group(2) if m else None}


def property_variables(props):
    """Variables a verdict must actually depend on."""
    out = set()
    for prop in props.get("properties", []):
        out.update(prop.get("variables", []))
        expr = prop.get("expression")
        if expr:
            out.update(t for t in IDENT.findall(expr) if t not in KEYWORDS)
    return sorted(out)


def encoded_assignments(program):
    """What the front-end produced. An empty list means the body was dropped."""
    txt = run_esbmc([program, "--goto-functions-only"])
    return [m.strip().rstrip(";")[len("ASSIGN "):]
            for m in re.findall(r"^\s+ASSIGN .*$", txt, re.M)]


def check_gate(assignments, pvars):
    """Ingestion gate.

    The front-end emits exactly one zero-initialiser per output variable, so a
    variable the BODY drives is assigned at least twice. Merely counting any
    assignment is not enough: a silently dropped body still leaves the
    initialisers behind, and every safety property then holds vacuously
    (probe/FINDINGS.md, Finding 1).
    """
    counts = {}
    for stmt in assignments:
        if "=" in stmt:
            name = stmt.split("=", 1)[0].strip()
            counts[name] = counts.get(name, 0) + 1
    missing = [v for v in pvars if counts.get(v, 0) < 2]
    return counts, missing, ("pass" if assignments and not missing else "fail")


def verify(program, props_path, expected, timeout):
    """Run the verification and classify the outcome."""
    mode = ["--k-induction"] if expected else ["--incremental-bmc", "--unwind", "20"]
    args = [program, "--ld-props", props_path, *mode, *WATCHDOG, "--timeout", f"{timeout}s"]
    start = time.time()
    txt = run_esbmc(args)
    if re.search(r"verification successful", txt, re.I):
        verdict = "true"
    elif re.search(r"verification failed", txt, re.I):
        verdict = "false"
    elif re.search(r"PARSING ERROR|CONVERSION ERROR", txt):
        verdict = "error"
    else:
        verdict = "unknown"
    trace = None
    if verdict == "false":
        m = re.search(r"^State 1.*?(?=\n+VERIFICATION)", txt, re.S | re.M)
        trace = m.group(0).strip() if m else None
    return {"command": " ".join([ESBMC, *args]), "verdict": verdict,
            "cpu_time_s": round(time.time() - start, 3), "counterexample": trace}


def classify(verdict, expected):
    """Map a verdict against its expectation."""
    if verdict in ("error", "unknown"):
        return verdict
    return "correct" if verdict == expected else "wrong"


def main():
    """Capture one record; return 1 if the ingestion gate rejects it."""
    ap = argparse.ArgumentParser()
    ap.add_argument("program")
    ap.add_argument("props")
    ap.add_argument("expected", choices=["true", "false"])
    ap.add_argument("-o", "--out")
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    with open(args.props, encoding="utf-8") as fh:
        props = yaml.safe_load(fh)

    pvars = property_variables(props)
    assignments = encoded_assignments(args.program)
    counts, missing, gate = check_gate(assignments, pvars)
    result = verify(args.program, args.props, args.expected == "true", args.timeout)

    record = {
        "schema_version": "0.1",
        "program": os.path.relpath(args.program),
        "properties_file": os.path.relpath(args.props),
        "properties": props.get("properties", []),
        "tool": tool_info(),
        "expected_verdict": args.expected,
        "status": classify(result["verdict"], args.expected),
        "encoding": {
            "assignments": assignments,
            "property_variables": pvars,
            "assignment_counts": counts,
            "not_driven_by_body": missing,
            "gate": gate,
        },
        **result,
    }

    text = json.dumps(record, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"{gate.upper():4}  {record['status']:8}  "
              f"{os.path.relpath(args.program)}  -> {args.out}")
    else:
        print(text)
    return 0 if gate == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
