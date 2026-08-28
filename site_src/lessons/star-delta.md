A 30 kW pump motor draws six or seven times its rated current if you throw it straight
onto the line. The wye-delta starter is the old answer: run the windings in star while
the rotor gets moving, then reconnect them in delta for normal running. Three contactors,
one changeover, and a hazard everybody in the trade knows. Close star and delta together
and you have shorted the supply through the winding ends.

## The rungs

```
Call ---| |---|/|--- ( Star )              Star := Call AND NOT StarDone
             StarDone

Call ---| |---| |---| |--- ( Delta )       Delta := Call AND StarDone AND DeadDone
            StarDone DeadDone
```

`StarDone` and `DeadDone` come from the changeover timer. The start and stop latch that
drives `Call` sits upstream and is the subject of lesson 1.4, so it is deliberately not
in this file; two rungs is the whole of the contactor selection.

{{files: benchmarks/motor_control/g_star_delta/program.xml | benchmarks/motor_control/g_star_delta/no_deadtime.xml | benchmarks/motor_control/g_star_delta/props.yaml | benchmarks/motor_control/g_star_delta/deadtime_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/motor_control/g_star_delta/props.yaml}}

{{record: g_star_delta__program}}

Star carries `NOT StarDone` and delta carries `StarDone`, so exclusion is structural and
the proof is immediate. Now delete the dead-time term, so that delta closes on the same
signal that opens star.

{{predict: g_star_delta__no_deadtime | Delta now closes the instant the star time expires. Are the two commands still mutually exclusive?}}

They are. One rung has the contact and the other has its complement, and that is all
mutual exclusion of the two coils ever asked for.

## The discriminator

An open-transition starter opens star, waits for the arc to clear, and only then closes
delta. During that wait the motor is called for and neither contactor is in. The window is
deliberate. Ask whether it exists.

{{show: benchmarks/motor_control/g_star_delta/deadtime_check.props.yaml}}

{{record: stardelta_deadtime_open}}

{{record: stardelta_deadtime_closed}}

The starter with a dead time refutes it. The one without proves it at k = 2, which is the
formal way of saying the second contactor pulls in on the same scan the first drops.

## The honest caveat

`!(Star && Delta)` is a statement about two program variables. A contactor is not one.
It carries a drop-out time of some tens of milliseconds, and the arc across its contacts
outlives the coil current by long enough that two commands which never overlap anywhere
in the model can still put two sets of contacts in circuit at the same instant on the
panel.

This is the part of the argument formal verification does not reach, and pretending
otherwise is how a proof becomes a liability. What the run above establishes is that the
program does not command the overlap. Whether the hardware permits it is a question for
the contactor's data sheet and the mechanical interlock bolted between the two blocks.
