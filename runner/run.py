#!/usr/bin/env python3
"""Benchmark suite runner (skeleton). For each (benchmark variant, tool), invoke the tool adapter,
map its output to {true,false,unknown}, compare to expected_verdict, and record a
result JSON. Honest-coverage rule: an unsupported input format is recorded as
status=error/reason=unsupported_format, never silently dropped.

This is a contract stub — adapters under runner/adapters/ are not yet wired to real tools.
"""
import sys, os, glob, json, time
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = {"esbmc-plc+": "esbmc_plc", "plcverif": "plcverif", "nuxmv": "nuxmv"}


def classify(expected, verdict):
    if verdict == "unknown":
        return "unknown"
    got = (verdict == "true")
    return "correct" if got == expected else "wrong"


def run(tool, bench_dir, out_dir):
    bench = yaml.safe_load(open(os.path.join(bench_dir, "benchmark.yml")))
    # adapter = importlib.import_module(f"adapters.{TOOLS[tool]}")   # TODO wire real tools
    for v in bench["variants"]:
        rec = {
            "benchmark": bench["id"], "variant": v["file"], "tool": tool,
            "expected": "true" if v["expected_verdict"] else "false",
            "verdict": "unknown", "status": "error", "reason": "adapter_not_implemented",
            "cpu_time_s": None, "mem_mb": None, "witness_valid": None,
        }
        # verdict = adapter.run(os.path.join(bench_dir, v["file"]), bench, timeout=900, mem_gb=15)
        # rec["verdict"] = verdict; rec["status"] = classify(v["expected_verdict"], verdict)
        os.makedirs(os.path.join(out_dir, tool), exist_ok=True)
        json.dump(rec, open(os.path.join(out_dir, tool, f"{bench['id']}__{v['file']}.json"), "w"), indent=2)
        print(f"[{tool}] {bench['id']}/{v['file']}: {rec['status']} ({rec['reason']})")


def main():
    tool = sys.argv[1] if len(sys.argv) > 1 else "esbmc-plc+"
    assert tool in TOOLS, f"unknown tool {tool}; choose from {list(TOOLS)}"
    out_dir = os.path.join(ROOT, "results")
    for bp in glob.glob(os.path.join(ROOT, "benchmarks", "**", "benchmark.yml"), recursive=True):
        run(tool, os.path.dirname(bp), out_dir)


if __name__ == "__main__":
    main()
