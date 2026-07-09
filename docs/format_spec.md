# P6 Benchmark Suite — Format & Schema Specification (v0.1 draft)

**Suite:** 50 IEC 61131-3 programs for formal verification of PLCs
**Goal of this spec:** a stable, SV-COMP-compatible layout so (a) every program is labeled
consistently, (b) any tool can be plugged in via an adapter, and (c) the artifact is
reproducible and citable. Evolves the existing `props.yaml` conventions (S1–S5, K-LD).

---

## 1. Directory layout

```
suite/
├── SUITE.yml                      # top-level manifest: version, license, domain list, index
├── schema/                        # JSON-Schema files that validate every descriptor & props file
│   ├── benchmark.schema.json
│   └── properties.schema.json
├── benchmarks/
│   └── <domain>/<benchmark-id>/
│       ├── benchmark.yml          # task descriptor: metadata + variants + expected verdicts
│       ├── props.yaml             # formal properties (your existing format, extended)
│       ├── <variant>.xml|.st|.ld  # one or more program variants (the SUT)
│       └── README.md              # optional human description + provenance notes
├── runner/
│   ├── run.py                     # harness: task -> tool adapter -> verdict compare
│   └── adapters/{esbmc_plc.py, plcverif.py, nuxmv.py}
└── results/
    └── <tool>/<benchmark-id>.json # per-run verdict, time, status
```

**Naming:** `benchmark-id = <domain>_<shortname>` (stable, lowercase, kebab/underscore),
e.g. `water_tank_overflow`, `manuf_ppu_scenario9`, `motor_star_delta`. IDs never change
once published (append, never rename).

---

## 2. `benchmark.yml` — task descriptor (one per benchmark)

Handles both the multi-variant case (S2: `clean.st` SAFE + `bomb.st` VIOLATION share one
`props.yaml`) and the single-program case (K-LD). SV-COMP `expected_verdict` compatible.

```yaml
format_version: "0.1"
id: motor_interlock                 # unique within suite
name: "Forward/reverse motor interlock"
domain: motor_control               # must be one of SUITE.yml domains
language: LD-textual                # LD-textual | LD-graphical | ST | FBD | SFC
source:
  origin: authored                  # authored | openplc | beremiz | ppu | swat | mathworks | controllino
  reference: "ESBMC-PLC-Sec S2"     # citation / URL / dataset name
  license: CC-BY-4.0                # redistribution license for THIS program
properties_file: props.yaml
variants:                           # ≥1 program file, each with its own expected verdict
  - file: clean.st
    expected_verdict: true          # true = SAFE (all properties hold)
    ground_truth:
      method: cross-tool-consensus  # expert | cross-tool-consensus | fault-injection
      confirmed_by: [esbmc-plc+, nuxmv]
  - file: bomb.st
    expected_verdict: false         # false = VIOLATION (≥1 property fails)
    violated_properties: [P2]       # ids from props.yaml
    ground_truth:
      method: fault-injection
      base_variant: clean.st
      seeded_defect: "Secret-knock sequence energises both contactors."
      witness: "IN sequence [1,0,1,1] reaches Motor_A AND Motor_B."
metrics:                            # auto-computed by an ingest script; see §5
  rungs: 6
  loc: 48
  pous: 1
  variables: 5
features: [contacts, coils, seal_in, comparison]   # controlled vocabulary, §4
difficulty: easy                    # easy | medium | hard | challenge
tags: [safety, interlock]           # free-form, optional
```

---

## 3. `props.yaml` — formal properties (extends your current format)

Backward-compatible superset of S1–S5 / K-LD. Every property gets a **stable `id`**
(referenced by `violated_properties`). Comments are no longer load-bearing.

```yaml
format_version: "0.1"
properties:
  - id: P1
    kind: mutual_exclusion          # closed vocabulary, §3.1
    variables: [Motor_A, Motor_B]
    justification: "Forward/reverse contactors must never be energised together."
  - id: P2
    kind: reachability
    expression: "Motor_A AND Motor_B"
    justification: "Witness recovers the secret-knock combination that detonates the bomb."
  - id: P3
    kind: invariant
    expression: "!Light || Btn"
```

### 3.1 Property `kind` vocabulary (closed)

| kind | meaning | proved when… | typical verdict use |
|---|---|---|---|
| `invariant` | expression holds in every scan | always true | SAFE programs |
| `mutual_exclusion` | listed `variables` never simultaneously true | never co-active | SAFE |
| `absence` | no runtime error of `subtype` (overflow, div0, array-oob) | error unreachable | SAFE |
| `reachability` | a state satisfying `expression` IS reachable | witness exists | VIOLATION / trigger-synthesis |
| `assertion` | inline assertion at `location` holds | assertion never fails | SAFE |
| `termination` | every scan cycle completes (no non-terminating loop) within the scan-watchdog budget | no scan hangs | SAFE; violated by non-termination LLBs (checked via `--ld-scan-watchdog`) |

