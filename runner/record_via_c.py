#!/usr/bin/env python3
"""Record a verification run that reaches ESBMC through C rather than the LD front end.

ESBMC registers one IEC extension and reads one body type, so ST, IL, FBD and SFC
programs never reach its solver by the direct route. They do reach it through the
compiler chain two other projects already provide:

    PLCopen XML --Beremiz--> Structured Text --MatIEC--> C --> ESBMC C front end

ST and IL skip the first hop, because MatIEC compiles them as they stand.

    record_via_c.py <program> <props.yaml> <true|false> --tool LABEL=PATH [-o out.json]

The record follows record.py's schema with route "via-c", so a benchmark page can show
both routes side by side, and adds a "toolchain" block naming the Beremiz and MatIEC
checkouts that produced the C. That block is why via-c records are schema 0.4.

What this asks is "is the program correct", not "does the LD front end read it
correctly": MatIEC's semantics and, for graphical bodies, Beremiz's rendering both
join the trusted base.
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

from paths import portable

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
        if expr is None:   # termination: the unwinding assertion carries it
            continue
        rendered = expr
        for name in sorted({n for _k, _t, n in variables} | {n.upper() for n in ins},
                           key=len, reverse=True):
            rendered = re.sub(rf"\b{name}\b", read(name), rendered, flags=re.I)
        body.append(f'    __ESBMC_assert({rendered}, "{prop_id}");')
    body += ["  }", "  return 0;", "}"]
    return "\n".join(body)


def is_termination(props_path):
    """True when the file's only claim is that every scan finishes."""
    props = yaml.safe_load(props_path.read_text(encoding="utf-8"))
    kinds = {prop.get("kind") for prop in props.get("properties", [])}
    return kinds == {"termination"}


def properties(props_path):
    """Each property as an assertion over the program's variables.

    Reachability inverts: the claim is written so that reaching the state fails it,
    which makes ESBMC's counterexample the witness.

    Termination is not an assertion over variables, so it returns none and relies on
    ESBMC's unwinding assertions instead: a loop that cannot be unwound within the
    bound fails the run. That is evidence rather than proof, since a merely deep loop
    fails the same way, which is why the caller records the bound it used.
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
        elif kind == "termination":
            out.append((prop["id"], None))
        else:
            skipped.append(f'{prop["id"]}:{kind}')
    if not out:
        raise RuntimeError("no property this route can express: " + ", ".join(skipped))
    return out


def entry_struct(program, header):
    """The generated struct for the POU whose inputs the harness drives.

    MatIEC emits function blocks before the program that calls them, so taking the
    first struct picked `valves_handler` while `inputs_of` read `program0`'s interface,
    and the harness then assigned variables the struct does not declare.
    """
    structs = re.findall(r"\}\s*(\w+_data__);", header)
    if not structs:
        raise RuntimeError("no POU instance struct in the generated header")
    if program.suffix == ".xml":
        named = re.search(r'<pou name="(\w+)" pouType="program"',
                          program.read_text(encoding="utf-8"))
        if named:
            want = named.group(1).upper() + "_data__"
            if want in structs:
                return want
    return structs[0]


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
    struct_name = entry_struct(program, header)
    harness_file = outdir / "harness.c"
    pou = (struct_name, struct_name[: -len("_data__")])
    harness_file.write_text(harness(pou, declared_vars(header), inputs_of(program),
                                    properties(props_path), scans), encoding="utf-8")
    return harness_file, outdir


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
    return {"path": portable(esbmc), "raw": raw, "commit": commit,
            "version": match.group(1) if match else None,
            "platform": match.group(2) if match else None}


def repo_state(path):
    """Short commit and working-tree cleanliness for one dependency checkout."""
    real = os.path.realpath(path)
    if not os.path.exists(os.path.join(real, ".git")):
        return {"path": portable(real), "commit": None, "dirty": None}
    code, commit = run(["git", "-C", real, "rev-parse", "--short", "HEAD"])
    if code != 0:
        return {"path": portable(real), "commit": None, "dirty": None}
    _, status = run(["git", "-C", real, "status", "--porcelain"])
    return {"path": portable(real), "commit": commit.strip(), "dirty": bool(status.strip())}


def toolchain_info():
    """Beremiz and MatIEC, which rewrite the program before ESBMC ever sees it.

    A via-C verdict rests on that translation as much as on the solver, so a record
    naming only the ESBMC commit cannot be reproduced. `dirty` carries the case that
    bites in practice: a locally patched generator emits different ST from the commit
    it reports, and nothing else in the record would show it.
    """
    return {"beremiz": repo_state(TOOLS / "beremiz"),
            "matiec": repo_state(TOOLS / "matiec")}


def verify(esbmc, generated, task, timeout, scans):
    """Run ESBMC over the generated C and classify the outcome.

    `task` is (expected, termination): whether the program should verify, and whether
    the only claim is that every scan finishes.

    The harness loop is a fixed count, so the unwinding bound has to clear it or a
    bomb on a long fuse is simply never reached and the run reports SAFE.

    Plain unwinding rather than incremental BMC, because the loop is already finite:
    incremental mode stops when its forward condition cannot prove completeness and
    reports UNKNOWN, which on a 255-scan fuse it does in two seconds while plain
    unwinding finds the violation in one.
    """
    harness_file, outdir = generated
    expected, termination = task
    # A termination task is decided by the unwinding assertions, so it always takes a
    # plain bound: k-induction would prove the property without ever reporting that a
    # loop failed to close.
    mode = (["--unwind", str(scans + 2)] if termination or not expected
            else ["--k-induction"])
    args = [str(harness_file), "-I", str(TOOLS / "matiec" / "lib" / "C"),
            "-I", str(outdir), *mode, "--timeout", f"{timeout}s"]
    start = time.time()
    _, out = run([esbmc, *args])
    # A timeout prints "ERROR: Timed out", but running out of budget is not the same
    # thing as a malformed program, and a table that calls it an error says the suite
    # produced something ESBMC could not read.
    verdict = ("SAFE" if "VERIFICATION SUCCESSFUL" in out else
               "VIOLATION" if "VERIFICATION FAILED" in out else
               "timeout" if "Timed out" in out else
               "error" if "ERROR" in out else "unknown")
    trace = None
    if verdict == "VIOLATION":
        match = re.search(r"^State 1.*?(?=\n+VERIFICATION)", out, re.S | re.M)
        trace = elide(match.group(0).strip()) if match else None
        if trace:
            trace = trace.replace(str(outdir), "<generated>")
            trace = trace.replace(str(TOOLS), "$PLC_TOOLS")
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
        result = verify(path, (harness_file, outdir),
                        (expected, is_termination(props_path)), args.timeout, args.scans)
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
            "schema_version": "0.4", "route": "via-c", "scans": args.scans,
            "toolchain": toolchain_info(),
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
