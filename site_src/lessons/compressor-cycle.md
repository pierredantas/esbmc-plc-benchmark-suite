A reciprocating compressor on a receiver, with two pressure switches setting the band.
Pressure falls to the cut-in, the compressor loads; pressure reaches the cut-out, it
unloads. Every workshop has one.

The interlock that matters is not in that description. A compressor motor started too
soon after stopping draws locked-rotor current into windings that have not cooled, and on
a receiver with a leak the cycle can repeat every few seconds. So the load rung carries a
minimum-off term, and the machine sits there for a while doing nothing while the pressure
is already low.

## The rung

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Load in parallel with press low and min-off-done in series, gated by normally closed press high, latches load"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H320"/><path d="M28 98 H140"/><path d="M156 98 H270"/><path d="M286 98 H320"/><path d="M320 52 V98"/><path d="M320 52 H396"/><path d="M412 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M140 86 V110"/><path d="M156 86 V110"/><path d="M270 86 V110"/><path d="M286 86 V110"/><path d="M396 40 V64"/><path d="M412 40 V64"/><path d="M392 66 L416 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/></g><circle cx="320" cy="52" r="3.5" fill="currentColor"/><circle cx="320" cy="98" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Load</text><text x="404" y="32">PressHigh</text><text x="588" y="32">Load</text><text x="148" y="128">PressLow</text><text x="278" y="128">MinOffDone</text></g></svg>

`Load := (Load OR (PressLow AND MinOffDone)) AND NOT PressHigh`. One rung, one latch.
`MinOffDone` gates the set branch only, so the compressor may always unload at once and
may not always load at once. That asymmetry is the design.

{{files: benchmarks/manufacturing/g_compressor_cycle/program.xml | benchmarks/manufacturing/g_compressor_cycle/short_cycle.xml | benchmarks/manufacturing/g_compressor_cycle/props.yaml | benchmarks/manufacturing/g_compressor_cycle/mincycle_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/manufacturing/g_compressor_cycle/props.yaml}}

{{record: g_compressor_cycle__program}}

Take `MinOffDone` out of the set branch and you have the short-cycling variant, which is
what a hurried commissioning leaves behind when the timer is inconvenient during testing.

{{predict: g_compressor_cycle__short_cycle | The minimum-off interlock is gone. Does the compressor still refuse to load above the cut-out?}}

`NOT PressHigh` is the tail of the rung in both files, so both prove it. The property
constrains the top of the band and says nothing about the bottom, which is where the
damage happens.

## The discriminator

{{show: benchmarks/manufacturing/g_compressor_cycle/mincycle_check.props.yaml}}

{{record: compressor_mincycle_interlocked}}

{{record: compressor_mincycle_short}}

The interlocked design refutes it: pressure is low, the machine is not loading, and that
is the interlock doing its job. The short-cycling one proves it at k = 2. A proof, here,
is the bad news.

## Reading the whole part at once

{{stat: benchmarks.discriminator|Words}} machines, and the same table in every one:

| | the safety property | the discriminator |
|---|---|---|
| the correct program | `SAFE` | `VIOLATION` |
| the defective program | `SAFE` | `SAFE` |

The left column is what gets written, reviewed, and reported. It is true of both programs
in every pair. The right column is the one that carries information, and in every
case it carries it by failing.

There is a habit buried in this. Engineers write properties that say the machine will not
hurt anybody, and those properties are satisfied by a machine that does nothing at all.
The interesting requirements are the ones about what the machine must still be able to
do: hold the drive down until somebody resets it, refuse a taped button, leave a gap
between two contactors, keep reversing after the beam clears, stay locked out, move duty
to the other pump, wait before restarting. Every one of those is checked by asking for a
counterexample and getting one.
