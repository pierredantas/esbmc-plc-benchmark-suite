A reciprocating compressor on a receiver, with two pressure switches setting the band.
Pressure falls to the cut-in, the compressor loads; pressure reaches the cut-out, it
unloads. Every workshop has one.

The interlock that matters is not in that description. A compressor motor started too
soon after stopping draws locked-rotor current into windings that have not cooled, and on
a receiver with a leak the cycle can repeat every few seconds. So the load rung carries a
minimum-off term, and the machine sits there for a while doing nothing while the pressure
is already low.

## The rung

```
Load ------| |------------+---|/|--- ( Load )
PressLow --| |---| |------+   PressHigh
              MinOffDone

Load := (Load OR (PressLow AND MinOffDone)) AND NOT PressHigh
```

One rung, one latch. `MinOffDone` gates the set branch only, so the compressor may always
unload at once and may not always load at once. That asymmetry is the design.

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

Seven machines, and the same table in every one:

| | the safety property | the discriminator |
|---|---|---|
| the correct program | `SAFE` | `VIOLATION` |
| the defective program | `SAFE` | `SAFE` |

The left column is what gets written, reviewed, and reported. It is true of both programs
in all seven pairs. The right column is the one that carries information, and in every
case it carries it by failing.

There is a habit buried in this. Engineers write properties that say the machine will not
hurt anybody, and those properties are satisfied by a machine that does nothing at all.
The interesting requirements are the ones about what the machine must still be able to
do: hold the drive down until somebody resets it, refuse a taped button, leave a gap
between two contactors, keep reversing after the beam clears, stay locked out, move duty
to the other pump, wait before restarting. Every one of those is checked by asking for a
counterexample and getting one.
