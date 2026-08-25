# Frontend probe pack

Four experiments that decide what the v2.0 generator has to emit. Run before writing
any generator code.

```
ESBMC=/path/to/esbmc-plc/build/src/esbmc/esbmc ./run_probe.sh
```

## Why every probe is a pair

Each probe ships a SAFE twin and a VIOLATION twin over the **same logic** and the
**same property**. That is not redundancy, it is the soundness gate.

A frontend that does not understand a body element may skip it, find nothing to
check, and report `VERIFICATION SUCCESSFUL`. A lone SAFE probe returning SUCCESSFUL
is then indistinguishable from "the file was ignored". If the bomb twin also returns
SUCCESSFUL, the probe is **VOID** and tells us nothing about support.

This is the same trap the project's `--error-label` rule already warns about: a silent
SUCCESSFUL because the instrumentation never reached the GOTO program.

## The four questions

| Probe | Question | What a SUPPORTED verdict changes |
|---|---|---|
| P0 | Does this build reproduce the verdicts in `results/`? | Nothing. If it fails, every other row below is uninterpretable. |
| P1 | Does ESBMC accept an `<ST>` body inside PLCopen XML? | Reopens the 38 skipped variants with no ESBMC work and no new logic. |
| P2 | Does it accept an `<FBD>` body? | Decides whether the FBD slice gets a baseline column or relies on `ir-equivalence`. |
| P3 | Does it accept an `<SFC>` body? | Same, for SFC. |
| P4 | What does `--ld-props` actually accept? | Sets the ceiling on the property tier, and on the temporal tier. |

P1 is the one to run first. It is the highest value and the least confounded.

## P4 detail

All six property files run against the **known-good LD pair**, so the frontend is held
constant and only the property form varies.

| File | Form | Why |
|---|---|---|
| `p4a_mutex.yaml` | `mutual_exclusion` | Control. This is what `run_v84.py` emits today. |
| `p4b_invariant_cstyle.yaml` | `invariant`, `!(Motor_A && Motor_B)` | Same meaning as p4a. `run_v84.py`'s docstring says v8.4 needs a single boolean var; this checks whether that still holds. |
| `p4c_invariant_iec.yaml` | `invariant`, `NOT (… AND …)` | Checks whether the `iec2c()` translation step is still needed. |
| `p4d_reachability.yaml` | `reachability` | `run_v84.py` drops these before calling ESBMC. Acceptance probe. |
| `p4e_absence.yaml` | `absence`, `overflow` | Acceptance probe. No overflow is possible in an all-BOOL program. |
| `p4f_two_props.yaml` | two properties | Checks whether both are checked or only the first. P2 is false on `clean.xml` by construction, so a SAFE verdict here means P2 was not evaluated. |

## Confounder on P2 and P3

The FBD and SFC files are hand-authored against my reading of PLCopen TC6, not against
the XSD. A `REJECTED` verdict on either therefore has two possible causes: ESBMC does
not support the body type, or the XML is malformed.

Disambiguate before drawing any conclusion:

1. Validate against the TC6 v2.01 XSD (`xmllint --schema tc6_xml_v201.xsd …`).
2. Or open the file in Beremiz or the OpenPLC Editor, which read PLCopen XML. If they
   load it and ESBMC does not, the gap is ESBMC's.

P1 and P4 do not have this problem: P1 changes exactly one element against a file
ESBMC already verifies, and P4 changes no XML at all.

## Interpreting the output

| Verdict | Meaning |
|---|---|
| `SUPPORTED` | clean proved, bomb refuted. The frontend really read the body. |
| `VOID` | bomb returned SUCCESSFUL. The body was probably ignored. Do not read this as support. |
| `REJECTED` | Parse or conversion error. See the log, and check the confounder above. |
| `INCONCLUSIVE` | Timeout or unknown. Raise `TIMEOUT` and retry. |
