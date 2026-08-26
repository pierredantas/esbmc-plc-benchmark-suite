#!/usr/bin/env python3
"""Record a verification run that reaches ESBMC through C rather than the LD front end.

ESBMC registers one IEC extension and reads one body type, so ST, IL, FBD and SFC
programs never reach its solver by the direct route. They do reach it through the
compiler chain two other projects already provide:

    PLCopen XML --Beremiz--> Structured Text --MatIEC--> C --> ESBMC C front end

ST and IL skip the first hop, because MatIEC compiles them as they stand.

    record_via_c.py <program> <props.yaml> <true|false> --tool LABEL=PATH [-o out.json]

The record uses the same schema as record.py, with route "via-c", so a benchmark page
can show both routes side by side. What this asks is "is the program correct", not
"does the LD front end read it correctly": MatIEC's semantics and, for graphical
bodies, Beremiz's rendering both join the trusted base.
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = pathlib.Path(os.environ.get("PLC_TOOLS", pathlib.Path.home() / "plc-tools"))
DECL = re.compile(r"__DECLARE_VAR\((\w+),\s*(\w+)\)")


def run(cmd, **kw):
    """A subprocess whose combined output is what we care about."""
    out = subprocess.run(cmd, capture_output=True, text=True, check=False, **kw)
    return out.returncode, (out.stdout or "") + (out.stderr or "")


def to_st(program, workdir):
    """Structured Text for this program, translating a graphical body if needed."""
    if program.suffix in (".st", ".il"):
        return program.read_text(encoding="utf-8")
    xml = workdir / "in.xml"
    xml.write_text(program.read_text(encoding="utf-8").replace("tc6_0200", "tc6_0201"),
                   encoding="utf-8")
    code, out = run([sys.executable, str(TOOLS / "xml2st.py"), str(xml)])
    if code != 0:
        raise RuntimeError(f"Beremiz could not render this body: {out.strip()[-200:]}")
    return out


def declared_vars(header):
    """Every variable MatIEC put in the POU instance struct, in declaration order."""
    return list(DECL.findall(header))


def inputs_of(program):
    """The variables the environment drives, read from the program's own interface."""
    text = program.read_text(encoding="utf-8")
    if program.suffix == ".xml":
        block = re.search(r"<inputVars>(.*?)</inputVars>", text, re.S)
        return re.findall(r'<variable name="(\w+)"', block.group(1)) if block else []
    block = re.search(r"VAR_INPUT(.*?)END_VAR", text, re.S)
    return re.findall(r"^\s*(\w+)\s*:", block.group(1), re.M) if block else []


def harness(pou, variables, ins, expressions, scans):
    """A C main that drives the scan loop and asserts the properties every scan."""
    struct, prefix = pou

    def ref(name):
        return f"__GET_VAR(d.{name},)"

    body = ['#include "iec_std_lib.h"', '#include "POUS.h"', '#include "POUS.c"', "",
            "int main(void) {", f"  {struct} d = {{0}};", f"  {prefix}_init__(&d, 0);",
            f"  for (int scan = 0; scan < {scans}; scan++) {{"]
    body += [f"    __SET_VAR(d., {name}, , nondet_bool());" for name in ins]
    body.append(f"    {prefix}_body__(&d);")
    for prop_id, expr in expressions:
        rendered = expr
        for _, name in sorted(variables, key=lambda v: -len(v[1])):
            rendered = re.sub(rf"\b{name}\b", ref(name), rendered)
        body.append(f'    __ESBMC_assert({rendered}, "{prop_id}");')
    body += ["  }", "  return 0;", "}"]
    return "\n".join(body)


def properties(props_path):
    """The invariant expressions this benchmark states, in C form."""
    props = yaml.safe_load(props_path.read_text(encoding="utf-8"))
    out = []
    for prop in props.get("properties", []):
        if prop.get("kind") == "invariant" and prop.get("expression"):
            out.append((prop["id"], prop["expression"]))
        elif prop.get("kind") == "mutual_exclusion":
            out.append((prop["id"], "!(" + " && ".join(prop["variables"]) + ")"))
    return out


def build(program, props_path, workdir, scans):
    """Compile the program to C and write the harness beside it."""
    st_text = to_st(program, workdir)
    st_file = workdir / "prog.st"
    st_file.write_text(st_text, encoding="utf-8")
    outdir = workdir / "c"
    outdir.mkdir(exist_ok=True)
    code, out = run([str(TOOLS / "matiec" / "iec2c"), "-I", str(TOOLS / "matiec" / "lib"),
                     "-T", str(outdir), str(st_file)])
    if code != 0:
        raise RuntimeError(f"iec2c rejected the program: {out.strip()[-200:]}")
    header = (outdir / "POUS.h").read_text(encoding="utf-8")
    struct = re.search(r"\}\s*(\w+_data__);", header)
    if not struct:
        raise RuntimeError("no POU instance struct in the generated header")
    struct_name = struct.group(1)
    harness_file = outdir / "harness.c"
    pou = (struct_name, struct_name[: -len("_data__")])
    harness_file.write_text(harness(pou, declared_vars(header), inputs_of(program),
                                    properties(props_path), scans), encoding="utf-8")
    return harness_file, outdir


