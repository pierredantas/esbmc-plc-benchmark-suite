# Porting the textual-LD and ST benchmarks to PLCopen XML (ESBMC-PLC v8.4)

**Why this exists.** ESBMC-PLC v8.4's front-end accepts **only PLCopen XML** (with a `.ld`
extension). The 15 textual-LD (`.ld` DSL) and 10 ST (`.st`) benchmarks therefore do not run as
stored. Porting them is **not** a mechanical re-serialisation: for timers, counters, and latches
the recorded verdict — established under an independent reference semantics — may **not transfer**,
because ESBMC-PLC's scan-cycle models differ. This document is the procedure: the accepted XML
forms, a per-construct recipe, and — the important part — how to re-establish ground truth under
the tool's own semantics. Verified against ESBMC-PLC v8.4 (build recipe in `tools/BUILD_AND_RUN.md`).

Status of the graphical slice (context): all 25 graphical benchmarks already run — 45 variants,
43 correct, 2 unknown, 0 wrong (`results/summary_v84_full.tsv`). This protocol is about the
remaining 25 textual-LD + ST benchmarks.

---

## 0. Hard rules learned about the v8.4 interface

1. **Input = PLCopen XML, file extension `.ld`.** Content can be graphical LD or ST-in-XML; the
   frontend XML-parses it. A raw `.st` or the `XIC/OTE` textual DSL is rejected
   (`failed to figure out type of file` / `No document element found`).
2. **Property operators are C-style: `&&`, `||`, `!`** — NOT IEC `AND`/`OR`/`NOT`. Writing `AND`
   makes the parser read the whole string as one variable (`undeclared variable 'A AND B'`).
3. **Property kinds:** `invariant`, `mutual_exclusion`, `reachability`, `absence`. **No
   `termination`** — non-termination is caught by `--ld-scan-watchdog --ld-scan-budget N` with
   **no property file**. `invariant.expression` may be a single boolean var *or* a C-style
   compound; `mutual_exclusion` takes `variables: [a, b]`.
4. **Authoring tooling:** `runner/run_v84.py` already translates the suite's IEC-operator schema
   to v8.4 at run time (`iec2c()`), so once a program is valid PLCopen XML the adapter handles
   its property. Keep the suite's `props.yaml` in the documented schema; let the adapter translate.
5. **Practical:** write test XML/YAML to files and mount them; do **not** heredoc `&&` through
   `docker ... bash -lc '...'` (the shell mangles it).

---

## 1. The two accepted PLCopen-XML shapes

### 1a. Simple `<rung>` LD (contacts, coils, standard FB blocks)
Far simpler than the full connection-graph. Series contacts = AND. One coil per rung.
```xml
<pou name="P" pouType="program">
  <interface>
    <inputVars><variable name="A"><type><BOOL/></type></variable> ... </inputVars>
    <outputVars><variable name="Y"><type><BOOL/></type></variable> ... </outputVars>
  </interface>
  <body><LD>
    <rung localId="1"><contact variable="A"/><contact variable="B"/><coil variable="Y"/></rung>
    <rung localId="2"><block typeName="TON" instanceName="t1">
       <variable formalParameter="IN">Run</variable><variable formalParameter="PT">PT</variable>
       <variable formalParameter="Q">TQ</variable><variable formalParameter="ET">ET</variable></block></rung>
  </LD></body>
</pou>
```
Standard blocks confirmed available: `TON`, `TOF`, `TP`, `CTU`, `CTD` (formal parameters
`IN/PT/Q/ET`, `CU/CD/R/PV/Q/CV`). **Parallel/OR is not expressible in this simple rung form** —
for OR logic use shape 1c.

### 1b. ST inside a function block + observer (for ST programs)
```xml
<pou name="CTRL" pouType="functionBlock">
  <interface>
    <inputVars><variable name="level"><type><INT/></type></variable></inputVars>
    <outputVars><variable name="Safe"><type><BOOL/></type></variable></outputVars>
    <localVars> ... </localVars>
  </interface>
  <body><ST><![CDATA[
  (* IEC ST here; MIND OPERATOR PRECEDENCE — parenthesise NOT(...) explicitly *)
  Safe := NOT (pump AND level_high);
  ]]></ST></body>
</pou>
<pou name="MAIN" pouType="program">
  <interface><outputVars><variable name="Safe"><type><BOOL/></type></variable></outputVars>
    <localVars><variable name="lv"><type><INT/></type></variable></localVars></interface>
  <body><LD>
    <block localId="10" typeName="CTRL" instanceName="c0"><variable formalParameter="level">lv</variable></block>
    <outVariable localId="11"><expression>Safe</expression>
      <connectionPointIn><connection refLocalId="10" formalParameter="Safe"/></connectionPointIn></outVariable>
  </LD></body>
</pou>
```
Property: `invariant expression: "Safe"`. The FB computes the safety observable; MAIN exposes it.

### 1c. Full connection-graph LD (only when you need OR / parallel branches)
Use the `leftPowerRail`/`contact`/`coil`/`rightPowerRail` form with an **OR-junction on a
contact** (multiple `<connection>` in one `connectionPointIn`) — the pattern the parseable corpus
uses and the authored `g_*` benchmarks already use successfully. See any authored graphical
benchmark (e.g. `benchmarks/power_substation/g_substation_breaker/`) for a worked example.

---

