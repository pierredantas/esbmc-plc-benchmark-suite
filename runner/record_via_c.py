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
DECL = re.compile(r"__DECLARE_(VAR|LOCATED)\((\w+),\s*(\w+)\)")
LOCATED = re.compile(r"(\w+)\s+AT\s+%([IQM])", re.I)
VAR_BLOCK = re.compile(r"( *VAR(?:_INPUT|_OUTPUT|_IN_OUT)?\b[^\n]*)\n(.*?)\n( *END_VAR)", re.S)
# What an unconstrained input of each IEC type looks like to the solver.
NONDET = {"BOOL": "nondet_bool()", "SINT": "nondet_char()", "INT": "nondet_int()",
          "DINT": "nondet_int()", "LINT": "nondet_long()", "UINT": "nondet_uint()",
          "UDINT": "nondet_uint()", "REAL": "nondet_float()", "LREAL": "nondet_double()",
          "TIME": "nondet_int()", "WORD": "nondet_uint()", "BYTE": "nondet_uint()"}


def run(cmd, **kw):
    """A subprocess whose combined output is what we care about."""
    out = subprocess.run(cmd, capture_output=True, text=True, check=False, **kw)
    return out.returncode, (out.stdout or "") + (out.stderr or "")


def to_st(program, workdir):
    """Structured Text for this program, translating a graphical body if needed."""
    if program.suffix in (".st", ".il"):
        return split_var_blocks(program.read_text(encoding="utf-8"))
    xml = workdir / "in.xml"
    xml.write_text(program.read_text(encoding="utf-8").replace("tc6_0200", "tc6_0201"),
                   encoding="utf-8")
    code, out = run([sys.executable, str(TOOLS / "xml2st.py"), str(xml)])
    if code != 0:
        raise RuntimeError(f"Beremiz could not render this body: {out.strip()[-200:]}")
    return out


def declared_vars(header):
    """Every variable in the POU struct: (storage, type, name), declaration order.

    MatIEC uppercases identifiers and gives a located variable a pointer rather than
    a value, so a harness has to know which is which before it can read one.
    """
    return list(DECL.findall(header))


def split_var_blocks(text):
    """Give located declarations a block of their own.

    MatIEC rejects a VAR block that mixes `x AT %IX0.0 : BOOL;` with a plain
    declaration, which several benchmarks here do. Splitting is a rewrite of the
    declaration only; no statement and no initial value changes.
    """
    def fix(match):
        head, body, tail = match.groups()
        located = [ln for ln in body.splitlines() if LOCATED.search(ln)]
        plain = [ln for ln in body.splitlines() if ln.strip() and not LOCATED.search(ln)]
        if not located or not plain:
            return match.group(0)
        return (f"{head}\n" + "\n".join(located) + f"\n{tail}\n{head}\n"
                + "\n".join(plain) + f"\n{tail}")
    return VAR_BLOCK.sub(fix, text)


def inputs_of(program):
    """The variables the environment drives, read from the program's own interface."""
    text = program.read_text(encoding="utf-8")
    if program.suffix == ".xml":
        block = re.search(r"<inputVars>(.*?)</inputVars>", text, re.S)
        return re.findall(r'<variable name="(\w+)"', block.group(1)) if block else []
    block = re.search(r"VAR_INPUT(.*?)END_VAR", text, re.S)
    names = re.findall(r"^\s*(\w+)\s*:", block.group(1), re.M) if block else []
    # A variable mapped to an input image is driven by the plant, not the program.
    names += [name for name, direction in LOCATED.findall(text) if direction.upper() == "I"]
    return names