- `expression`: Boolean/arithmetic over declared program variables, **per-scan semantics**
  (values sampled at scan top, as in the ESBMC-PLC scan model). Operators:
  `AND OR NOT`, `= <> < <= > >=`, `+ - * /`, parentheses. No temporal operators in v0.1.
- `absence` carries `subtype: overflow|div_zero|array_bounds`.
- Each property is checked **independently**; a task's overall verdict is `false`
  iff any expected-SAFE property is violated or any expected-reachable state is unreachable.

---

## 4. Controlled vocabularies

**Domains (target: 10).** `water_treatment, motor_control, manufacturing, traffic,
hvac, elevator, chemical_batch, packaging, power_substation, building_automation`
(final list frozen in `SUITE.yml`; ≥3 programs per domain recommended).

**Features (LD/ST constructs, for the coverage matrix).**
`contacts, coils, latch (set/reset), seal_in, ton, tof, tp, ctu, ctd, edge_rising,
edge_falling, comparison, arithmetic_int, arithmetic_real, array, function_block,
multi_pou, case, for_loop, while_loop`.

**Difficulty.** `easy` (single-rung / feature demo), `medium` (multi-rung, one FB kind),
`hard` (multi-POU, arithmetic, deep k), `challenge` (currently unsolved by ≥1 baseline —
report but do not require agreement).

**Ground-truth method.** `expert` (hand-proved/hand-audited), `cross-tool-consensus`
(≥2 tools agree + audited), `fault-injection` (mutant of a known-SAFE base; witness documented).

---

## 5. Metrics (auto-computed at ingest)

A single `ingest.py` parses each program and fills `metrics:` — `rungs, loc, pous,
variables`, plus a derived `features` sanity-check. Guarantees consistency and prevents
hand-miscounting. Programs failing schema validation or ingest are rejected from the suite.

---

## 6. Runner contract (SV-COMP-style)

For each `(variant, tool)`:
1. adapter converts/loads the program (LD-graphical → tool's input as needed),
2. runs the tool with a fixed resource limit (e.g. 900 s CPU, 15 GB) under `runexec`,
3. maps the tool's output to `{true, false, unknown}`,
4. compares to `expected_verdict` → status ∈ `{correct, wrong, unknown, timeout, error}`,
5. for `false` results, optionally validates the witness against the seeded defect.

Result record (`results/<tool>/<id>.json`):
```json
{"benchmark": "motor_interlock", "variant": "bomb.st", "tool": "esbmc-plc+",
 "verdict": "false", "expected": "false", "status": "correct",
 "cpu_time_s": 3.4, "mem_mb": 210, "witness_valid": true}
```

**Honest-coverage rule:** if a tool cannot ingest a program (e.g. PLCverif on graphical LD,
nuXmv on ST-without-SMV-translation), record `status: error, reason: unsupported_format`
rather than dropping the row. Per-tool coverage gaps are a reported finding, not hidden.

---

## 7. Top-level `SUITE.yml`

```yaml
format_version: "0.1"
name: "IEC 61131-3 Formal Verification Benchmark Suite"
version: "1.0.0"
license: CC-BY-4.0                  # suite-level; per-program license in each benchmark.yml
zenodo_doi: "TBD"
domains: [water_treatment, motor_control, manufacturing, traffic, hvac,
          elevator, chemical_batch, packaging, power_substation, building_automation]
composition_target: {LD-textual: 25, LD-graphical: 20, ST: 5}
benchmarks: []                      # generated index: id -> path, language, domain, verdict
```

---

## 8. Design rationale (for the paper's "Design Principles" section)

- **SV-COMP compatibility** (`expected_verdict: true|false`, task descriptor, property files,
  witness validation) → the suite drops straight into P10 (SV-COMP entry) with no rework.
- **Verdict out of comments, into schema** → machine-checkable ground truth; no ambiguity.
- **Stable ids + append-only** → citable, reproducible across suite versions.
- **Per-program license field** → clean handling of MathWorks/SWaT redistribution limits
  (link-only programs get `license: link-only` and a URL instead of a bundled file).
- **fault-injection as a first-class ground-truth method** → leverages your existing
  legit/malicious pairs (PLC-LD-dataset, SWaT) as ready-made known-UNSAFE tasks.
```
```
```

**Open decisions for you (§4 / §7):** final 10-domain list, resource limits, and whether
LD-graphical is stored as native PLCopen XML only or also mirrored to textual LD.
