The fifth language in the standard is a state machine: numbered steps, transitions between
them, and actions attached to the steps. It is how batch plants and anything else with a
sequence get written.

The suite ships four Sequential Function Chart benchmarks and can tell you nothing
trustworthy about any of them. This lesson is that result, and it is the one page in this
part that the August 2026 fix to
[esbmc#7354](https://github.com/esbmc/esbmc/issues/7354) barely improved. The front end now
says out loud that it cannot read a chart. It still cannot read a chart.

## What the programs are

Two plants, each with a clean and a bombed variant.

`sfc_batch_fill_drain` fills a vessel, reacts, then drains it, and the claim is that the two
valves are never open together:

{{show: benchmarks/chemical_batch/sfc_batch_fill_drain/props.yaml}}

`sfc_elevator_door` sequences a car between floors, and the claim is the one from
[lesson 2.4](../elevator-door/index.md):

{{show: benchmarks/elevator/sfc_elevator_door/props.yaml}}

Both properties are the kind this suite verifies routinely on ladder. Neither is exotic.

## Four runs, four refusals

{{record: sfc_batch_fill_drain__clean}}

```
ERROR: UnsupportedConstruct(SFC body of POU 'batch_cycle', tier=2)
```

That is what the fix bought: a named refusal instead of a verdict. It is worth knowing what
this row used to say, because it was the most misleading shape a record can have. `SAFE`,
`status: correct`, and the gate failing on both `fill_valve` and `drain_valve`. The verdict
matched what the benchmark expected and the status column agreed, so a table scoring tools
on whether the verdict matched would have counted it a success. The program was never read.
The `<SFC>` body went the way of the `<FBD>` bodies in
[lesson 6.1](../fbd-unread/index.md), leaving a scan loop that drove neither valve.

An empty program satisfies mutual exclusion. It satisfies everything.

{{record: sfc_batch_fill_drain__bomb}}

The elevator pair behaves identically, and all four SFC benchmarks are now uniform: refused
at parse, gate failing, nothing reaching the solver.

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

Three attempts to make it cheaper all failed, which is worth recording so nobody spends the
day twice. Assuming the one-hot step invariant, deleting the stored-action bookkeeping that
an `N` qualifier never uses, and pinning the step and action counts the loops read from the
instance each left the run timing out at four scans. Verification conditions grow roughly
linearly with depth, from 322 at two scans to 1984 at eight, while the solving time does
not, so the cost is in how hard each condition is rather than how many there are.

The depth that matters is fixed by the attack, not by us. Reaching Draining takes `start`,
then `level_high`, then `reaction_done`, so any honest run has to survive at least four
scans, and two is the most this encoding affords. Reporting a verdict at two scans would put
`SAFE` against the bombed chart as well as the clean one, which is the failure this whole
part is about.

## What this part is for

A benchmark suite is allowed to have holes. It is not allowed to hide them behind a column
that says `SAFE`.

Four benchmarks here used to carry a green verdict and a failing gate. They now carry an
error and a failing gate, which is better and is not a verdict either. The honest reading is
unchanged: the suite ships SFC programs it cannot currently verify.

Two things would change that. The front end could learn to read `<SFC>` bodies, which the
`tier=2` in that diagnostic says it does not; #7354 fixed the silence, not the gap. Or the
generated state machine could become tractable on the C route, which probably means a
harness driving the chart's own step variable instead of nesting two loops.

Until one of them happens, the SFC rows are here to be counted against the tool rather than
for it. [Lesson 3.6](../what-a-property-says/index.md) collects the {{stat: gate.fail|words}}
recorded runs whose verdict rests on nothing. Four of them are on this page.
