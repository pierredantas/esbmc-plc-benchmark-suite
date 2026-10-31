"""Mutation check of the properties of the 12 standard-anchored programs (R2.4).

Single-fault mutants of each program (graphical: flip one contact, swap one set/reset coil; structured text: change
one AND, OR, NOT, TRUE, or FALSE) are checked against the benchmark's own properties and its discriminator
properties. A mutant is killed when a property is violated. Graphical programs run on ESBMC 8.6 (ladder front end),
structured text on PLCverif.

    mutation_check.py SUITE ESBMC JAVA PLCVERIF NUSMV BUILTIN_SCL IEC_BLOCKS_SCL OUT
"""
import glob, json, pathlib, re, subprocess, sys, tempfile
import yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "plcverif_st"))
import plcverif_st as pv  # noqa: E402

suite, esbmc, java, cli, nusmv, builtin, blocks, out = sys.argv[1:9]
MUT_DIR = pathlib.Path(sys.argv[9]) if len(sys.argv) > 9 else None
if MUT_DIR:
    MUT_DIR.mkdir(parents=True, exist_ok=True)
IDS = "g_burner_purge g_door_reversal g_estop_reset g_guard_lock g_phase_hold_permissive g_two_hand g_two_hand_fb st_burner_purge st_door_reversal st_estop_reset st_guard_lock st_two_hand".split()
FLAGS = ["--k-induction", "--ld-scan-watchdog", "--ld-scan-budget", "8", "--ld-sound-mode", "--timeout", "60s"]


def esbmc_verdict(xml_text, props_path):
    with tempfile.NamedTemporaryFile("w", suffix=".ld", delete=False) as f:
        f.write(xml_text); name = f.name
    r = subprocess.run([esbmc, name, "--ld-props", str(props_path), *FLAGS], capture_output=True, text=True)
    o = r.stdout + r.stderr
    return "SAFE" if "VERIFICATION SUCCESSFUL" in o else "VIOLATION" if "VERIFICATION FAILED" in o else "unknown"


def pv_verdict(st_text, props_path, tag):
    props = yaml.safe_load(open(props_path))["properties"]
    try:
        scl, entry, uses = pv.convert(st_text, props)
    except ValueError:
        return "unknown"
    d = pathlib.Path(tempfile.mkdtemp()); f = d / "p.scl"; f.write_text(scl)
    files = [str(f)] + ([builtin] if uses & {"TON", "TOF", "TP"} else []) + ([blocks] if uses & {"CTU", "CTD", "R_TRIG", "F_TRIG"} else [])
    res, _, _ = pv.run_plcverif(java, cli, nusmv, files, entry, tag, str(d / "out"))
    return {"SATISFIED": "SAFE", "VIOLATED": "VIOLATION"}.get(res[0] if res else "", "unknown")


def varname(t, pos):
    m = re.search(r"<variable>([^<]*)</variable>", t[pos:pos + 600])
    return m.group(1) if m else "?"


