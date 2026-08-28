A PLC has no clock in the sense a program on your laptop has one. It has scans, and a
timer counts them. Everything awkward about verifying timers follows from that.

## Time is counted in scans

ESBMC models a timer on a fixed tick: one scan advances time by exactly one task
period. A preset of `T#30ms` on a task declared at `T#10ms` is three scans, and the
GOTO program says so in as many words:

```
ASSIGN TON0__PT=3;
```

<svg class="diagram" viewBox="0 0 620 130" role="img" aria-label="Ladder rung: a Btn contact into a TON block with preset T#30ms, driving the Light coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V112"/><path d="M592 18 V112"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 56 H120"/><path d="M136 56 H250"/><path d="M370 56 H501"/><path d="M535 56 H592"/><path d="M120 44 V68"/><path d="M136 44 V68"/><rect x="250" y="28" width="120" height="56" rx="3"/><path d="M508 42 Q494 56 508 70"/><path d="M528 42 Q542 56 528 70"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="36">Btn</text><text x="310" y="52">TON</text><text x="310" y="72">PT = T#30ms</text><text x="518" y="36">Light</text></g></svg>

The block's power flow is its `Q` pin, so the coil after it is driven by the timer
output rather than by the contact in front of it.

{{files: benchmarks/hvac/g_ton_single/program.xml | benchmarks/hvac/g_ton_single/props.yaml}}

{{record: ton_single}}

SUCCESSFUL, with the gate passing. Before believing it, look at what the front end built.

## What a timer becomes

A `TON` is not a primitive to the solver. It has to be unrolled into state the scan loop
carries between iterations, and you can read the whole of it:

```
ASSIGN TOF0__IN=1 && pf3;
IF !TOF0__IN THEN GOTO ...
ASSIGN TOF0__ET=TOF0__ET + 1;
ASSIGN TOF0__Q=...
```

An elapsed-time counter, incremented on the scans where the input holds, and an output
raised when it passes the preset. That is the timer, and its presence in the scan body is
what makes any verdict about the lamp mean something. A front end that dropped the block
would leave `Light` as a plain copy of `Button`, and every property that happened to hold
of that reduced program would come back proved. The gate exists to catch exactly that,
mechanically, without anybody reading the encoding.

## The property was wrong, and the tool was right to say so

The textual benchmark `ld_tof_hold` carries this requirement:

{{show: benchmarks/hvac/g_tof_hold/implies_input.props.yaml}}

Read it against what an off-delay is for. The whole point of a TOF is to keep the lamp
lit after the sensor clears. So the property claims the component does not do its job.

{{record: tof_implies_input}}

Refuted, and the counterexample is the off-delay working: `Pir` goes high and `Light`
comes on, then `Pir` drops to 0 with `Button` still 0, and `Light` stays on.

The tool is right and the requirement is wrong. That is a distinction worth keeping
separate from a tool being wrong, because both arrive on the page as a red row.

## A requirement that does hold

Ask for something an off-delay really guarantees: while the sensor sees motion, the lamp
is lit. The delay only extends that, it never shortens it.

{{show: benchmarks/hvac/g_tof_hold/props.yaml}}

{{record: tof_hold}}

Proved. Between them the two properties pin the block down from both sides: the timer
extends the lamp past the sensor, and never cuts it short. A front end that had dropped the
`TOF` would answer the pair the other way round, refuting the requirement that holds and
proving the one that does not, which makes them a discriminator for the block in exactly
the sense lesson 1.2 used one for a dropped branch.

## The trap that cost this suite a factor of ten

PLCopen types the task interval as a string and the TC6 schema annotates it: *"Either a
constant duration as defined in the IEC or variable name"*, which reads as `T#10ms`.
Every program in this suite used to declare `interval="PT0.01S"`, the ISO 8601 spelling,
which the front end does not parse. It then falls back to a one millisecond tick,
silently, and every preset in the suite was ten times longer than intended.

Calling that purely our mistake would be too generous to the tooling. The one file in
this catalog exported by a real engineering tool writes `interval="PT0S"`, ISO 8601 as
well, so a genuine TwinCAT project hits this same silent fallback.
[Lesson 4.1](../real-export/index.md) has the comparison.

Nothing failed. No warning was printed. A `T#30ms` preset simply became 30 scans instead
of 3, and every timer benchmark still verified. It was fixed across all 43 programs on
2026-08-26, which is also why the Beremiz and MatIEC round trip in
[docs/INTEROP.md](https://github.com/pierredantas/esbmc-plc-benchmark-suite/blob/main/docs/INTEROP.md)
now runs without a hand patch.

If you write timer benchmarks, check the preset in the GOTO output. It is one grep, and
it is the only place the mistake is visible.
