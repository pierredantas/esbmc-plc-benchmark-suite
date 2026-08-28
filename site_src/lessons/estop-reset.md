Twist the mushroom button back out. Does the conveyor start moving?

On a machine built to ISO 13850 it must not. Releasing the actuator clears the stop
command, and nothing more; the safety function comes back only when somebody presses a
separate reset button, sited where they can see the whole hazard zone. ISO 13849-1 calls
this a manual reset. The clause exists because the person who pressed the button is
often not the person standing in the machine.

## The rungs

```
Reset_prev ---| |---|/|--- ( ResetEdge )     ResetEdge := Reset_prev AND NOT Reset
                   Reset

Safe ---------| |---+---|/|--- ( Safe )      Safe := (Safe OR ResetEdge) AND NOT EStop
ResetEdge ----| |---+   EStop

Safe ---------| |---| |---|/|--- ( Run )     Run := Safe AND Start AND NOT EStop
                   Start  EStop

Reset --------| |--- ( Reset_prev )          Reset_prev := Reset
```

The reset is taken on the falling edge, when the button comes back up. A reset that has
been bridged with a jumper, or taped down by an operator who got tired of walking to it,
then restores nothing at all. That is the whole point of the word "monitored".

`EStop` also breaks the drive rung directly, not only through `Safe`. Real stop circuits
are wired that way, and it happens to make the property below independent of the order
the rungs run in, which lesson 1.5 shows is not the order the file specifies.

{{files: benchmarks/motor_control/g_estop_reset/program.xml | benchmarks/motor_control/g_estop_reset/auto_reset.xml | benchmarks/motor_control/g_estop_reset/props.yaml | benchmarks/motor_control/g_estop_reset/restart_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/motor_control/g_estop_reset/props.yaml}}

The drive is never energized while the button is in. It is the requirement a reviewer
asks for, it is true, and both builds discharge it at k = 2.

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