def feeds(t):
    """For each contact element (by localId): the names of the coils its output reaches."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(re.sub(r"<\?xml[^>]*\?>", "", t).strip())
    nodes, consumers = {}, {}
    for e in root.iter():
        if e.get("localId"):
            nodes[int(e.get("localId"))] = e
    for e in nodes.values():
        for c in e.iter():
            if c.tag.split("}")[-1] == "connection" and c.get("refLocalId"):
                consumers.setdefault(int(c.get("refLocalId")), set()).add(int(e.get("localId")))
    out = {}
    for i, e in nodes.items():
        if e.tag.split("}")[-1] != "contact":
            continue
        seen, stack, coils = set(), [i], []
        while stack:
            x = stack.pop()
            for y in consumers.get(x, ()):
                if y in seen:
                    continue
                seen.add(y)
                if nodes[y].tag.split("}")[-1] == "coil":
                    coils.append(nodes[y].findtext("{*}variable") or "?")
                else:
                    stack.append(y)
        out[i] = ", ".join(sorted(set(coils))) or "no coil"
    return out


def xml_mutants(t):
    fmap = feeds(t)
    for m in re.finditer(r"<contact\b[^>]*>", t):
        tag = m.group(0)
        lid = re.search(r'localId="(\d+)"', tag)
        feed = fmap.get(int(lid.group(1)), "?") if lid else "?"
        neg = re.search(r'negated="(true|false)"', tag)
        if neg:
            flip = "false" if neg.group(1) == "true" else "true"
            new = tag[:neg.start(1)] + flip + tag[neg.end(1):]
            yield f"contact {varname(t, m.end())} (feeds {feed}) negated {neg.group(1)}->{flip}", t[:m.start()] + new + t[m.end():]
        else:
            new = tag[:-1] + ' negated="true">'
            yield f"contact {varname(t, m.end())} (feeds {feed}) negated false->true", t[:m.start()] + new + t[m.end():]
    for m in re.finditer(r'(<coil\b[^>]*storage=")(set|reset)(")', t):
        flip = "reset" if m.group(2) == "set" else "set"
        yield f"coil {varname(t, m.end())} storage {m.group(2)}->{flip}", t[:m.start(2)] + flip + t[m.end(2):]


def cdata_mutants(t):
    for m in re.finditer(r"<!\[CDATA\[(.*?)\]\]>", t, re.S):
        for desc, mt in st_mutants(m.group(1)):
            yield "ST body: " + desc, t[:m.start(1)] + mt + t[m.end(1):]


def st_mutants(t):
    code = re.sub(r"\(\*.*?\*\)", lambda m: " " * len(m.group(0)), t, flags=re.S)
    start = code.find("END_VAR")
    start = code.rfind("END_VAR") + 7 if start >= 0 else 0
    for pat, rep in ((r"\bAND\b", "OR"), (r"\bOR\b", "AND"), (r"\bNOT\b ?", ""), (r"\bTRUE\b", "FALSE"), (r"\bFALSE\b", "TRUE")):
        for m in re.finditer(pat, code[start:]):
            a, b = start + m.start(), start + m.end()
            line = t[t.rfind("\n", 0, a) + 1:t.find("\n", a)].strip()[:90]
            yield f"{m.group(0).strip()} -> {rep or '(removed)'} in: {line}", t[:a] + rep + (" " if rep == "" else "") + t[b:]


results = {}
for bid in IDS:
    d = pathlib.Path(next(glob.iglob(f"{suite}/benchmarks/*/{bid}")))
    main = d / "props.yaml"
    discs = sorted(d.glob("*.props.yaml"))
    base = next((d / n for n in ("program.xml", "clean.xml") if (d / n).exists()), None) or next(f for f in sorted(d.iterdir()) if f.suffix == ".st")
    t = base.read_text()
    if base.suffix == ".xml":
        verdict = lambda text, props, tag: esbmc_verdict(text, props)
        muts = list(xml_mutants(t)) + list(cdata_mutants(t))
    else:
        verdict = lambda text, props, tag: pv_verdict(text, props, tag)
        muts = list(st_mutants(t))
    b_main = verdict(t, main, bid + "_b")
    b_disc = {p.name: verdict(t, p, bid + "_bd") for p in discs}
    rec = dict(base=base.name, base_main=b_main, base_disc=b_disc, mutants=len(muts), killed_main=0, killed_disc_only=0, survivors=[])
    for i, (desc, mt) in enumerate(muts):
        v = verdict(mt, main, f"{bid}_m{i}")
        if v == "VIOLATION":
            rec["killed_main"] += 1
            continue
        dv = {p.name: verdict(mt, p, f"{bid}_m{i}d") for p in discs}
        if any(dv[k] != b_disc[k] for k in dv):
            rec["killed_disc_only"] += 1
        else:
            rec["survivors"].append(dict(mutant=desc, verdict_main=v))
            if MUT_DIR:
                (MUT_DIR / f"{bid}_S{len(rec['survivors'])}{base.suffix}").write_text(mt)
    results[bid] = rec
    print(bid, {k: v for k, v in rec.items() if k != "survivors"}, "survivors", len(rec["survivors"]), flush=True)
json.dump(results, open(out, "w"), indent=1)
print("FINISHED", flush=True)
