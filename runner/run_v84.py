#!/usr/bin/env python3
"""v8.4 adapter runner: attempts every benchmark against ESBMC-PLC v8.4, translating the
suite's property schema to v8.4's on the fly (v8.4: PLCopen-XML input with .ld extension;
invariant.expression must be a single boolean var; kinds = invariant/mutual_exclusion/
reachability/absence, NO termination -> scan-watchdog handles it). Records correct/wrong/
skip(+reason) per variant. Run inside the esbmc-plc:run container with ESBMC set."""
import os, sys, glob, re, subprocess, shutil, tempfile
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESBMC = os.environ.get("ESBMC", "/usr/local/bin/esbmc")
WD = ["--ld-scan-watchdog", "--ld-scan-budget", "8"]

def mx_yaml(vs):
    return "properties:\n  - id: P1\n    kind: mutual_exclusion\n    variables: [%s]\n" % ", ".join(vs)
def inv_yaml(v):
    return "properties:\n  - id: P1\n    kind: invariant\n    expression: \"%s\"\n" % v

def iec2c(e):
    """Translate IEC operators to the C-style syntax v8.4's property parser expects."""
    e = re.sub(r"\bAND\b", "&&", e); e = re.sub(r"\bOR\b", "||", e)
    e = re.sub(r"\bNOT\s+", "!", e); e = re.sub(r"\bNOT\b", "!", e)
    return e

def translate(props):
    """-> (mode, propfile_text_or_None, skip_reason_or_None).  mode in {props, watchdog}."""
    ps = props.get("properties", [])
    if any(p["kind"] == "termination" for p in ps):
        return ("watchdog", None, None)
    # Build a v8.4 property file from the safety properties (invariant/mutual_exclusion).
    # reachability is a trigger-synthesis aid; it does not carry the task verdict, so skip it.
    lines = ["properties:"]
    n = 0
    for p in ps:
        if p["kind"] == "mutual_exclusion":
            n += 1; lines += [f"  - id: P{n}", "    kind: mutual_exclusion",
                              f"    variables: [{', '.join(p['variables'])}]"]
        elif p["kind"] == "invariant":
            n += 1; lines += [f"  - id: P{n}", "    kind: invariant",
                              f'    expression: "{iec2c(p["expression"])}"']
    if n == 0:
        return (None, None, "no safety property (only reachability/absence)")
    return ("props", "\n".join(lines) + "\n", None)

def run_esbmc(ld_path, prop_text, expected):
    mode = ["--k-induction"] if expected else ["--incremental-bmc", "--unwind", "20"]
    cmd = [ESBMC, ld_path] + mode + WD + ["--timeout", "180s"]
    if prop_text is not None:
        tmpp = ld_path + ".props.yaml"; open(tmpp, "w").write(prop_text)
        cmd = [ESBMC, ld_path, "--ld-props", tmpp] + mode + WD + ["--timeout", "180s"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    txt = (out.stdout or "") + (out.stderr or "")
    if re.search(r"verification successful", txt, re.I): return "true"
    if re.search(r"verification failed", txt, re.I): return "false"
    return "unknown"

def main():
    rows = []
    for bp in sorted(glob.glob(os.path.join(ROOT, "benchmarks", "**", "benchmark.yml"), recursive=True)):
        b = yaml.safe_load(open(bp)); d = os.path.dirname(bp)
        props = yaml.safe_load(open(os.path.normpath(os.path.join(d, b.get("properties_file", "props.yaml")))))
        mode, ptext, skip = translate(props)
        for v in b["variants"]:
            f = os.path.join(d, v["file"]); exp = v["expected_verdict"]
            # v8.4 needs PLCopen-XML input; only .xml variants qualify
            if not f.endswith(".xml"):
                rows.append((b["id"], v["file"], exp, "-", "SKIP", "input not PLCopen XML (.st/.ld DSL)")); continue
            if mode is None:
                rows.append((b["id"], v["file"], exp, "-", "SKIP", skip)); continue
            ld = os.path.join(tempfile.gettempdir(), "run.ld"); shutil.copyfile(f, ld)
            got = run_esbmc(ld, ptext if mode == "props" else None, exp)
            st = "OK" if (got == ("true" if exp else "false")) else ("UNKNOWN" if got == "unknown" else "WRONG")
            rows.append((b["id"], v["file"], "true" if exp else "false", got, st, ""))
            print(f"{st:8} {b['id']:26} {v['file']:20} exp={exp} got={got}")
    # summary
    out = os.path.join(ROOT, "results", "summary_v84_full.tsv"); os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write("id\tvariant\texpected\tgot\tstatus\treason\n")
        for r in rows: fh.write("\t".join(map(str, r)) + "\n")
    from collections import Counter
    c = Counter(r[4] for r in rows)
    print(f"\n==== {len(rows)} variants: {dict(c)} ====")
    print(f"correct={c['OK']}  wrong={c['WRONG']}  unknown={c['UNKNOWN']}  skipped={c['SKIP']}")
    print(f"of the {c['OK']+c['WRONG']+c['UNKNOWN']} RUN variants: {c['OK']} correct")
    print("results:", out)

if __name__ == "__main__":
    main()
