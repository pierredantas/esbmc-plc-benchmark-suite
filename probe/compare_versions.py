#!/usr/bin/env python3
"""Run the same tasks through two ESBMC builds and report where they disagree.

  compare_versions.py --a <esbmc-A> --b <esbmc-B> [--label-a v8.4] [--label-b master]

Covers the probe pack (front-end behaviour) and every graphical LD benchmark in
the suite (verdict drift between versions).
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import tempfile

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHDOG = ["--ld-scan-watchdog", "--ld-scan-budget", "8"]


def iec_to_c(expr):
    """v8.4 and master both parse C operators only; run_v84.py does the same."""
    expr = re.sub(r"\bAND\b", "&&", expr)
    expr = re.sub(r"\bOR\b", "||", expr)
    return re.sub(r"\bNOT\s*", "!", expr)


def translate_props(props, out_path):
    """Emit a property file both builds accept, or None if nothing is checkable."""
    lines, n = ["properties:"], 0
    for p in props.get("properties", []):
        if p["kind"] == "mutual_exclusion":
            n += 1
            lines += [f"  - id: P{n}", "    kind: mutual_exclusion",
                      f"    variables: [{', '.join(p['variables'])}]"]
        elif p["kind"] == "invariant":
            n += 1
            lines += [f"  - id: P{n}", "    kind: invariant",
                      f'    expression: "{iec_to_c(p["expression"])}"']
    if not n:
        return None
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return out_path


def verdict(esbmc, program, props_path, expected, timeout=120):
    """Run one task and return (verdict, gate)."""
    mode = ["--k-induction"] if expected else ["--incremental-bmc", "--unwind", "20"]
    args = [esbmc, program, "--ld-props", props_path, *mode, *WATCHDOG,
            "--timeout", f"{timeout}s"]
    out = subprocess.run(args, capture_output=True, text=True, check=False)
    txt = (out.stdout or "") + (out.stderr or "")
    if re.search(r"verification successful", txt, re.I):
        v = "SAFE"
    elif re.search(r"verification failed", txt, re.I):
        v = "VIOL"
    elif re.search(r"PARSING ERROR|CONVERSION ERROR", txt):
        v = "error"
    else:
        v = "unknown"
    dump = subprocess.run([esbmc, program, "--goto-functions-only"],
                          capture_output=True, text=True, check=False)
    asg = re.findall(r"^\s+ASSIGN (\S+)\s*=", (dump.stdout or "") + (dump.stderr or ""), re.M)
    counts = {}
    for name in asg:
        counts[name] = counts.get(name, 0) + 1
    return v, counts


def tasks():
    """Yield (id, program_xml, props_dict, expected) for every graphical benchmark."""
    for bp in sorted(glob.glob(os.path.join(ROOT, "benchmarks", "**", "benchmark.yml"),
                               recursive=True)):
        with open(bp, encoding="utf-8") as fh:
            b = yaml.safe_load(fh)
        d = os.path.dirname(bp)
        pp = os.path.normpath(os.path.join(d, b.get("properties_file", "props.yaml")))
        with open(pp, encoding="utf-8") as fh:
            props = yaml.safe_load(fh)
        for v in b["variants"]:
            if v["file"].endswith(".xml"):
                yield (f"{b['id']}/{v['file']}", os.path.join(d, v["file"]),
                       props, bool(v["expected_verdict"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--label-a", default="A")
    ap.add_argument("--label-b", default="B")
    args = ap.parse_args()

    tmp = tempfile.mkdtemp()
    rows, diffs = [], []
    for tid, xml, props, expected in tasks():
        ppath = translate_props(props, os.path.join(tmp, "p.yaml"))
        if ppath is None:
            continue
        ld = os.path.join(tmp, "t.ld")
        shutil.copyfile(xml, ld)
        va, ca = verdict(args.a, ld, ppath, expected)
        vb, cb = verdict(args.b, ld, ppath, expected)
        exp = "SAFE" if expected else "VIOL"
        rows.append((tid, exp, va, vb, ca, cb))
        if va != vb:
            diffs.append((tid, exp, va, vb, ca, cb))

    print(f"{'task':46} {'expect':7} {args.label_a:9} {args.label_b:9} encoding")
    print("-" * 96)
    for tid, exp, va, vb, ca, cb in rows:
        na, nb = sum(ca.values()), sum(cb.values())
        mark = "  <-- DIFFERS" if va != vb else ("  (encoding changed)" if na != nb else "")
        print(f"{tid:46} {exp:7} {va:9} {vb:9} {na:2} -> {nb:2}{mark}")
    print()
    print(f"{len(rows)} task(s); {len(diffs)} verdict difference(s); "
          f"{sum(1 for r in rows if sum(r[4].values()) != sum(r[5].values()))} encoding change(s)")


if __name__ == "__main__":
    main()
