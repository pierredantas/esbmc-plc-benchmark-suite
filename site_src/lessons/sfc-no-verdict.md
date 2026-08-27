The fifth language in the standard is a state machine: numbered steps, transitions between
them, and actions attached to the steps. It is how batch plants and anything else with a
sequence get written.

The suite ships four Sequential Function Chart benchmarks and can tell you nothing
trustworthy about any of them. This lesson is that result.

## What the programs are

Two plants, each with a clean and a bombed variant.

`sfc_batch_fill_drain` fills a vessel, reacts, then drains it, and the claim is that the two
valves are never open together:

{{show: benchmarks/chemical_batch/sfc_batch_fill_drain/props.yaml}}

`sfc_elevator_door` sequences a car between floors, and the claim is the one from
[lesson 2.4](../elevator-door/index.md):

{{show: benchmarks/elevator/sfc_elevator_door/props.yaml}}

Both properties are the kind this suite verifies routinely on ladder. Neither is exotic.

## Eight runs, eight gate failures

{{record: sfc_batch_fill_drain__clean}}

`SAFE` on both builds, `status: correct`, and the ingestion gate failing on both
`fill_valve` and `drain_valve`.

Take that row apart, because it is the most misleading shape a record can have. The verdict
matches what the benchmark expected, and the status column agrees. A table that scores tools on
whether the verdict matched would count this as a success, and the program was never read:
the `<SFC>` body went the way of the `<FBD>` bodies in
[lesson 6.1](../fbd-unread/index.md), leaving a scan loop that drives neither valve.

An empty program satisfies mutual exclusion. It satisfies everything.

{{record: sfc_batch_fill_drain__bomb}}

`unknown`, which at least declines to claim anything.

The elevator pair behaves identically, and the summary across all four SFC benchmarks is
uniform:

| | verdict | status | gate |
|---|---|---|---|
| `sfc_batch_fill_drain` clean | `SAFE` | correct | **fail** |
| `sfc_batch_fill_drain` bomb | `unknown` | unknown | **fail** |
| `sfc_elevator_door` clean | `SAFE` | correct | **fail** |
| `sfc_elevator_door` bomb | `unknown` | unknown | **fail** |

Eight runs across two builds, eight gate failures. Two of them say `SAFE`.

## The second route reaches them, and still cannot answer

The C route rescued the FBD programs in the last two lessons. Pointing it at these charts
took three attempts, and each failure was a different layer.

**The files were unreadable.** Beremiz extracts inline text with an XPath for an
`xhtml:p` element. These four charts wrote their transition conditions as
`<xhtml xmlns="...">start</xhtml>`, text directly inside the wrapper with no paragraph,
which satisfies the TC6 schema and is why `schema_check.py` never complained. Beremiz
raised `IndexError` on the empty XPath result. A file can be valid PLCopen and still be
unreadable by the reference open-source toolchain, and nothing in the schema will tell
you.

**MatIEC then emitted C that does not compile.** The elevator chart has a step named
`Moving` and an output named `moving`. MatIEC uppercases identifiers, so both became
`MOVING`, and the generated code applied the variable macro to a step struct:

```
./POUS.c:194:24: error: no member named 'flags' in 'STEP'
```

`iec2c` exited 0 while writing that file. A compiler that reports success and produces
uncompilable output is the same failure this suite keeps finding in front ends, one layer
down. Renaming the step clears it.

**ESBMC cannot decide the result.** With both fixed, all four charts now reach the solver:

{{record: sfc_batch_fill_drain__clean__viac}}

`timeout`. MatIEC compiles an SFC into a state machine whose transition scan is itself a
loop, so the harness nests that inside its own scan loop. The smallest bound that still
carries an honest unwinding assertion generates around a thousand verification conditions
that Z3 does not discharge in eight minutes. Dropping the bound low enough to finish makes
the run report a violated unwinding assertion in `BATCH_CYCLE_init__` rather than anything
about valves, which is a bound artifact and not a verdict.

So the answer changed from "no route reaches these" to "the route reaches them and runs out
of budget". That is progress worth having, and it is still not a verdict.

## What this part is for

A benchmark suite is allowed to have holes. It is not allowed to hide them behind a column
that says `SAFE`.

Four benchmarks here carry a green verdict and a failing gate, and the honest reading is
that the suite ships SFC programs it cannot currently verify. Two things would change that,
and both are open work rather than opinion: ESBMC reading `<SFC>` bodies, which is
[#7354](https://github.com/esbmc/esbmc/issues/7354), or the generated state machine
becoming tractable, which probably means a harness that drives the chart's own step
variable instead of nesting two loops.

Until one of them happens, the SFC rows are here to be counted against the tool rather than
for it. [Lesson 3.6](../what-a-property-says/index.md) collects the {{stat: gate.fail|words}}
recorded runs whose verdict meant nothing. Eight of them are on this page.
