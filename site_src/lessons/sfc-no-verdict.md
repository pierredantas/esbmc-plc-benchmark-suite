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

## No second opinion either

The C route rescued the FBD programs in the last two lessons. It cannot rescue these.

Beremiz renders ladder and function block diagrams to Structured Text, and the suite's
adapter carries LD, ST, IL and FBD sources through to a verdict. SFC is the gap: no
sequential function chart in this catalog has been carried through, so there are zero via-C
records for any of them. The route that exists precisely to answer what the ladder front end
cannot has not been extended to the one language where it is needed most.

## What this part is for

A benchmark suite is allowed to have holes. It is not allowed to hide them behind a column
that says `SAFE`.

Four benchmarks here carry a green verdict and a failing gate, and the honest reading is
that the suite ships SFC programs it cannot currently verify. Two things would change that,
and both are open work rather than opinion: ESBMC reading `<SFC>` bodies, which is
[#7354](https://github.com/esbmc/esbmc/issues/7354), or the via-C adapter learning to carry
a chart through Beremiz.

Until one of them happens, the SFC rows are here to be counted against the tool rather than
for it. [Lesson 3.6](../what-a-property-says/index.md) collects the thirty recorded runs whose
verdict meant nothing. Eight of them are on this page.