def harness(pou, variables, ins, expressions, scans):
    """A C main that drives the scan loop and asserts the properties every scan."""
    struct, prefix = pou
    storage = {name: kind for kind, _type, name in variables}
    types = {name: iec for _kind, iec, name in variables}

    def resolve(name):
        """Source spelling to the identifier MatIEC emitted."""
        return name.upper() if name.upper() in storage else name

    def read(name):
        target = resolve(name)
        macro = "__GET_LOCATED" if storage.get(target) == "LOCATED" else "__GET_VAR"
        return f"{macro}(d.{target},)"

    def write(name, value):
        target = resolve(name)
        macro = "__SET_LOCATED" if storage.get(target) == "LOCATED" else "__SET_VAR"
        return f"    {macro}(d., {target}, , {value});"

    body = ['#include "iec_std_lib.h"', '#include "POUS.h"', '#include "POUS.c"', ""]
    if any(kind == "LOCATED" for kind, _t, _n in variables):
        # A located variable points into the I/O image, which the runtime normally
        # supplies by expanding this header. Standing in for the runtime is what
        # lets the program run without one.
        body += ["#define __LOCATED_VAR(type, name, ...) \\",
                 "  type name##__image; type *name = &name##__image;",
                 '#include "LOCATED_VARIABLES.h"', "#undef __LOCATED_VAR", ""]
    body += ["int main(void) {", f"  {struct} d = {{0}};",
             f"  {prefix}_init__(&d, 0);",
             f"  for (int scan = 0; scan < {scans}; scan++) {{"]
    body += [write(name, NONDET.get(types.get(resolve(name), "BOOL"), "nondet_int()"))
             for name in ins]
    body.append(f"    {prefix}_body__(&d);")
    for prop_id, expr in expressions:
        rendered = expr
        for name in sorted({n for _k, _t, n in variables} | {n.upper() for n in ins},
                           key=len, reverse=True):
            rendered = re.sub(rf"\b{name}\b", read(name), rendered, flags=re.I)
        body.append(f'    __ESBMC_assert({rendered}, "{prop_id}");')
    body += ["  }", "  return 0;", "}"]
    return "\n".join(body)


def properties(props_path):
    """Each property as an assertion over the program's variables.

    Reachability inverts: the claim is written so that reaching the state fails it,
    which makes ESBMC's counterexample the witness. Termination is not expressible
    as an assertion inside a bounded scan harness, so it is left to the scan
    watchdog on the ladder route.
    """
    props = yaml.safe_load(props_path.read_text(encoding="utf-8"))
    out, skipped = [], []
    for prop in props.get("properties", []):
        kind, expr = prop.get("kind"), prop.get("expression")
        if kind == "invariant" and expr:
            out.append((prop["id"], expr))
        elif kind == "absence" and expr:
            out.append((prop["id"], f"!({expr})"))
        elif kind == "reachability" and expr:
            out.append((prop["id"], f"!({expr})"))
        elif kind == "mutual_exclusion":
            out.append((prop["id"], "!(" + " && ".join(prop["variables"]) + ")"))
        else:
            skipped.append(f'{prop["id"]}:{kind}')
    if not out:
        raise RuntimeError("no property this route can express: " + ", ".join(skipped))
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


def verify(esbmc, generated, expected, timeout, scans):
    """Run ESBMC over the generated C and classify the outcome.

    The harness loop is a fixed count, so the unwinding bound has to clear it or a
    bomb on a long fuse is simply never reached and the run reports SAFE.

    Plain unwinding rather than incremental BMC, because the loop is already finite:
    incremental mode stops when its forward condition cannot prove completeness and
    reports UNKNOWN, which on a 255-scan fuse it does in two seconds while plain
    unwinding finds the violation in one.
    """
    harness_file, outdir = generated
    mode = (["--k-induction"] if expected else ["--unwind", str(scans + 2)])
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


def build_record(args, paths, generated):
    """Every build's answer, plus what it was asked."""
    program, props_path = paths
    harness_file, outdir = generated
    expected = args.expected == "true"
    runs = {}
    for spec in args.tool:
        label, path = spec.split("=", 1)
        result = verify(path, (harness_file, outdir), expected, args.timeout, args.scans)
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
        runs = build_record(args, (program, props_path), (harness_file, outdir))
        record = {
            "schema_version": "0.3", "route": "via-c", "scans": args.scans,
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
