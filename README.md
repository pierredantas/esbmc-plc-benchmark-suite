# IEC 61131-3 Formal Verification Benchmark Suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21642385.svg)](https://doi.org/10.5281/zenodo.21642385)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-blue.svg)](LICENSE)
[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE-CODE)

A community suite of IEC 61131-3 benchmarks across **10 industrial domains**, written in all
five languages of the standard and carried as PLCopen XML or plain text, each with formal
safety properties (YAML), machine-checkable expected verdicts, witnesses, and baseline results
from ESBMC-PLC+ and nuXmv. SV-COMP–compatible so the artifact feeds a future SV-COMP PLC/ICS
category.

**[Read it as a course](https://pierredantas.github.io/esbmc-plc-benchmark-suite/)** —
thirty-two lessons in six parts, each built on one program and the runs recorded against
it. Nothing on that site runs live: every verdict, scan body and counterexample came out
of a command printed beside it, and its counts are tallied from `results/records/` when
the pages are built.

This repository is the reproducibility artifact for:

> P. Dantas, L. C. Cordeiro, W. Junior. *A Benchmark Suite and Ground-Truth Methodology for
> Formal Verification of IEC 61131-3 Ladder Diagram Programs.* Under review, **Scientific
> Reports**, 2026.

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
runner/schema_check.py         PLCopen TC6 XSD validation via xmllint
runner/build_index.py          regenerates docs/INDEX.md; --check fails on drift
runner/record.py               one recorded run through ESBMC's LD front end
runner/record_via_c.py         the same question through Beremiz -> MatIEC -> C
runner/record_all.py           drives either route over the whole catalog
runner/record_custom.py        the records whose names the catalog does not derive
results/records/*.json         one record per task: command, encoding, verdict, trace
site_src/                      portal sources; build.py renders them into portal/
docs/INTEROP.md                the second verification route and what it costs
```

## Status

> **Released version and working tree differ.** The archived release **v1.0.1**
> ([DOI 10.5281/zenodo.21642386](https://doi.org/10.5281/zenodo.21642386)) holds
> **50 benchmarks over 83 program variants** in 15 LD-textual, 25 LD-graphical and
> 10 ST. Those are the numbers the accompanying paper reports, and they are what you
> should cite. This branch has grown since, and its size changes with every benchmark
> added, so no count for it is written here. For current figures read the
> [benchmarks catalog](https://pierredantas.github.io/esbmc-plc-benchmark-suite/benchmarks/)
> or `docs/INDEX.md`; both derive their counts from `benchmarks/` at build time.
> Everything below this note describes v1.0.1.

50 benchmarks / 83 variants across 10 domains, all passing `runner/validate.py`.
Composition: **15 LD-textual · 25 LD-graphical · 10 ST**.
Verdicts: 49 SAFE / 34 VIOLATION. Ground truth: 36 expert · 29 fault-injection · 18 cross-tool-consensus.
Difficulty: 26 easy · 18 medium · 6 hard. Note that `docs/INDEX.md` now lists the
working tree rather than this release, since it is generated from `benchmarks/`.

### Validation status of expected verdicts
Each benchmark records a `validation_status` field: `validated` (tool-confirmed) or `candidate`.

* **31 validated** — the 25 graphical benchmarks (ESBMC-PLC+, 15 of them also confirmed by
  nuXmv) and the 6 semantics-independent textual-LD benchmarks (Boolean and edge/latch logic,
  confirmed by nuXmv).
* **19 candidates** — the 9 timer/counter/latch feature benchmarks, whose verdicts are
  *semantics-dependent* (a standard timer's verdict can change across tools' scan-cycle timing
  models), and the 10 Structured-Text programs, whose non-termination and multi-POU structure
  are not yet encoded for a second checker. These are flagged so that no result depends on an
  unconfirmed label; confirming them follows the porting protocol in `docs/`.

### Known limitations
`water_treatment` is over-represented (16/50) because SWaT and PLC-LD, the two richest public
ICS corpora, are both in the water domain; results are reported per domain so they can be
reweighted. Five benchmarks are textual/graphical syntax-coverage pairs (same logic, two
encodings), labelled via `syntax_pair_of` and counted once per language slice.

**ESBMC OR-branch coil bug** ([esbmc/esbmc#7577](https://github.com/esbmc/esbmc/issues/7577)):
ESBMC's LD front end does not OR-combine a coil driven by more than one parallel branch — it
compiles the branches as sequential overwrites instead, so only the last one in document order
has any effect. This silently breaks any seal-in/latch coil (`Q := S OR (Q AND NOT R)`) and any
plain OR gate wired as two branches into one coil. Every benchmark using either idiom is
tagged `known-issue-esbmc-7577` and carries `validation_status: candidate` rather than
`validated` until the upstream fix lands, whatever its prior status said — a tool-confirmed
verdict on one of these was never actually sound. Check a task's tags before trusting its
expected verdict as tool-confirmed.

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

## Contributing

`main` is protected: the `validate` job has to pass before a commit lands there. It runs
the schema check, the PLCopen TC6 check, and `runner/build_index.py --check`, so a
benchmark added without regenerating `docs/INDEX.md` is rejected rather than merged.

Run the same three checks before pushing:

```bash
python3 runner/validate.py
python3 runner/schema_check.py      # needs xmllint
python3 runner/build_index.py       # regenerate the index if you changed benchmarks/
```

## License
Property files, witnesses, documentation, and every program authored for this suite are
released under **CC-BY-4.0** (see [`LICENSE`](LICENSE)). The schema, validator, runner, and
adapters are released under the **MIT License** (see [`LICENSE-CODE`](LICENSE-CODE),
inherited from ESBMC).

Imported programs keep their upstream license, declared per program in `benchmark.yml`
(`source.license`). Sixteen are **GPL-3.0**: the eight `g_tank_*` and six `st_swat_*`
programs from PLC-LD-dataset and PLC_Defuser (both published by UniboSecurityResearch),
plus `g_start_cycle` and `g_stop_eq`, also from PLC-LD-dataset. Five are
**GPL-2.0-or-later**: the `*_counter_reset` cross-language set and
`g_traffic_light_pedestrian`, both from Beremiz. Redistributing those carries the GPL
obligation rather than CC-BY-4.0. Check `source.license` before reusing a program, and
note that redistribution-restricted programs use `link-only` with a URL instead of a
bundled file.

## Citation
Please cite both the paper and the archived artifact.

```bibtex
@dataset{dantas2026suite,
  title     = {A Benchmark Suite and Ground-Truth Methodology for Formal Verification
               of {IEC} 61131-3 Ladder Diagram Programs},
  author    = {Dantas, Pierre and Cordeiro, Lucas C. and Junior, Waldir},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0.1},
  doi       = {10.5281/zenodo.21642385}
}
```

```bibtex
@article{dantas2026benchmark,
  title   = {A Benchmark Suite and Ground-Truth Methodology for Formal Verification
             of {IEC} 61131-3 Ladder Diagram Programs},
  author  = {Dantas, Pierre and Cordeiro, Lucas C. and Junior, Waldir},
  journal = {Scientific Reports},
  year    = {2026},
  note    = {Under review}
}
```