## 2. Per-construct porting recipe

| Construct (K-LD DSL) | XML shape | Verdict transfers? | Notes |
|---|---|---|---|
| Series AND (`XIC*XIC`) | 1a rung, series contacts | **yes** | verified (`comb_and` → SAFE) |
| Parallel OR (`XIC+XIC`) | 1c graph, junction-on-contact | yes (Boolean) | rung form can't express OR |
| Coil (`OTE`) | `<coil variable=.../>` | yes | — |
| Latch (`OTL`/`OTU`) | **open problem** | — | `storage="set"/"reset"` is **NOT honored** (both act as normal coils → wrong verdict). Encode the latch in an ST FB body (1b) instead, or find the block form the tool accepts. |
| Timer (`TON`/`TOF`/`TP`) | 1a block rung | **NO — re-establish** | ESBMC-PLC's scan-cycle timer model differs from the reference; `!Light\|\|Btn` fails (`Light=1,Btn=0` reachable). Re-label per §3. |
| Counter (`CTU`/`CTD`) | 1a block rung | **NO — re-establish** | same as timers |
| Edge (`R_TRIG`/`F_TRIG`) | rungs with a `_prev` coil | mostly | k-induction may return UNKNOWN on the safe case (proof strength) |
| ST program (single POU) | 1b FB + observer | usually, but | parenthesise `NOT(...)`; watch precedence |
| ST multi-POU (SWaT) | 1b, one FB per PLC + MAIN | verdict = termination | for the non-termination bombs, run **watchdog-only, no property**; the whole IEC structure must be represented as multiple `<pou>`s — the hardest case |

---

## 3. Ground-truth re-establishment (the part that is not mechanical)

For latches, timers, and counters the reference verdict may be wrong under ESBMC-PLC. **Do not
copy the stored verdict.** For each ported benchmark:

1. **Convert** the program to PLCopen XML (§1–2) and translate the property to C-operators
   (or let `run_v84.py` do it).
2. **Run** it under ESBMC-PLC v8.4:
   - expected-SAFE → `--k-induction`; expected-VIOLATION → `--incremental-bmc --unwind 20`;
   - always add `--ld-scan-watchdog --ld-scan-budget 8`.
3. **If the verdict matches** the reference → record it, done.
4. **If it differs** → read the counterexample (`--incremental-bmc` prints the state trace).
   Decide which case you are in:
   - **(a) Semantic divergence** — the tool's timer/counter/latch model legitimately makes the
     property hold/fail differently (e.g. Q persists a scan). The tool's verdict is *correct for
     this tool*. Record it as a **per-tool verdict** (`ground_truth.method: cross-tool-consensus`
     with a note, or a tool-specific verdict field) and document the divergence. This is a
     finding, not a bug.
   - **(b) Conversion error** — the XML doesn't model the intended logic (wrong wiring, precedence,
     unhonored `storage`). Fix the XML and re-run.
   - **(c) Genuine tool bug** — the program provably satisfies the property under the standard
     semantics yet the tool refutes it (or vice-versa), and it is not a modelling choice. Minimise
     to a small reproducer and report upstream; keep the benchmark with the standard-semantics
     verdict and mark it a known tool discrepancy.
5. **Never fold `UNKNOWN` into `SAFE`.** A `k`-induction `unknown` is recorded as `unknown`.

**Telling (a) from (c):** (a) is a defensible modelling difference documented in the tool's timer
semantics; (c) contradicts the IEC-61131-3 standard's stated timer/counter behaviour. When in
doubt, minimise and ask the tool authors — the adjudication itself is citable content for the
paper's cross-tool-semantics discussion.

---

## 4. Work loop (verified, reproducible)

```bash
# one-time: build the LD-enabled binary + run image  (tools/BUILD_AND_RUN.md)
# then, per candidate benchmark:
docker run --rm --platform linux/amd64 -v "$SUITE":"$SUITE" -v "$WORK":/w -w "$SUITE" esbmc-plc:run bash -lc '
  cp /w/candidate.ld /tmp/in.ld
  /usr/local/bin/esbmc /tmp/in.ld --ld-props /w/candidate.yaml --k-induction \
      --ld-scan-watchdog --ld-scan-budget 8 2>&1 | tail -20'
# once a batch is converted + labelled, re-run the whole suite:
docker run --rm --platform linux/amd64 -v "$SUITE":"$SUITE" -w "$SUITE" esbmc-plc:run \
  bash -lc "ESBMC=/usr/local/bin/esbmc python3 runner/run_v84.py"
```

## 5. Suggested order (easiest first, to build confidence)
1. **Boolean textual-LD** (`comb_or`, `comb_mixed` via shape 1c; the rest already have graphical
   twins) — verdicts transfer.
2. **Single-POU ST S-benchmarks** (`tank_overflow`, `sensor_forge`, `counter_scalability`) via 1b.
3. **Timers/counters** (7 benchmarks) via 1a — **re-establish verdicts per §3**; expect divergence.
4. **Latches** (`latch_basic`, `timer_latch_mix`) — solve the OTL/OTU encoding first (§2).
5. **SWaT multi-POU ST** (6) — hardest; for the non-termination bombs, watchdog-only.

Record every ported program in PLCopen XML **alongside** its original (do not delete the source),
and note in `benchmark.yml` when a verdict is tool-specific because the semantics diverge.
