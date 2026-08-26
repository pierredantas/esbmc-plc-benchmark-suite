# Probe results — ESBMC-PLC v8.4, run 2026-08-26

Binary: `ESBMC version 8.4.0 64-bit aarch64 macos`, built from source at `61172c6f`
(tag v8.4) against LLVM 18.1.8 arm64 and Z3 4.13.3. See `../docs/BUILD_MACOS.md`
for the six build blockers and their fixes.

**Caveat:** this is not the binary that produced `results/summary_v84_full.tsv`
(that was linux/amd64 with LLVM 22.1.6). P0 below exists to bound that risk.

## Results

| Probe | Verdict | Answer |
|---|---|---|
| P0 sanity | SUPPORTED | This build reproduces the recorded verdicts. Everything below is interpretable. |
| P1a ST body (xhtml wrapper) | **silently ignored** | No. |
| P1b ST body (bare text) | **silently ignored** | No. |
| P2 FBD body | **silently ignored** | No. |
| P3 SFC body | **silently ignored** | No. |
| P4a `mutual_exclusion` | SUPPORTED | Control. |
| P4b `invariant`, compound C syntax | SUPPORTED | `!(Motor_A && Motor_B)` works. |
| P4c `invariant`, IEC syntax | REJECTED | `NOT (… AND …)` → "undeclared variable". |
| P4d `reachability` | SUPPORTED | Requires a `justification` field. |
| P4e `absence` | SUPPORTED | Requires an `expression` field as well as `subtype`. |
| P4f two properties | both checked | Reports `Violated property: P2`. |

P4e and P4f show `clean=false` in `probe_results.tsv`. That is correct behaviour, not a
failure: both properties genuinely fail on `clean.xml`. They are acceptance probes, so the
SAFE/VIOLATION pairing the runner applies elsewhere does not apply to them.

## Finding 1 — v8.4 reads only `<LD>` bodies, and fails open

The frontend parses `<interface>` but drops `<ST>`, `<FBD>` and `<SFC>` bodies **without
any diagnostic**. The resulting GOTO program holds the declarations and nothing else.

Known-good `<LD>` body:

```
ASSIGN Motor_B=1 && rev;
ASSIGN Motor_A=1 && fwd && !rev;
```

`<ST>` body, same interface, same property:

```
ASSIGN Motor_A=0;
ASSIGN Motor_B=0;
```

With no assignments the coils keep their initial 0 and every safety property holds
vacuously. `p5_falsesafe/st_always_both.xml` clinches it: a body that unconditionally
executes `Motor_A := TRUE; Motor_B := TRUE;` returns **VERIFICATION SUCCESSFUL** against a
mutual-exclusion property on exactly those two variables.

This is a **false SAFE**, not a coverage gap. An unsupported input is indistinguishable
from a proof.

### Consequences for the suite

1. **The ST-in-XML shortcut does not exist.** The 38 variants ESBMC currently skips cannot
   be recovered by wrapping them in PLCopen XML. `BUILD_AND_RUN.md`'s "content ST/XML" is
   misleading; only an `<LD>` body is read.
2. **FBD and SFC have no ESBMC baseline**, which is what `ir-equivalence` is for.
3. **The runner needs an ingestion gate.** `run_v84.py` skips on file extension, which
   happens to be safe today. Any future adapter that feeds ESBMC an FBD or SFC task will
   silently record a correct-looking SAFE. Before trusting a verdict, assert the GOTO
   program actually assigns the property's variables.

## Finding 2 — the property tier is wider than documented

`BUILD_AND_RUN.md` states `invariant.expression` must be "a single boolean variable (not a
compound formula)". P4b refutes this: `!(Motor_A && Motor_B)` is accepted and gives the
right verdict on both variants. `reachability` and `absence` also work, given their
required fields, though `run_v84.py` drops `reachability` before calling ESBMC.

The one real constraint is syntax: expressions must use C operators. The `iec2c()`
translation in `run_v84.py` is still required.

## Finding 3 — parallel (OR) branches are encoded as last-branch-wins

A rung with two parallel branches into one coil, `Run := A OR B`, encodes as two
sequential assignments:

```
ASSIGN Run = 1 && A;
ASSIGN Run = 1 && B;
```

The second overwrites the first, so the program means `Run == B`. The branch structure
is discarded rather than disjoined.

**Discriminator** (`demo2/or_discriminator.ld`): ask whether `Run` implies `B`.
Under correct OR semantics `A=1, B=0` gives `Run=1` with `B=0`, so it must fail. Under
last-branch-wins `Run == B`, so it holds. ESBMC returns **VERIFICATION SUCCESSFUL**.

### Reach inside the suite

29 of the 45 graphical LD files contain a multi-connection `connectionPointIn`, i.e. an
OR junction. For every one of them the program ESBMC verified is not the program the
`benchmark.yml` documents.

`g_seal_in` is the sharpest case. Its `.ld` twin defines
`OTE(Run) := (XIC(Start) + XIC(Run)) * XIO(Stop)`, a self-holding coil. ESBMC encodes:

```
ASSIGN Run = 1 && Start && !Stop;
ASSIGN Run = 1 && Run   && !Stop;
```

which collapses to `Run = Start && !Stop`. Proof that the latch is gone: the invariant
`!Run || Start` ("Run implies Start"), which a genuine seal-in must violate, is **proved**
by k-induction. The benchmark named "seal in" contains no seal-in once parsed.