def tool_info(esbmc):
    """Version, build commit and platform, so a column names a specific binary."""
    _, raw = run([esbmc, "--version"])
    raw = raw.strip()
    match = re.search(r"ESBMC version (\S+) .*?(\S+ \S+)$", raw)
    path = os.path.dirname(os.path.abspath(esbmc))
    commit = None
    while path not in ("/", ""):
        if os.path.exists(os.path.join(path, ".git")):
            _, out = run(["git", "-C", path, "rev-parse", "--short", "HEAD"])
            commit = out.strip() or None
            break
        path = os.path.dirname(path)
    return {"path": esbmc, "raw": raw, "commit": commit,
            "version": match.group(1) if match else None,
            "platform": match.group(2) if match else None}


def verify(esbmc, harness_file, outdir, expected, timeout):
    """Run ESBMC over the generated C and classify the outcome."""
    mode = ["--k-induction"] if expected else ["--incremental-bmc", "--unwind", "10"]
    args = [str(harness_file), "-I", str(TOOLS / "matiec" / "lib" / "C"),
            "-I", str(outdir), *mode, "--timeout", f"{timeout}s"]
    start = time.time()
    _, out = run([esbmc, *args])
    verdict = ("SAFE" if "VERIFICATION SUCCESSFUL" in out else
               "VIOLATION" if "VERIFICATION FAILED" in out else
               "error" if "ERROR" in out else "unknown")
    trace = None
    if verdict == "VIOLATION":
        match = re.search(r"^State 1.*?(?=\n+VERIFICATION)", out, re.S | re.M)
        trace = match.group(0).strip() if match else None
    proof = re.search(r"Solution found by (.+)", out)
    shown = list(args)
    shown[0] = "<generated>/harness.c"
    shown[shown.index(str(outdir))] = "<generated>"
    shown = [a.replace(str(TOOLS), "$PLC_TOOLS") for a in shown]
    return {"solver_command": " ".join([os.path.basename(esbmc), *shown]),
            "verdict": verdict,
            "proof": proof.group(1).strip() if proof else None,
            "cpu_time_s": round(time.time() - start, 3), "counterexample": trace}


def build_record(args, program, props_path, harness_file, outdir):
    """Every build's answer, plus what it was asked."""
    expected = args.expected == "true"
    runs = {}
    for spec in args.tool:
        label, path = spec.split("=", 1)
        result = verify(path, harness_file, outdir, expected, args.timeout)
        result["tool"] = tool_info(path)
        result["command"] = (
            f"runner/record_via_c.py {os.path.relpath(program, ROOT)} "
            f"{os.path.relpath(props_path, ROOT)} {args.expected} "
            f"--tool {label}=<path-to-esbmc>")
        expected_v = "SAFE" if expected else "VIOLATION"
        result["status"] = (result["verdict"] if result["verdict"] in ("error", "unknown")
                            else "correct" if result["verdict"] == expected_v else "wrong")
        runs[label] = result
    return runs


def main():
    """Capture one via-C record across every named build."""
    ap = argparse.ArgumentParser()
    ap.add_argument("program")
    ap.add_argument("props")
    ap.add_argument("expected", choices=["true", "false"])
    ap.add_argument("--tool", action="append", required=True, metavar="LABEL=PATH")
    ap.add_argument("--scans", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    program = pathlib.Path(args.program).resolve()
    props_path = pathlib.Path(args.props).resolve()
    expected = args.expected == "true"

    with tempfile.TemporaryDirectory() as tmp:
        harness_file, outdir = build(program, props_path, pathlib.Path(tmp), args.scans)
        runs = build_record(args, program, props_path, harness_file, outdir)
        record = {
            "schema_version": "0.3", "route": "via-c",
            "recorded_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "program": os.path.relpath(program, ROOT),
            "properties_file": os.path.relpath(props_path, ROOT),
            "properties": yaml.safe_load(props_path.read_text(encoding="utf-8"))["properties"],
            "expected_verdict": "SAFE" if expected else "VIOLATION",
            "generated_c": harness_file.read_text(encoding="utf-8"),
            "runs": runs,
        }
    text = json.dumps(record, indent=2)
    if args.out:
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
        summary = "  ".join(f"{k}:{v['verdict']}" for k, v in runs.items())
        print(f"{os.path.relpath(program, ROOT):48} via-c  {summary}  -> {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
