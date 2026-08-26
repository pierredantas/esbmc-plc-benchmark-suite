# How ESBMC-PLC works

ESBMC-PLC is not a separate tool. It is a front end inside ESBMC, sitting beside the
front ends for C, C++, Python and Solidity, and it hands its result to the same
verification engine they all use. `langapi/mode.cpp` maps the `ld` extension to it,
which is why a file has to be named `program.ld` even when its content is PLCopen XML.

That split matters when you read a verdict. The engine underneath has been attacked by
years of SV-COMP entries and C benchmarks. The front end is young, and it is where your
ladder becomes something the engine can reason about. Almost everything that can go
wrong for a PLC program goes wrong on the left of the diagram below.

## The pipeline

<svg class="diagram" viewBox="0 0 620 600" role="img" aria-label="Pipeline diagram: program and properties enter the LD front end, which parses, type checks, builds an IR, converts to GOTO and encodes properties as assertions, then the shared ESBMC engine symbolically executes, solves and reports"><defs><marker id="ar1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs><g stroke="currentColor" fill="none" stroke-width="1.4" marker-end="url(#ar1)"><path d="M310 58 V82"/><path d="M310 126 V144"/><path d="M310 188 V206"/><path d="M310 250 V268"/><path d="M310 312 V330"/><path d="M535 58 V353 H446"/><path d="M310 374 V404"/><path d="M310 448 V466"/><path d="M310 510 V528"/></g><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="210" y="20" width="200" height="38" rx="3"/><rect x="470" y="20" width="130" height="38" rx="3"/><rect x="180" y="84" width="260" height="42" rx="3"/><rect x="180" y="146" width="260" height="42" rx="3"/><rect x="180" y="208" width="260" height="42" rx="3"/><rect x="180" y="270" width="260" height="42" rx="3"/><rect x="180" y="332" width="260" height="42" rx="3"/><rect x="180" y="406" width="260" height="42" rx="3"/><rect x="180" y="468" width="260" height="42" rx="3"/><rect x="180" y="530" width="260" height="42" rx="3"/></g><path d="M40 388 H580" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" fill="none" opacity="0.6"/><g fill="currentColor" font-size="12.5" text-anchor="middle"><text x="310" y="44">program.ld  (PLCopen XML)</text><text x="535" y="44">props.yaml</text><text x="310" y="110">PLCopen XML parser → LdAst</text><text x="310" y="172">type checker</text><text x="310" y="234">IR builder → LdIR</text><text x="310" y="296">ld_converter → GOTO</text><text x="310" y="352">property encoder → assertions</text><text x="310" y="432">goto-symex: unroll scans → SSA</text><text x="310" y="494">SMT backend: Bitwuzla or Z3</text><text x="310" y="556">verdict and counterexample</text></g><g fill="currentColor" font-size="11" opacity="0.75"><text x="46" y="100">ld-frontend</text><text x="46" y="410">shared ESBMC engine</text></g></svg>

The first five boxes are roughly 4,600 lines under `src/ld-frontend/`. The last three
are the engine that every other ESBMC front end also feeds.

## What each stage does

**Parse.** `parser/plcopen_xml_parser.cpp` reads the XML into an AST of rungs and
elements. It is the largest single file in the front end, because PLCopen graphical
bodies are a graph: each element names the elements it draws power from, and the parser
has to turn that fan-in into an order.

**Type check.** `semantics/type_checker.cpp` rejects programs that reference undeclared
variables or wire incompatible types together.

**Properties.** `property/yaml_property_parser.cpp` reads `--ld-props`. It accepts
`invariant`, `mutual_exclusion`, `absence` and `reachability`. Nothing else, which is
why a `termination` property errors out rather than being checked.

**Build the IR.** `ir/ld_ir_builder.cpp` turns the AST into `LdIR`, a cyclic control
flow graph whose nodes are applications of a structural operational semantics. The
header states the shape directly:

```
INIT_BLOCK
└── SCAN_LOOP (while true)
    ├── READ_INPUTS
    ├── RUNG_1 ... RUNG_n
    └── WRITE_OUTPUTS
```

**Convert.** `ir_gen/ld_converter.cpp` emits GOTO code into the symbol table. This is
the step whose output every lesson on this site prints, because it is the last point at
which your program is still recognizable.

**Encode properties.** `property/property_encoder.cpp` builds assertions and splices
them into the body of the scan loop, so each one is checked once per scan rather than
once per program.

## The scan model

<svg class="diagram" viewBox="0 0 620 392" role="img" aria-label="Scan model: ESBMC main runs static init then calls scan loop, which forever re-samples inputs, evaluates rungs, checks assertions and latches previous values"><defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="110" y="18" width="400" height="38" rx="3"/><rect x="60" y="86" width="500" height="282" rx="6"/><rect x="100" y="132" width="400" height="42" rx="3"/><rect x="100" y="187" width="400" height="42" rx="3"/><rect x="100" y="242" width="400" height="42" rx="3"/><rect x="100" y="297" width="400" height="42" rx="3"/></g><g stroke="currentColor" fill="none" stroke-width="1.4" marker-end="url(#ar2)"><path d="M310 56 V84"/><path d="M310 174 V185"/><path d="M310 229 V240"/><path d="M310 284 V295"/><path d="M520 318 H536 V153 H502"/></g><g fill="currentColor" font-size="12.5" text-anchor="middle"><text x="310" y="42">__ESBMC_main: static init, then call ld::scan_loop()</text><text x="310" y="158">READ_INPUTS: every input := nondet</text><text x="310" y="213">RUNG 1 … RUNG n: contacts, coils, timers, counters</text><text x="310" y="268">property assertions</text><text x="310" y="323">epilogue: latch prev(var) for edge contacts</text></g><g fill="currentColor" font-size="11.5" opacity="0.8"><text x="76" y="112">ld::scan_loop — while (true)</text></g></svg>

Three details in there are worth more than they look.

**Inputs are re-sampled every scan.** Not once at startup. The converter says why:

> READ_INPUTS (SOS cyclic-scan model, §3.3): at the start of every scan iteration each
> physical input is re-sampled nondeterministically. Without this the inputs stay frozen
> at their initial value and every property verifies vacuously.

That sentence is the whole reason the ingestion gate on every lesson page checks that
your property variables are assigned inside the loop. A body that never reaches the
scan loop leaves the inputs frozen at zero, and a frozen program satisfies almost any
safety property you can write.

**The loop lives in its own function.** `__ESBMC_main` does static initialization and
then calls `ld::scan_loop`, so main stays loop-free and the unwinding bound applies to
scans.

**Edges need a previous value.** A rising-edge contact compares its variable against
the value it held at the last scan boundary, and the epilogue latches that shadow. Get
the boundary wrong and an edge either never fires or fires one scan late.

## The semantics, rule by rule

`semantics/sos_semantics.h` names twelve rules. Every node in the IR records which one
produced it, so a rung is a sequence of rule applications rather than an opaque
formula.

| rule | meaning |
|---|---|
| `NO_Contact_True` / `NO_Contact_False` | a normally-open contact passes power when its variable is true |
| `NC_Contact_True` / `NC_Contact_False` | a normally-closed contact passes power when its variable is false |
| `Rising_Contact` | `pf_out = IN and var and not prev(var)` |
| `Falling_Contact` | `pf_out = IN and not var and prev(var)` |
| `Output_Coil` | `var := pf` |
| `Set_Coil` / `Reset_Coil` | `if pf then var := true` / `:= false` |
| `TON_Step` | `if IN then ET++ else ET := 0; Q := IN and ET >= PT` |
| `TOF_Step` | `if IN then {ET := 0; Q := T} elif Q then {ET++; Q := ET < PT}` |
| `TP_Step` | `if Q then {ET++; Q := ET < PT} elif rising IN then {ET := 0; Q := T}` |
| `CTU_Step` | rising `CU` increments `CV`; `Q := CV >= PV`; `R` resets |
| `CTD_Step` | rising `CD` decrements `CV`; `Q := CV <= 0`; `LD` loads `PV` |
| `Arith_Step` | `OUT := IN1 op IN2` |

Timers use a fixed-tick model: `ET` counts scans, not milliseconds. A `PT` of 5 means
five scans. That is a modeling choice, and it is the reason several timer benchmarks
in this suite are marked `candidate` rather than `validated`.

## How a property becomes an assertion

| kind | what gets asserted |
|---|---|
| `invariant` | `assert(expr)` |
| `mutual_exclusion` | `assert(!(A && B && ...))` |
| `absence` | `assert(!expr)` |
| `reachability` | `if (guard) assert(false)`, so a counterexample is the witness |

`reachability` is the interesting one. It inverts the usual reading: the property is
written to fail, and the counterexample ESBMC returns is the input sequence that gets
you there. That is how the suite recovers a trigger for a logic-level bomb rather than
merely proving one exists.

Expressions are parsed as C, so write `!(A && B)`. The IEC spelling `NOT (A AND B)` is
rejected as an undeclared variable.

## Then the engine takes over

From the GOTO program onward, nothing is PLC-specific. `goto-symex` unrolls the scan
loop, builds a single static assignment formula over the unrolled scans, and hands it to
an SMT solver. The mode you pick decides what that unrolling means.

| mode | what it does | when to use it |
|---|---|---|
| `--incremental-bmc --unwind N` | search for a counterexample within N scans | you expect a violation and want the trace |
| `--k-induction` | base case, forward condition, inductive step | you expect the property to hold for every scan |
| default BMC | one fixed bound | quick triage |

A `VERIFICATION SUCCESSFUL` from k-induction is a proof over all scans. The same words
from bounded model checking mean only that no counterexample exists within the bound,
which is a much weaker claim wearing the same label.

## Options that change the model

| option | effect |
|---|---|
| `--ld-props FILE` | the YAML property specification |
| `--ld-scan-watchdog` | instruments `WHILE` loops **in user function-block ST bodies** with an assertion that fails past the budget, modeling a scan overrun |
| `--ld-scan-budget N` | tolerated iterations, default 8; keep it at or below `--unwind` |
| `--ld-sound-mode` | an unsupported construct in an FB body becomes a no-op instead of a nondeterministic over-approximation |
| `--ld-fault-injection` | plants known semantic errors, negating contact polarities and degrading Set/Reset coils, to check that your properties would notice |

The watchdog is narrower than its name suggests. It instruments loops inside function
block bodies written in Structured Text, not the ladder scan itself, which is what makes
it the right instrument for the non-termination benchmarks in this suite and the wrong
one for anything else.

## Why the lessons print the encoding

Read the diagram again and notice how much happens before the solver is involved. Your
rung is parsed from a graph, ordered, rewritten into rule applications, lowered into
GOTO, and only then verified. A defect anywhere in that chain produces a smaller or
different program that still verifies, and the verdict looks identical either way.

[Lesson 1.2](lessons/series-parallel/index.md) shows one build losing a parallel branch
and still reporting SUCCESSFUL. [Lesson 1.4](lessons/seal-in/index.md) shows the same
thing costing a latch. Neither is visible in the verdict, and both are obvious in the
scan body.
