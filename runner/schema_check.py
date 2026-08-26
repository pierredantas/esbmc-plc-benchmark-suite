#!/usr/bin/env python3
"""Validate every PLCopen XML program against the official TC6 schema.

Well-formed XML is not the same as a file a real engineering tool will open. This
checks structure against PLCopen's own XSD, which is what an importer validates
against, so a program that passes here is one another vendor's tool has a fair
chance of reading.

    schema_check.py [path ...]        # default: benchmarks/, demo/, demo2/

The schema is not vendored. It is fetched once into ~/.cache/plcopen and reused,
because redistributing PLCopen's XSD is their call rather than ours.

Programs here declare the tc6_0200 namespace while the published schema targets
tc6_0201. The element vocabulary is the same, so validation rewrites the namespace
in memory rather than editing the files.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import urllib.request

XSD_URL = "https://raw.githubusercontent.com/beremiz/beremiz/master/plcopen/tc6_xml_v201.xsd"
CACHE = pathlib.Path(os.path.expanduser("~/.cache/plcopen/tc6_xml_v201.xsd"))
DEFAULTS = ["benchmarks", "demo", "demo2"]


def schema_path():
    """The TC6 XSD, downloaded on first use."""
    if CACHE.exists() and CACHE.stat().st_size > 10000:
        return CACHE
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(XSD_URL, timeout=60) as resp:
        CACHE.write_bytes(resp.read())
    return CACHE


def programs(roots):
    """Every XML program under the given roots.

    Files without the PLCopen namespace are included rather than skipped. A
    document that omits it is not PLCopen XML as far as a conforming importer is
    concerned, however much it looks like one, and silently passing over such a
    file would hide the very thing this check exists to find.
    """
    out = []
    for root in roots:
        for path in sorted(pathlib.Path(root).rglob("*")):
            if path.suffix in (".xml", ".ld") and _head(path).lstrip().startswith("<?xml"):
                out.append(path)
    return out


def _head(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:2000]
    except OSError:
        return ""


def validate(path, xsd, tmp):
    """Run xmllint against the schema and return the first validity error."""
    text = path.read_text(encoding="utf-8")
    if "plcopen.org/xml" not in text[:2000]:
        return "no PLCopen namespace: an importer will not recognise this as PLCopen XML"
    text = text.replace("tc6_0200", "tc6_0201")
    tmp.write_text(text, encoding="utf-8")
    out = subprocess.run(["xmllint", "--noout", "--schema", str(xsd), str(tmp)],
                         capture_output=True, text=True, check=False)
    if out.returncode == 0:
        return None
    for line in out.stderr.splitlines():
        if "validity error" in line:
            msg = line.split("validity error : ", 1)[-1]
            return re.sub(r"\{[^}]*\}", "", msg).strip()
    return out.stderr.strip().splitlines()[0] if out.stderr else "unknown failure"


def main():
    """Report one line per program and exit non-zero if any fails."""
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*", default=DEFAULTS)
    ap.add_argument("-q", "--quiet", action="store_true", help="only list failures")
    args = ap.parse_args()

    xsd = schema_path()
    tmp = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "plcopen_schema_check.xml"
    failures = 0
    paths = programs(args.roots or DEFAULTS)
    for path in paths:
        err = validate(path, xsd, tmp)
        if err:
            failures += 1
            print(f"FAIL {path}\n       {err[:110]}")
        elif not args.quiet:
            print(f"OK   {path}")
    print(f"\n{len(paths)} program(s) checked, {failures} failed schema validation.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