Its recorded verdict is still SAFE, and still correct, because the degenerate program also
satisfies `!Run || !Stop`. That is the trap: **the verdict survives, but the benchmark does
not test the feature it is named for.** `g_motor_interlock/bomb.xml` is the same shape — its
VIOLATION verdict happens to hold under both readings.

### Consequence

No verdict on an OR-junction benchmark is evidence for the documented logic until it is
rechecked. This does not mean the 29 verdicts are wrong; it means they are unsupported.
Each needs its GOTO encoding compared against its documented rung before the
`validated` label means anything.

This is a second, independent reason the v2.0 runner needs rung R0: an ingestion gate must
check not only that the body was read, but that what was encoded matches what was written.

---

# Two-version comparison — v8.4 `61172c6f` vs master `d88a9fa4`

Both built identically (LLVM 18.1.8, Z3 4.13.3, arm64 macOS), so the only variable
is ESBMC itself. Run with `probe/compare_versions.py`.

## Finding 3 is FIXED on master

The parallel-branch defect is gone. Master synthesises an accumulator per junction:

```
pf11 = B ;  pf10 = A
Run__pf0 = 0
IF pf11 THEN Run__pf0 = 1
IF pf10 THEN Run__pf0 = 1
Run = 1 && Run__pf0            <-- a genuine disjunction
```

The discriminator in `demo2/or_discriminator.ld` returns SUCCESSFUL on v8.4 (wrong)
and FAILED on master (right). Do not file Finding 3 upstream; it is already fixed.

**Caution when reading GOTO dumps.** Master's encoding is guarded, so grepping only
`ASSIGN` lines hides the conditions and makes the accumulators look like unconditional
constants. Always read the full `--goto-functions-only` output, guards included.

## Finding 1 is NOT fixed on master

The probe pack returns identical results on both binaries. `<ST>`, `<FBD>` and `<SFC>`
bodies are still discarded silently, and the false SAFE still occurs. Worth filing.

## Finding 4 — rung evaluation order does not follow IEC 61131-3

Both versions emit rungs in **reverse** document order. They differ in what they do
about it.

`g_ftrig_edge` is a falling-edge one-shot. Source order (identical in the graphical
XML and its textual twin):

```
Fall     := !Sig AND Sig_prev
OneShot  := Fall
Sig_prev := Sig
```

**v8.4** emits the reverse with no snapshots:

```
Sig_prev = Sig
OneShot  = Fall
Fall     = !Sig && Sig_prev      <-- Sig_prev was overwritten above
```

so `Fall = !Sig && Sig`, which is false in every scan. Confirmed: the invariant
`!Fall` is **proved** on v8.4. The falling-edge benchmark cannot fire its edge, so on
v8.4 it tests nothing. Its recorded result is `unknown`, which concealed this.

**master** emits the reverse but snapshots every variable at scan top, giving a
coherent *simultaneous* model:

```
Fall__prev = Fall ; Sig_prev__prev = Sig_prev      <-- snapshot
Sig_prev = Sig
OneShot  = Fall__prev                              <-- one scan late
Fall     = !Sig && Sig_prev__prev
```

`!Fall` is now refuted, so the edge fires. But `OneShot` lags a scan, and by then
`Sig` may be high again, so `!OneShot || !Sig` is violated.

IEC 61131-3 evaluates rungs sequentially, top to bottom, within one scan: a coil
written in rung 1 is visible to rung 2 in that same scan. Under those semantics
`OneShot` fires in the scan of the fall, while `Sig` is low, and the property holds.
That matches the benchmark's `expert` label and nuXmv's SAFE.

**Neither version implements IEC sequential rung semantics.** v8.4 is incoherent;
master is coherent but synchronous. This is worth reporting upstream, and it is the
kind of disagreement the suite exists to surface.

## Verdict drift across the 29 comparable tasks

| | |
|---|---|
| tasks compared | 29 |
| encoding changed | 29 (all) |
| verdict changed | 2 |

The two are `g_ftrig_edge/program.xml` and `g_rtrig_edge/program.xml`: expected SAFE,
`validated`, `unknown` on v8.4, **VIOL** on master. Every other verdict survives the
encoding change, but survival is not confirmation, for the reason given above.

## The termination slice, run with the scan watchdog

The other 16 graphical files carry `kind: termination` only, which `--ld-props` rejects
because the scan watchdog carries the property instead. Run with `--only watchdog`, so
`--ld-props` is omitted and `--ld-scan-watchdog --ld-scan-budget 8` does the work:

| | |
|---|---|
| tasks | 16 |
| verdict changed | **0** |
| encoding changed | 14 |

All 16 are correct on both versions. The two whose encoding did not move are the
`g_tank_substitution_coil` pair. This slice is the water_treatment corpus, the
over-represented domain, and it is stable across the two versions.

## Complete picture, all 45 graphical files

| slice | tasks | encoding changed | verdict changed |
|---|---|---|---|
| property-based (`--ld-props`) | 29 | 29 | 2 |
| termination (`--ld-scan-watchdog`) | 16 | 14 | 0 |
| **total** | **45** | **43** | **2** |

The two verdict changes are `g_ftrig_edge` and `g_rtrig_edge`, both explained by
Finding 4. Everything else holds its label across a near-total change of encoding,
which is reassuring for the corpus and says nothing about whether each encoding
matches its documented rung.
