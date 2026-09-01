Twist the mushroom button back out. Does the conveyor start moving?

On a machine built to ISO 13850 it must not. Releasing the actuator clears the stop
command, and nothing more; the safety function comes back only when somebody presses a
separate reset button, sited where they can see the whole hazard zone. ISO 13849-1 calls
this a manual reset. The clause exists because the person who pressed the button is
often not the person standing in the machine.

## The rungs

<svg class="diagram" viewBox="0 0 700 290" role="img" aria-label="Four rungs: a previous reset sample and normally closed reset drive a reset edge; safe or reset edge in parallel, gated by normally closed EStop, drives safe; safe, start and normally closed EStop drive run; reset drives the previous reset sample"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V272"/><path d="M672 18 V272"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M296 66 L320 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 116 H140"/><path d="M156 116 H320"/><path d="M28 138 H140"/><path d="M156 138 H240"/><path d="M240 138 H320"/><path d="M320 116 V138"/><path d="M320 116 H396"/><path d="M412 116 H571"/><path d="M605 116 H672"/><path d="M140 104 V128"/><path d="M156 104 V128"/><path d="M140 126 V150"/><path d="M156 126 V150"/><path d="M396 104 V128"/><path d="M412 104 V128"/><path d="M392 130 L416 102"/><path d="M578 102 Q564 116 578 130"/><path d="M598 102 Q612 116 598 130"/><path d="M28 194 H140"/><path d="M156 194 H270"/><path d="M286 194 H400"/><path d="M416 194 H571"/><path d="M605 194 H672"/><path d="M140 182 V206"/><path d="M156 182 V206"/><path d="M270 182 V206"/><path d="M286 182 V206"/><path d="M400 182 V206"/><path d="M416 182 V206"/><path d="M578 180 Q564 194 578 208"/><path d="M598 180 Q612 194 598 208"/><path d="M28 252 H140"/><path d="M156 252 H571"/><path d="M605 252 H672"/><path d="M140 240 V264"/><path d="M156 240 V264"/><path d="M578 238 Q564 252 578 266"/><path d="M598 238 Q612 252 598 266"/></g><circle cx="320" cy="116" r="3.5" fill="currentColor"/><circle cx="320" cy="138" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Reset_prev</text><text x="308" y="32">Reset</text><text x="588" y="32">ResetEdge</text><text x="148" y="96">Safe</text><text x="148" y="118">ResetEdge</text><text x="404" y="96">EStop</text><text x="588" y="96">Safe</text><text x="148" y="174">Safe</text><text x="278" y="174">Start</text><text x="408" y="174">EStop</text><text x="588" y="174">Run</text><text x="148" y="232">Reset</text><text x="588" y="232">Reset_prev</text></g></svg>

`ResetEdge := Reset_prev AND NOT Reset`, `Safe := (Safe OR ResetEdge) AND NOT EStop`,
`Run := Safe AND Start AND NOT EStop`, `Reset_prev := Reset`. The reset is taken on the falling edge, when the button comes back up. A reset that has
been bridged with a jumper, or taped down by an operator who got tired of walking to it,
then restores nothing at all. That is the whole point of the word "monitored".

`EStop` also breaks the drive rung directly, not only through `Safe`. Real stop circuits
are wired that way, and it happens to make the property below independent of the order
the rungs run in, which lesson 1.5 shows is not the order the file specifies.

{{files: benchmarks/motor_control/g_estop_reset/program.xml | benchmarks/motor_control/g_estop_reset/auto_reset.xml | benchmarks/motor_control/g_estop_reset/props.yaml | benchmarks/motor_control/g_estop_reset/restart_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/motor_control/g_estop_reset/props.yaml}}

The drive is never energized while the button is in. It is the requirement a reviewer
asks for, it is true, and the checker discharges it at k = 2.

{{record: g_estop_reset__program}}

Now the same property against a program with no reset in it at all, where `Safe` follows
the emergency stop contact directly.

{{predict: g_estop_reset__auto_reset | The reset latch has been deleted, so the drive is available again the moment the button is twisted out. Does `!(Run && EStop)` still hold?}}

It holds. Nothing in that property mentions how the machine comes back, so it cannot
distinguish a monitored reset from a machine that restarts under your hands. Both
programs pass, and one of them is the hazard the clause was written to prevent.

## The discriminator

Ask instead whether the machine is allowed to sit still with the button already out.

{{show: benchmarks/motor_control/g_estop_reset/restart_check.props.yaml}}

{{record: estop_restart_monitored}}

Read the counterexample. It is one state long: `EStop = 0`, and `Safe` is still down. A
trace that short is not a weakness of the property. It is the requirement, arriving in
the first scan, because "stopped with the button released" is precisely the state a
manual reset has to be able to hold.

Against the automatic restart, the same property is provable.

{{record: estop_restart_auto}}

Both builds discharge it at k = 2. The program can never be in the state the standard
requires it to reach, and the proof says so.

## What to take from it

Two programs, one property, one verdict each way. The safety property is true of the
dangerous program; the discriminator is false of the safe one. Neither result is a tool
error, and no amount of running the first property harder would have found the defect.

The general shape recurs through this part. A requirement written as "the machine never
does X" is usually cheap to satisfy by doing nothing, and a program that does nothing
satisfies every property of that form. The requirement worth checking is the one that
says the machine can still be brought to a state you need, and that one has to be
refuted, not proved.

{{files: benchmarks/motor_control/st_estop_reset/estop_reset.st}}

The Structured Text twin carries the same four assignments and reaches the solver
through Beremiz and MatIEC rather than the ladder front end.

{{record: st_estop_reset__estop_reset__viac}}
