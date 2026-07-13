# IEC 61131-3 Formal Verification Benchmark Suite

A community suite of **50 IEC 61131-3 programs** (25 textual LD · 20 graphical LD · 5 ST)
across **10 industrial domains**, in PLCopen XML / ST, each with formal safety properties
(YAML), machine-checkable expected verdicts, and baseline results from ESBMC-PLC+, PLCverif,
and nuXmv. SV-COMP–compatible so the artifact feeds a future SV-COMP PLC/ICS category.

Accompanying artifact for a manuscript under review; baseline results are produced with ESBMC-PLC, PLCverif, and nuXmv.

## Layout
```
SUITE.yml                      top-level manifest (domains, composition, index)
docs/format_spec.md            the format & schema specification (v0.1)
docs/selection_50.md           the finalized 50-program selection
schema/*.json                  JSON-Schema validators for benchmark.yml and props.yaml
benchmarks/<domain>/<id>/      one directory per benchmark task
  ├── benchmark.yml            metadata + variants + expected verdicts + ground truth
  ├── props.yaml               formal properties (stable ids)
  ├── <variant>.st|.xml        program variant(s) — the system under test
  └── README.md                optional notes / provenance
runner/validate.py             schema + file + XML validation (CI gate)
runner/run.py                  tool-runner skeleton (adapters WIP)
results/<tool>/                per-run verdict/time/status records
```

## Status — all 50 benchmarks assembled (2026-07-09)
50 benchmarks / 83 variants across 10 domains, all passing `runner/validate.py`.
Composition matches target: **15 LD-textual · 25 LD-graphical · 10 ST**.
Verdicts: 49 SAFE / 34 VIOLATION. Ground truth: 36 expert · 29 fault-injection · 18 cross-tool-consensus.
Difficulty: 26 easy · 18 medium · 6 hard. Full list in `docs/INDEX.md`.

**Pending confirmation:** the ~14 hand-authored graphical XML files and all inferred/derived
properties have NOT yet been run through the real ESBMC-GraphPLC frontend (no binary in the
authoring environment). They use only corpus-proven LD constructs and validate structurally,
but the expected verdicts must be confirmed with `esbmc --ld-props` before publication.
Two honest caveats for the paper: `water_treatment` is over-represented (16/50 — SWaT and
PLC-LD, the abundant real ICS corpora, are both water); and 9 benchmarks are textual/graphical
syntax-coverage pairs (same logic, two encodings), labelled via `syntax_pair_of`.

## Validate
```
pip3 install pyyaml jsonschema
python3 runner/validate.py            # whole suite
python3 runner/validate.py benchmarks/motor_control/motor_interlock
```

## Ground truth
Expected verdicts are established by `expert` proof/audit, `cross-tool-consensus`, or
`fault-injection` (a mutant of a known-SAFE base with a documented seeded defect and
witness). ~24 of the 50 tasks arrive with fault-injection pairs.

## License
Code MIT (inherited from ESBMC); benchmarks and container CC-BY-4.0. Per-program licenses
are declared in each `benchmark.yml` (`source.license`); redistribution-restricted programs
use `link-only` with a URL instead of a bundled file.
