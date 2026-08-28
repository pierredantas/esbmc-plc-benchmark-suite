Every lesson so far has been combinational. Nothing carried a value from one scan into
the next, so the order in which rungs ran could not matter. Edge detection breaks that,
and the moment order matters this suite stops agreeing with the tool.

## Detecting a rising edge

A PLC has no interrupt for "this input just went high". You compare the input against
what it was last scan, and you keep last scan's value yourself:

<svg class="diagram" viewBox="0 0 620 220" role="img" aria-label="Three rungs: Rise from Sig and not Sig_prev, OneShot from Rise, then Sig_prev from Sig"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V202"/><path d="M592 18 V202"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H110"/><path d="M126 52 H250"/><path d="M266 52 H501"/><path d="M535 52 H592"/><path d="M110 40 V64"/><path d="M126 40 V64"/><path d="M250 40 V64"/><path d="M266 40 V64"/><path d="M246 66 L270 38"/><path d="M508 38 Q494 52 508 66"/><path d="M528 38 Q542 52 528 66"/><path d="M28 112 H110"/><path d="M126 112 H501"/><path d="M535 112 H592"/><path d="M110 100 V124"/><path d="M126 100 V124"/><path d="M508 98 Q494 112 508 126"/><path d="M528 98 Q542 112 528 126"/><path d="M28 172 H110"/><path d="M126 172 H501"/><path d="M535 172 H592"/><path d="M110 160 V184"/><path d="M126 160 V184"/><path d="M508 158 Q494 172 508 186"/><path d="M528 158 Q542 172 528 186"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="118" y="32">Sig</text><text x="258" y="32">Sig_prev</text><text x="518" y="32">Rise</text><text x="118" y="92">Rise</text><text x="518" y="92">OneShot</text><text x="118" y="152">Sig</text><text x="518" y="152">Sig_prev</text></g></svg>

Three rungs, and the order is the whole design:

1. `Rise := Sig AND NOT Sig_prev` compares now against last scan
2. `OneShot := Rise` publishes the pulse
3. `Sig_prev := Sig` records now, for the next scan to compare against

Rung 3 has to run last. If it runs before rung 1, then `Sig_prev` already equals `Sig`
when rung 1 reads it, `Rise` is always false, and the edge detector detects nothing.

IEC 61131-3 makes that guarantee: rungs execute in order, and each one reads what the
rungs above it wrote in this same scan. The order is not a hint from the drawing. It is
the semantics.

{{files: benchmarks/traffic/g_rtrig_edge/program.xml | benchmarks/traffic/g_rtrig_edge/props.yaml}}

## The property

{{show: benchmarks/traffic/g_rtrig_edge/props.yaml}}

`!OneShot || Sig` says the one-shot only fires while the signal is high. Trace the three
rungs by hand under sequential evaluation and it holds: `OneShot` is raised in the same
scan as the edge, and in that scan `Sig` is 1. The suite records the expected verdict as
SAFE, and by the standard that is right.

## The run

{{record: rtrig_edge}}

Neither build agrees.

## What went wrong, in the encoding

The front end emits the three rungs in this order:

```
ASSIGN Sig_prev=1 && Sig;              rung 3
ASSIGN OneShot=1 && Rise;              rung 2
ASSIGN Rise=1 && Sig && !Sig_prev;     rung 1
```

Rung 3 first. By the time rung 1 asks whether `Sig_prev` differs from `Sig`, they are
equal by construction, so `Rise` is permanently false. The edge detector is dead code.
The property still holds, vacuously, and k-induction cannot close the proof from an
arbitrary starting state, so the verdict is UNKNOWN rather than a false SUCCESSFUL.

master reorders too, and then adds a snapshot:

```
ASSIGN Rise__prev=1 && Rise;           snapshot at scan top
ASSIGN Sig_prev__prev=1 && Sig_prev;
ASSIGN Sig_prev=1 && pf8;              rung 3
ASSIGN OneShot=1 && pf6;               rung 2, from Rise__prev
```

Snapshotting at the top of the scan makes the result independent of rung order, which
is coherent, and it is the semantics of a synchronous language such as Lustre or SMV.
It is not the semantics of IEC 61131-3. Every rung now reads last scan's values, so
`OneShot` lags the edge by one scan and fires when `Sig` has already gone low. That is a
real violation of the property, in the program master built.

The counterexample above is worth reading slowly. `Sig` goes high, `Rise` goes high.
Next scan `Sig` is back low, `Rise__prev` still carries the 1, and `OneShot` comes up
against a low signal.

## The cause

This is not a heuristic that guessed wrong. `parser/plcopen_xml_parser.cpp` decides scan
order in what its comment calls step 7:

> emit one sink per coil, in rightPowerRail order — the order the vendor tool draws the
> networks, hence the scan execution order.

Coils that the right power rail does not enumerate fall through to a second loop over
the node table, and that table is a `std::unordered_map<int, GNode>`. Scan order then
comes from hash iteration order.

In this repository, 35 of the 51 graphical programs leave the right rail's
`<connectionPointIn />` empty, so 35 of them take the fallback. The consequences are
visible without reading any source:

| program | coil localIds | order executed |
|---|---|---|
| `g_rtrig_edge` | 5, 7, 9 | 9, 7, 5 |
| `demo/interlock.ld` | 12, 21 | 12, 21 |
| `demo/interlock_bug.ld` | the same file, one contact fewer | the opposite order |

Two files that differ by a single deleted contact run their rungs in opposite orders.
Nothing in either file asked for that.

## The falling-edge twin behaves the same way

{{files: benchmarks/packaging/g_ftrig_edge/program.xml | benchmarks/packaging/g_ftrig_edge/props.yaml}}

{{record: ftrig_edge}}

## What to take from this

Read the verdict column and you would conclude the benchmark is wrong. Read the encoding
and you find the opposite: the program is right, the property is right, the expected
verdict is right under the standard, and the tool ran the rungs in an order the file
never specified.

This is what a benchmark suite is for. A task with a defensible ground truth, established
independently of any tool, is the only thing that can tell you a tool is wrong rather
than merely different. Had the expected verdict been recorded as "whatever ESBMC says",
this defect would have been invisible.

Two practical consequences if you are writing PLCopen XML by hand. Wire the right power
rail: list every coil in `<connectionPointIn>` in the order you want the scan to run,
and the well-defined path is taken. And when order matters to your program, write a
property that is sensitive to it, the way lesson 1.2 used a discriminator, rather than
trusting that the tool read your drawing the way you drew it.
