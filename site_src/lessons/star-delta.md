A 30 kW pump motor draws six or seven times its rated current if you throw it straight
onto the line. The wye-delta starter is the old answer: run the windings in star while
the rotor gets moving, then reconnect them in delta for normal running. Three contactors,
one changeover, and a hazard everybody in the trade knows. Close star and delta together
and you have shorted the supply through the winding ends.

## The rungs

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a call command and a normally closed star-done contact drive the star contactor; a call command with star-done and dead-time-done in series drives the delta contactor"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M136 66 L160 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H140"/><path d="M156 110 H270"/><path d="M286 110 H400"/><path d="M416 110 H571"/><path d="M605 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M270 98 V122"/><path d="M286 98 V122"/><path d="M400 98 V122"/><path d="M416 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Call</text><text x="588" y="32">Star</text><text x="148" y="90">Call</text><text x="278" y="90">StarDone</text><text x="408" y="90">DeadDone</text><text x="588" y="90">Delta</text></g></svg>

`Star := Call AND NOT StarDone`, `Delta := Call AND StarDone AND DeadDone`. `StarDone` and `DeadDone` come from the changeover timer. The start and stop latch that
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
