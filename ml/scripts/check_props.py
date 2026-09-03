#!/usr/bin/env python3
"""Deterministic sanity check for a generated props.yaml against its source program.

The fine-tuned SLM can produce plausible-looking but wrong output: real
variable names combined into a relationship the program's logic doesn't
support, a variable that does not exist in the program at all, or a
mutual_exclusion pair that is not actually a symmetric output-output pair
(the shape every mutual_exclusion example in the training corpus has). None
of these are caught by schema validation, since the schema only checks
structure, not whether the content is grounded in the program.

This is advisory, not a fixer: it flags for human review, it does not alter
the generated YAML.

    python3 ml/scripts/check_props.py path/to/program.st path/to/props.yaml
    python3 ml/scripts/generate_props.py program.st --domain X --language ST \\
      | python3 ml/scripts/check_props.py program.st -
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

_VAR_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_RESERVED = {
    "AND", "OR", "NOT", "XOR", "TRUE", "FALSE", "IF", "THEN", "ELSE", "ELSIF",
    "END_IF", "END_VAR", "END_PROGRAM", "PROGRAM", "VAR", "VAR_INPUT",
    "VAR_OUTPUT", "BOOL", "INT", "CONFIGURATION", "RESOURCE", "TASK", "AT",
}


def extract_declared_vars(source: str) -> dict[str, str]:
    """Map declared variable name -> 'input' | 'output' | 'other', across
    ST/IL (AT %IX/%QX, VAR_INPUT/VAR_OUTPUT blocks), LD-textual (XIC/OTE
    usage), and PLCopen XML (<inputVars>/<outputVars>)."""
    roles: dict[str, str] = {}

    for block, role in [("inputVars", "input"), ("outputVars", "output")]:
        m = re.search(rf"<{block}>(.*?)</{block}>", source, re.DOTALL)
        if m:
            for vm in re.finditer(r'<variable name="([^"]+)"', m.group(1)):
                roles[vm.group(1)] = role

    for m in re.finditer(r"(\w+)\s+AT\s+%([IQ])X", source):
        roles[m.group(1)] = "input" if m.group(2) == "I" else "output"

    for block, role in [("VAR_INPUT", "input"), ("VAR_OUTPUT", "output"), ("VAR", "other")]:
        for m in re.finditer(rf"\b{block}\b(.*?)END_VAR", source, re.DOTALL):
            for vm in re.finditer(r"(\w+)\s*(?:AT\s+%\w+)?\s*:\s*\w+", m.group(1)):
                name = vm.group(1)
                roles.setdefault(name, role)

    for m in re.finditer(r"(?:XIC|XIO)\((\w+)\)", source):
        roles.setdefault(m.group(1), "input")
    for m in re.finditer(r"OTE\((\w+)\)", source):
        roles[m.group(1)] = "output"

    return roles


def extract_property_vars(prop: dict) -> set[str]:
    if prop.get("variables"):
        return set(prop["variables"])
    expr = prop.get("expression", "")
    tokens = set(_VAR_TOKEN.findall(expr)) - _RESERVED
    return tokens


def check(source: str, props_text: str) -> list[str]:
    findings = []
    declared = extract_declared_vars(source)
    declared_names = set(declared.keys())

    try:
        obj = yaml.safe_load(props_text)
    except yaml.YAMLError as e:
        return [f"props.yaml is not valid YAML: {e}"]

    if not isinstance(obj, dict) or not isinstance(obj.get("properties"), list):
        return ["props.yaml has no top-level 'properties' list"]

    for prop in obj["properties"]:
        if not isinstance(prop, dict):
            continue
        pid = prop.get("id", "?")
        used = extract_property_vars(prop)
        unknown = used - declared_names
        if unknown:
            findings.append(
                f"{pid}: references variable(s) not declared in the source program: {sorted(unknown)}"
            )

        if prop.get("kind") == "mutual_exclusion":
            vars_ = prop.get("variables", [])
            roles = [declared.get(v, "unknown") for v in vars_]
            if roles and not all(r == "output" for r in roles):
                findings.append(
                    f"{pid}: mutual_exclusion over {vars_} — not all declared as outputs "
                    f"(roles: {dict(zip(vars_, roles))}); every mutual_exclusion example in "
                    f"the training corpus is a symmetric output-output pair, this may be a "
                    f"cause-effect pair mislabeled as mutual_exclusion"
                )

    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source_file")
    ap.add_argument("props_file", help="path to a props.yaml, or '-' to read from stdin")
    args = ap.parse_args()

    source = Path(args.source_file).read_text()
    props_text = sys.stdin.read() if args.props_file == "-" else Path(args.props_file).read_text()

    findings = check(source, props_text)
    if not findings:
        print("OK: no issues found")
        return 0

    print(f"FLAGGED: {len(findings)} issue(s)")
    for f in findings:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
