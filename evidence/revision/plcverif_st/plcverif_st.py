#!/usr/bin/env python3
"""PLCverif on the suite's native structured-text variants (R1.1).

A program is converted to SCL (PROGRAM -> FUNCTION_BLOCK, CONFIGURATION dropped, VAR_INPUT kept,
properties as //#ASSERT lines at the end of the scan, encoded as runner/record_via_c.py encodes them) and
checked with PLCverif's NuSMV backend. Variants with a termination or witness property, a user function
block, or a loop are skipped, because PLCverif cannot express the property or the pilot cannot convert them.

    plcverif_st.py SUITE_V131 OUT JAVA PLCVERIF NUSMV BUILTIN_SCL IEC_BLOCKS_SCL [NAME ...]
"""
import csv, json, os, pathlib, re, subprocess, sys, time
import yaml

S7_OPERAND = re.compile(r"\b((?:T|C|Z|I|Q|E|A|M|L|DB|DI|FB|FC|SFB|SFC|UDT|OB|PIB|PIW|PID|PQB|PQW|PQD|IB|IW|ID|QB|QW|QD|"
                        r"EB|EW|ED|AB|AW|AD|MB|MW|MD|LB|LW|LD)\d+)\b", re.I)
SUPPORTED = {"invariant", "absence", "reachability", "mutual_exclusion"}
IMPLIES = re.compile(r"^(.*?)\s*->\s*(.*)$")


def rewrite_implication(e):
    m = IMPLIES.match(e.strip())
    return f"!({m.group(1).strip()} && !({m.group(2).strip()}))" if m else e


def scl_expr(expr):
    e = expr.replace("&&", " AND ").replace("||", " OR ").replace("!=", "<>").replace("==", "=")
    e = re.sub(r"!\s*", "NOT ", e)
    return re.sub(r"\s+", " ", e).strip()


def claims(props):
    out = []
    for p in props:
        kind, expr = p["kind"], p.get("expression")
        expr = rewrite_implication(expr) if expr else expr
        if kind == "invariant" and expr:
            out.append((p["id"], expr))
        elif kind in ("absence", "reachability") and expr:
            out.append((p["id"], f"!({expr})"))
        elif kind == "mutual_exclusion" and p.get("variables"):
            out.append((p["id"], "!(" + " && ".join(p["variables"]) + ")"))
    return out


AT_DECL = re.compile(r"^(\s*\w+)\s+AT\s+%([IQM])\w*[\d.]*\s*:(.*)$", re.I)


def relocate(decls):
    """Drop AT %address clauses (PLCverif's SCL reader rejects them); %I variables become VAR_INPUT."""
    blocks, ins = [], []
    for kind, block in re.findall(r"(VAR\w*)\s(.*?)END_VAR", decls, re.S):
        keep = []
        for ln in block.splitlines():
            m = AT_DECL.match(ln)
            if m and m.group(2).upper() == "I":
                ins.append(f"{m.group(1)} :{m.group(3)}")
            elif m:
                keep.append(f"{m.group(1)} :{m.group(3)}")
            elif ln.strip():
                keep.append(ln)
        if keep:
            blocks.append((kind, keep))
    if ins:
        blocks.insert(0, ("VAR_INPUT", ins))
    return "".join(f"  {k}\n" + "\n".join(ls) + "\n  END_VAR\n" for k, ls in blocks)


