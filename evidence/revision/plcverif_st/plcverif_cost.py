#!/usr/bin/env python3
"""Wall time and peak memory of every PLCverif run in the paper (137 variants), five repetitions each (R1.2).

Ladder variants replay the October 23 command lines recorded in the PLCverif logs; structured-text variants
use the SCL of plcverif_st.py. /usr/bin/time -l gives the peak resident set of the PLCverif JVM; a wrapper
around NuSMV gives the peak of the model-checker process separately.

    plcverif_cost.py OUT JAVA PLCVERIF NUSMV REPS [NAME ...]
"""
import csv, glob, json, os, pathlib, re, statistics as st, subprocess, sys, time

RES = pathlib.Path("/Users/user/Claude/5_ESBMC-PLC Toolkit/ESBMC_PLC/results")
HERE = pathlib.Path(__file__).resolve().parent
EV = HERE.parent


def core_names():
    return {f"{v['id']}__{v['file'].split('.')[0]}": v for v in csv.DictReader(open(EV / "variants_302.csv"))
            if v["core_suite"] == "yes"}


def ladder_jobs(core):
    jobs = {}
    for d in ("bool", "counters", "rest", "timers"):
        for log in sorted((RES / f"plcverif-{d}-2026-10-23" / "logs").glob("*.log")):
            if ".convert" in log.name:
                continue
            line = next((l for l in log.read_text(errors="replace").splitlines() if l.startswith("Arguments:")), None)
            if not line:
                continue
            parts = re.split(r"  (?=-)", line[len("Arguments:"):].strip())
            ident = next(p[4:] for p in parts if p.startswith("-id="))
            if ident in core and core[ident]["lang"].startswith("LD"):
                jobs[ident] = parts
    return jobs


def st_jobs(core, scl_dir):
    jobs = {}
    for scl in sorted(pathlib.Path(scl_dir).glob("*.scl")):
        ident = scl.stem
        text = scl.read_text()
        entry = re.search(r"FUNCTION_BLOCK\s+(\w+)", text).group(1)
        parts = [f"-id={ident}", "-job=verif", "-lf=step7", f"-sourcefiles.0={scl}"]
        i = 1
        if re.search(r"\b(TON|TOF|TP)\b", text):
            parts.append(f"-sourcefiles.{i}={RES / 'plcverif-timers-2026-10-23' / 'builtin.scl'}"); i += 1
        if re.search(r"\b(CTU|CTD|R_TRIG|F_TRIG)\b", text):
            parts.append(f"-sourcefiles.{i}={RES / 'plcverif-counters-2026-10-23' / 'iec_blocks.scl'}")
        parts += [f"-lf.entry={entry}", "-job.backend=nusmv", "-job.backend.binary_path=X", "-job.backend.timeout=120",
                  "-job.req=assertion", "-job.reporters.0=plaintext", "-output=X"]
        jobs[ident] = parts
    return jobs


def main():
    out, java, plcverif, nusmv, reps = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    only = set(sys.argv[6:])
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    memlog = out / "nusmv_rss.log"
    wrapper = out / "nusmv_mem.sh"
    wrapper.write_text(f'#!/bin/bash\nT=$(mktemp)\n/usr/bin/time -l -o "$T" "{nusmv}" "$@"\nrc=$?\n'
                       f'awk \'/maximum resident set size/{{print $1}}\' "$T" >> "{memlog}"\nrm -f "$T"\nexit $rc\n')
    wrapper.chmod(0o755)
    launcher = next((plcverif / "plugins").glob("org.eclipse.equinox.launcher_*.jar")).as_posix()
    core = core_names()
    jobs = {**ladder_jobs(core), **st_jobs(core, HERE / "scl")}
    results = {}
    for ident, parts in sorted(jobs.items()):
        if only and ident not in only:
            continue
        args = []
        for p in parts:
            if p.startswith("-job.backend.binary_path="):
                p = f"-job.backend.binary_path={wrapper}"
            elif p.startswith("-output="):
                p = f"-output={out / 'work' / ident}"
            args.append(p)
        runs = []
        for _ in range(reps):
            memlog.write_text("")
            t0 = time.perf_counter()
            r = subprocess.run(["/usr/bin/time", "-l", java, "-jar", launcher, *args], cwd=plcverif,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            wall = time.perf_counter() - t0
            jvm = int(re.search(r"(\d+)\s+maximum resident set size", r.stderr).group(1))
            nu = [int(x) for x in memlog.read_text().split()]
            res = re.findall(r"requirement is (SATISFIED|VIOLATED|[A-Z]+)",
                             pathlib.Path(out, "work", ident, f"{ident}.report.txt").read_text(errors="replace")
                             if pathlib.Path(out, "work", ident, f"{ident}.report.txt").exists() else r.stdout)
            runs.append(dict(wall=round(wall, 3), jvm_mib=round(jvm / 1048576, 1),
                             nusmv_mib=round(max(nu) / 1048576, 1) if nu else None, result=res[0] if res else None))
        results[ident] = runs
        print(ident, runs[0], flush=True)
    json.dump(results, open(out / "cost.json", "w"), indent=1)


if __name__ == "__main__":
    main()
