"""Build the review packet for the 12 standard-anchored programs (R2.4).

For each program the packet holds: the clause as the descriptor states it, the safety intent, the program text (and,
for graphical programs, a mechanical rendering of the coils as Boolean equations), the property and any
discriminator, and the mutants that no property kills. The reviewer answers two CSV files: one row per program and
one row per surviving mutant.

    make_packet.py SUITE_BENCHMARKS_DIR
"""
import csv
import glob
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

import yaml

HERE = pathlib.Path(__file__).resolve().parent
suite = sys.argv[1]
mut = json.load(open(HERE.parent / "mutation_results.json"))
nm = lambda e: e.tag.split("}")[-1]  # noqa: E731


def equations(path):
    """Coil := expression for a graphical program, read mechanically from the PLCopen XML."""
    root = ET.parse(path).getroot()
    lines = []
    for pou in root.iter():
        if nm(pou) != "pou":
            continue
        body = next((c for c in pou if nm(c) == "body"), None)
        ld = [x for x in body.iter() if nm(x) in ("LD", "FBD")] if body is not None else []
        if not ld:
            continue
        nodes = {int(e.get("localId")): e for e in ld[0].iter() if e.get("localId")}
        srcs = lambda e: [int(c.get("refLocalId")) for c in e.iter() if nm(c) == "connection"]  # noqa: E731

        def expr(i, seen=()):
            if i not in nodes or i in seen:
                return "TRUE"
            e = nodes[i]
            t = nm(e)
            if t == "leftPowerRail":
                return "TRUE"
            if t == "inVariable":
                return e.findtext("{*}expression") or "?"
            if t == "block":
                pins = []
                iv = next((c for c in e if nm(c) == "inputVariables"), None)
                for v in (iv if iv is not None else []):
                    ss = [expr(s, seen + (i,)) for s in srcs(v)]
                    pins.append(f"{v.get('formalParameter')}={' OR '.join(ss) if ss else 'FALSE'}")
                return f"{e.get('typeName')}({', '.join(pins)})"
            inc = " OR ".join(sorted({expr(s, seen + (i,)) for s in srcs(e)})) or "FALSE"
            if t == "contact":
                v = e.findtext("{*}variable")
                lit = f"NOT {v}" if e.get("negated") == "true" else v
                return lit if inc == "TRUE" else f"(({inc}) AND {lit})"
            return inc

        for e in nodes.values():
            if nm(e) == "coil":
                st = {"set": " [set]", "reset": " [reset]"}.get(e.get("storage"), "")
                lines.append(f"{pou.get('name')}: {e.findtext('{*}variable')}{st} := {expr(int(e.get('localId')))}")
    return "\n".join(lines)


fence = {".st": "iecst", ".xml": "xml"}
out_dir = HERE / "programs"
out_dir.mkdir(exist_ok=True)
for old in out_dir.glob("batch_*.md"):
    old.unlink()
ids = list(mut)
prog_rows, surv_rows = [], []
for n in range(0, len(ids), 6):
    chunk = ids[n:n + 6]
    parts = [f"# Batch {n // 6 + 1}: {', '.join(chunk)}\n"]
    for bid in chunk:
        d = pathlib.Path(glob.glob(f"{suite}/*/{bid}")[0])
        b = yaml.safe_load(open(d / "benchmark.yml"))
        base = d / mut[bid]["base"]
        props = yaml.safe_load(open(d / "props.yaml"))["properties"]
        discs = {p.name: yaml.safe_load(open(p))["properties"] for p in sorted(d.glob("*.props.yaml"))}
        text = base.read_text(errors="replace").rstrip()
        sec = [f"## {bid}\n",
               f"- Language: {b['language']}",
               f"- Clause cited by the descriptor: {b['source']['reference']}",
               f"- Safety intent: {b.get('safety_intent', '')}",
               "- Property (checked and holds): " + "; ".join(f"{p['id']}: {p.get('expression') or p.get('variables')}  ({p.get('justification', '')})" for p in props)]
        for dn, ps in discs.items():
            sec.append(f"- Discriminator `{dn}` (not a requirement; it separates a compliant program from a non-compliant one): "
                       + "; ".join(f"{p['id']}: {p.get('expression')}  ({p.get('justification', '')[:160]})" for p in ps)
                       + f"; on this program it is {mut[bid]['base_disc'].get(dn)}")
        sec.append(f"\nProgram `{base.name}`:\n\n```{fence.get(base.suffix, 'text')}\n{text}\n```\n")
        if base.suffix == ".xml":
            sec.append("The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):\n\n```\n" + equations(base) + "\n```\n")
        sec.append(f"Mutants that no property kills ({len(mut[bid]['survivors'])}):\n")
        for i, s in enumerate(mut[bid]["survivors"], 1):
            sec.append(f"- S{i}: {s['mutant']}")
            surv_rows.append([bid, f"S{i}", s["mutant"], "", ""])
        sec.append("")
        parts += sec
        prog_rows.append([bid, b["language"], "", "", "", "", ""])
    (out_dir / f"batch_{n // 6 + 1}.md").write_text("\n".join(parts))

with open(HERE / "answers_programs_template.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["benchmark", "language", "implements_cited_requirement", "requirements_considered",
                "requirements_not_covered", "confidence", "reasoning"])
    w.writerows(prog_rows)
with open(HERE / "answers_survivors_template.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["benchmark", "mutant_id", "mutant", "classification", "reasoning"])
    w.writerows(surv_rows)
print(len(prog_rows), "programs;", len(surv_rows), "surviving mutants;", len(list(out_dir.glob("batch_*.md"))), "batches")