def convert(st_text, props):
    """Return (scl_text, entry, uses) or raise ValueError with the reason the pilot skips it."""
    kinds = {p["kind"] for p in props}
    if not kinds <= SUPPORTED:
        raise ValueError("property kind " + ",".join(sorted(kinds - SUPPORTED)))
    st = re.sub(r"\(\*.*?\*\)", "", st_text, flags=re.S).split("CONFIGURATION", 1)[0]
    if re.search(r"\b(FUNCTION_BLOCK|FUNCTION)\b", st):
        raise ValueError("user function block")
    if re.search(r"\b(WHILE|REPEAT|FOR)\b", st, re.I):
        raise ValueError("loop")
    if len(re.findall(r"\bPROGRAM\b", st)) != 1:
        raise ValueError("not one PROGRAM")
    m = re.search(r"PROGRAM\s+(\w+)(.*?)END_PROGRAM", st, re.S)
    pou, rest = m.group(1), m.group(2)
    last = list(re.finditer(r"END_VAR", rest))[-1].end()
    decls, body = rest[:last], rest[last:]
    decls = relocate(decls)
    asserts = [f"  //#ASSERT {scl_expr(c)} : {i}" for i, c in claims(props)]
    if not asserts:
        raise ValueError("no claim")
    text = f"{decls}\nBEGIN\n{body.strip()}\n" + "\n".join(asserts) + "\n"
    text = S7_OPERAND.sub(lambda mm: "v_" + mm.group(1), text)
    uses = {k for k in ("TON", "TOF", "TP", "CTU", "CTD", "R_TRIG", "F_TRIG") if re.search(rf"\b{k}\b", st)}
    return f"FUNCTION_BLOCK {pou.upper()}\n{text}END_FUNCTION_BLOCK\n", pou.upper(), uses


def run_plcverif(java, plcverif, nusmv, files, entry, ident, out):
    args = [java, "-jar", next(pathlib.Path(plcverif, "plugins").glob("org.eclipse.equinox.launcher_*.jar")).as_posix(),
            f"-id={ident}", "-job=verif", "-lf=step7"]
    args += [f"-sourcefiles.{i}={f}" for i, f in enumerate(files)]
    args += [f"-lf.entry={entry}", "-job.backend=nusmv", f"-job.backend.binary_path={nusmv}",
             "-job.backend.timeout=120", "-job.req=assertion", "-job.reporters.0=plaintext", f"-output={out}"]
    t0 = time.time()
    p = subprocess.run(args, cwd=plcverif, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    rep = pathlib.Path(out, f"{ident}.report.txt")
    txt = rep.read_text(errors="replace") if rep.exists() else p.stdout
    res = re.findall(r"requirement is (SATISFIED|VIOLATED|INCONCLUSIVE|[A-Z]+)", txt)
    return res, round(dt, 2), txt


def main():
    suite, out, java, plcverif, nusmv, builtin, blocks = sys.argv[1:8]
    only = set(sys.argv[8:])
    out = pathlib.Path(out); (out / "scl").mkdir(parents=True, exist_ok=True)
    rows = [v for v in csv.DictReader(open(pathlib.Path(__file__).parents[1] / "variants_302.csv"))
            if v["core_suite"] == "yes" and v["lang"] == "ST"]
    results = {}
    for v in rows:
        name = f"{v['id']}__{v['file'].split('.')[0]}"
        if only and name not in only:
            continue
        d = next(pathlib.Path(suite, "benchmarks").glob(f"*/{v['id']}"))
        props = yaml.safe_load((d / "props.yaml").read_text())["properties"]
        try:
            scl, entry, uses = convert((d / v["file"]).read_text(), props)
        except ValueError as e:
            results[name] = {"status": "skipped", "reason": str(e)}
            continue
        (out / "scl" / f"{name}.scl").write_text(scl)
        files = [(out / "scl" / f"{name}.scl").as_posix()]
        if uses & {"TON", "TOF", "TP"}:
            files.append(builtin)
        if uses & {"CTU", "CTD", "R_TRIG", "F_TRIG"}:
            files.append(blocks)
        res, dt, txt = run_plcverif(java, plcverif, nusmv, files, entry, name, (out / "out" / name).as_posix())
        verdict = {"SATISFIED": "SAFE", "VIOLATED": "VIOLATION"}.get(res[0] if res else "", "unknown")
        results[name] = {"status": "run", "verdict": verdict, "raw": res, "time_s": dt, "expected": v["exp"]}
        print(name, results[name])
    json.dump(results, open(out / "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
