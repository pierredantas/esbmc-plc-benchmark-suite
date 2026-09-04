#!/usr/bin/env python3
"""Capture a reproducible run record for one (program, property) pair.

A record holds one entry per tool build, so the same ladder can be shown against
several ESBMC versions side by side. It carries what the ingestion gate needs and
what the portal renders, because they are the same data: the command, what the
front end actually encoded, and the verdict it reached.

  record.py <program.ld> <props.yaml> <expected:true|false> \
            --tool v8.4=/path/to/esbmc --tool master=/path/to/esbmc [-o out.json]

Exit status is 1 when any tool's ingestion gate rejects the record, so this doubles
as a CI check.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import yaml

from paths import ROOT, portable

WATCHDOG = ["--ld-scan-watchdog", "--ld-scan-budget", "8"]
IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
KEYWORDS = {"true", "false", "TRUE", "FALSE", "AND", "OR", "NOT"}
NOISE = re.compile(r"^\s*(//|\^+|$)")


def run_esbmc(esbmc, args):
    """Invoke one ESBMC build and return its combined output."""
    out = subprocess.run([esbmc, *args], capture_output=True, text=True, check=False)
    return (out.stdout or "") + (out.stderr or "")


def build_commit(esbmc):
    """Short commit of the source tree this binary was built from.

    Both local builds answer --version with 8.4.0, so the version string cannot
    tell them apart. The commit is what makes a recorded run identifiable.
    """
    path = os.path.dirname(os.path.abspath(esbmc))
    while path not in ("/", ""):
        if os.path.exists(os.path.join(path, ".git")):  # a worktree has .git as a file
            out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, check=False)
            return out.stdout.strip() or None
        path = os.path.dirname(path)
    return None


def tool_info(esbmc):
    """Version, build commit, and platform of one build."""
    raw = run_esbmc(esbmc, ["--version"]).strip()
    m = re.search(r"ESBMC version (\S+) .*?(\S+ \S+)$", raw)
    return {"path": portable(esbmc), "raw": raw,
            "version": m.group(1) if m else None,
            "commit": build_commit(esbmc),
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


IMPLIES = re.compile(r"(.+?)\s*->\s*(.+)")


def rewrite_implication(expr):
    """`A -> B` as `!(A && !(B))`: --ld-props has no implication operator, and
    silently reads the whole expression as one undeclared variable name instead."""
    m = IMPLIES.match(expr.strip())
    if not m:
        return expr
    a, b = m.group(1).strip(), m.group(2).strip()
    return f"!({a} && !({b}))"


def props_for_esbmc(props_path, tmp_dir):
    """The props.yaml ESBMC actually reads: unchanged, unless some property uses
    `->`, in which case a rewritten copy is written into `tmp_dir` and returned
    instead. `properties_file` in the record still names the original."""
    with open(props_path, encoding="utf-8") as fh:
        text = fh.read()
    props = yaml.safe_load(text)
    if not any("->" in (p.get("expression") or "") for p in props.get("properties", [])):
        return props_path
    for p in props.get("properties", []):
        if p.get("expression"):
            p["expression"] = rewrite_implication(p["expression"])
    rewritten = os.path.join(tmp_dir, "props_no_implies.yaml")
    with open(rewritten, "w", encoding="utf-8") as fh:
        yaml.safe_dump(props, fh)
    return rewritten


def encoding(esbmc, program):
    """The scan body as the front end produced it.

    Keeps the branch guards. An ASSIGN-only view hides them, which makes guarded
    accumulators look like unconditional constants and invites a wrong reading of
    what the tool did.
    """
    txt = run_esbmc(esbmc, [program, "--goto-functions-only"])
    marker = "scan_loop (ld::scan_loop):"
    body = txt.split(marker, 1)[1] if marker in txt else txt
    body = body.split("END_FUNCTION", 1)[0]
    lines = [ln.rstrip() for ln in body.splitlines()
             if not NOISE.match(ln) and not ln.startswith("ESBMC version")]
    assigns = [m.group(1) for m in re.finditer(r"ASSIGN (\S+)\s*=", body)]
    counts = {}
    for name in assigns:
        counts[name] = counts.get(name, 0) + 1
    return lines, counts


def elide(trace, head=60, tail=60):
    """Keep the ends that carry evidence and mark what was dropped.

    Unwinding a 32767-scan fuse produces a quarter of a million trace lines, nearly
    all of them identical scans. What a reader needs is the opening assignments and
    the violated-property block; the middle is volume. Storing it whole made one
    record 14 MB and the page that showed it 37 MB.

    The tail is taken from the violated-property block rather than from the end of
    the output, because ESBMC prints its per-claim summary after it and that summary
    would otherwise crowd out the finding.
    """
    if trace is None:
        return None
    lines = trace.splitlines()
    if len(lines) <= head + tail:
        return trace
    marks = [i for i, ln in enumerate(lines) if ln.strip().startswith("Violated property")]
    start = max(marks[-1] - 6, head) if marks else max(len(lines) - tail, head)
    kept = lines[start:start + tail] if marks else lines[-tail:]
    omitted = start - head
    if omitted <= 0:
        return trace
    return "\n".join(lines[:head]
                     + ["", f"... {omitted} lines omitted from the middle of the trace "
                            f"({len(lines)} lines in total) ...", ""]
                     + kept)

def check_gate(counts, pvars):
    """Every property variable must be assigned inside the scan loop.

    Counts come from the scan body only, so the zero-initialisers emitted outside
    it do not qualify. A silently dropped body leaves those initialisers behind and
    an empty scan loop, at which point every safety property holds vacuously.
    """
    missing = [v for v in pvars if counts.get(v, 0) < 1]
    return missing, ("pass" if counts and not missing else "fail")


def resolve_mode(mode, expected):
    """k-induction proves an expected-SAFE program; BMC hunts for the counterexample."""
    if mode != "auto":
        return mode
    return "kinduction" if expected else "bmc"


def counterexample(txt):
    """The violated-property trace, elided, with repository paths made relative.

    ESBMC names the file it read absolutely, which is the machine that recorded the
    run rather than anything a reader can act on.
    """
    match = re.search(r"^State 1.*?(?=\n+VERIFICATION)", txt, re.S | re.M)
    if not match:
        return None
    return elide(match.group(0).strip()).replace(str(ROOT) + os.sep, "")


def command_line(esbmc, args, program, source, converted):
    """The command a reader can replay, including the copy ESBMC's extension forces.

    ESBMC picks its LD front end from the file extension, so a PLCopen `.xml` is
    copied to `.ld` for the run and removed afterwards. A command that omits the copy
    names a file the repository does not contain.

    A source written in the plain-text LD DSL is not byte-identical to what ESBMC
    read: `tools/ld_text_to_xml.py` converted it to PLCopen XML first. Printing a
    plain `cp` there would name a command that feeds ESBMC a file it cannot parse.
    """
    shown = " ".join([os.path.basename(esbmc), *(portable(a) for a in args)])
    if source and source != program and converted:
        return (f"python3 -m tools.ld_text_to_xml {portable(source)} > {portable(program)}"
                f"\n{shown}")
    if source and source != program:
        return f"cp {portable(source)} {portable(program)}\n{shown}"
    return shown


def verify(esbmc, paths, props_path, timeout, mode, converted):
    """Run the verification and classify the outcome.

    `paths` is (program, source): the file ESBMC reads, and the file that lives in the
    repository. They differ whenever a `.ld` copy was made purely for the extension,
    or when `source` is in the plain-text LD DSL and was converted to XML first.
    """
    program, source = paths
    flags = ["--k-induction"] if mode == "kinduction" else ["--incremental-bmc", "--unwind", "20"]
    props = ["--ld-props", props_path] if props_path else []
    args = [program, *props, *flags, *WATCHDOG, "--timeout", f"{timeout}s"]
    start = time.time()
    txt = run_esbmc(esbmc, args)
    if re.search(r"verification successful", txt, re.I):
        verdict = "SAFE"
    elif re.search(r"verification failed", txt, re.I):
        verdict = "VIOLATION"
    elif re.search(r"PARSING ERROR|CONVERSION ERROR", txt):
        verdict = "error"
    else:
        verdict = "unknown"
    trace = counterexample(txt) if verdict == "VIOLATION" else None
    proof = re.search(r"Solution found by (.+)", txt)
    return {"command": command_line(esbmc, args, program, source, converted),
            "verdict": verdict, "proof": proof.group(1).strip() if proof else None,
            "cpu_time_s": round(time.time() - start, 3), "counterexample": trace}


def record_one(label, esbmc, args, props_path, pvars):
    """Everything one build has to say about this task."""
    lines, counts = encoding(esbmc, args.program)
    missing, gate = check_gate(counts, pvars)
    expected = args.expected == "true"
    result = verify(esbmc, (args.program, args.source), props_path, args.timeout,
                    resolve_mode(args.mode, expected), args.converted_from_text_ld)
    expected_v = "SAFE" if expected else "VIOLATION"
    if result["verdict"] in ("error", "unknown"):
        status = result["verdict"]
    else:
        status = "correct" if result["verdict"] == expected_v else "wrong"
    return label, {"tool": tool_info(esbmc), "status": status,
                   "encoding": {"scan_body": lines, "assignment_counts": counts,
                                "not_driven_by_body": missing, "gate": gate},
                   **result}


def main():
    """Capture one record across every named build."""
    ap = argparse.ArgumentParser()
    ap.add_argument("program")
    ap.add_argument("props")
    ap.add_argument("expected", choices=["true", "false"])
    ap.add_argument("--source", help="the repository file this run was copied from, when "
                                     "the copy exists only to give ESBMC a .ld extension")
    ap.add_argument("--converted-from-text-ld", action="store_true",
                    help="`program` is tools/ld_text_to_xml.py's XML rendering of "
                         "`source`, not a byte-identical copy of it")
    ap.add_argument("--tool", action="append", required=True, metavar="LABEL=PATH")
    ap.add_argument("--mode", choices=["auto", "kinduction", "bmc"], default="auto",
                    help="auto picks k-induction for an expected-SAFE task and "
                         "incremental BMC otherwise. Force k-induction on a "
                         "discriminator, where SUCCESSFUL has to be a proof and "
                         "not a bounded silence.")
    ap.add_argument("--watchdog-only", action="store_true",
                    help="termination task: omit --ld-props, the watchdog carries it")
    ap.add_argument("-o", "--out")
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    with open(args.props, encoding="utf-8") as fh:
        props = yaml.safe_load(fh)
    pvars = property_variables(props)

    with tempfile.TemporaryDirectory() as tmp_dir:
        props_path = None if args.watchdog_only else props_for_esbmc(args.props, tmp_dir)
        runs = dict(record_one(t.split("=", 1)[0], t.split("=", 1)[1], args, props_path, pvars)
                    for t in args.tool)

    record = {
        "schema_version": "0.3",
        "recorded_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": os.path.relpath(args.source or args.program),
        "properties_file": os.path.relpath(args.props),
        "properties": props.get("properties", []),
        "property_variables": pvars,
        "expected_verdict": "SAFE" if args.expected == "true" else "VIOLATION",
        "runs": runs,
    }

    text = json.dumps(record, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        summary = "  ".join(f"{k}:{v['verdict']}/{v['encoding']['gate']}"
                            for k, v in runs.items())
        print(f"{os.path.relpath(args.program):26} {summary}  -> {args.out}")
    else:
        print(text)
    return 0 if all(r["encoding"]["gate"] == "pass" for r in runs.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
