Tony Kuphaldt's *Lessons In Electric Circuits* teaches ladder logic the way most people
first meet it: a forward/reverse starter with a cross-interlock, a fail-safe stop wired
through normally-closed contacts. Both rungs are correct relay diagrams, drawn the way
an electrician reads them, contacts and coils resolving together. Transcribe them into a
scanned PLC program and one of the two stops being correct, not because the transcription
was careless, but because a scan cycle is not a relay panel.

## The interlock, as drawn

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a forward start in series with a normally closed reverse-run contact drives the forward contactor; a reverse start in series with a normally closed forward-run contact drives the reverse contactor"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H140"/><path d="M156 110 H300"/><path d="M316 110 H571"/><path d="M605 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M300 98 V122"/><path d="M316 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">START_FWD</text><text x="308" y="32">M2_REV (NC)</text><text x="588" y="32">M1_FWD</text><text x="148" y="90">START_REV</text><text x="308" y="90">M1_FWD (NC)</text><text x="588" y="90">M2_REV</text></g></svg>

`M1_FWD := START_FWD AND NOT M2_REV`, `M2_REV := START_REV AND NOT M1_FWD`. On a relay
panel this is airtight: the two coils and the two auxiliary contacts settle together, so
whichever direction's demand contact closes first, its own coil energizes and the other
direction's normally-closed contact opens before the second coil ever gets a chance.
There is no "before". Contacts and coils are simultaneous.

{{files: benchmarks/motor_control/g_fwd_rev_interlock/fwd_rev_interlock.xml | benchmarks/motor_control/g_fwd_rev_interlock/props.yaml}}

## The property, and the proof it fails

{{show: benchmarks/motor_control/g_fwd_rev_interlock/props.yaml}}

{{record: g_fwd_rev_interlock__fwd_rev_interlock}}

Read the trace. `START_FWD` and `START_REV` come up true together on the first scan,
`STOP` is false, and both `M1_FWD` and `M2_REV` follow. The interlock a relay panel
enforces for free costs a PLC its first scan.

## Why the scan cycle breaks it

A scanned program cannot evaluate two coils simultaneously. Somewhere in program order,
`M1_FWD` is computed before `M2_REV`, or after it, and whichever contact reads the other
coil's value reads last scan's value, because this scan's has not been computed yet. The
front end's own encoding makes the dependency explicit:

```text
ASSIGN M1_FWD__prev = M1_FWD;
ASSIGN M2_REV__prev = M2_REV;
...
ASSIGN M1_FWD = START_FWD && !M2_REV__prev;
...
ASSIGN M2_REV = START_REV && !M1_FWD__prev;
```

On scan 1, `M1_FWD__prev` and `M2_REV__prev` both start false, because nothing has run
yet. Press both start buttons in the same instant, on the same scan, and neither
interlock contact has anything to block on. From scan 2 onward the interlock does exactly
what the diagram promises. The gap is one scan wide and it is enough.

{{predict: g_fwd_rev_interlock__fwd_rev_interlock | If START_FWD and START_REV are asserted one scan apart rather than together, does the property still fail?}}

It does not. Whichever coil's `__prev` value updates first is read by the other rung on
the following scan, and the interlock closes normally. The counterexample above needs the
exact coincidence of both starts landing in the same scan, which is a real input a
maintenance panel with two buttons under two thumbs can produce, and a fault the relay
original never had to survive.

A same-scan mutual exclusion, `M1_FWD := START_FWD AND NOT START_REV AND NOT M2_REV`,
closes the gap by making each direction's own demand block the other outright rather than
only through the other coil's settled state. That is a different rung from the one the
textbook draws, which is the point: the transcription is faithful, and faithful is not
the same as safe once the medium changes.

## The fail-safe latch, and a property that would not parse

<svg class="diagram" viewBox="0 0 700 90" role="img" aria-label="A start contact in parallel with a run seal-in contact, in series with normally closed thermal-overload and stop contacts, drives the run coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V72"/><path d="M672 18 V72"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 32 H140"/><path d="M156 32 H300"/><path d="M316 32 H430"/><path d="M446 32 H571"/><path d="M605 32 H672"/><path d="M140 20 V44"/><path d="M156 20 V44"/><path d="M300 20 V44"/><path d="M316 20 V44"/><path d="M430 20 V44"/><path d="M446 20 V44"/><path d="M28 58 H140"/><path d="M156 58 H300"/><path d="M136 60 L160 30"/></g><g fill="currentColor" font-size="12" text-anchor="middle"><text x="148" y="14">START</text><text x="308" y="14">THERMAL_OVL (NC)</text><text x="438" y="14">STOP (NC)</text><text x="588" y="14">MOTOR_RUN</text><text x="148" y="72">MOTOR_RUN</text></g></svg>

`MOTOR_RUN := (START OR MOTOR_RUN) AND THERMAL_OVERLOAD_NC AND STOP_NC`. Both guard
contacts are wired normally-closed, so a broken wire or a tripped overload reads as
false and drops the seal-in the same way an active stop command would. This rung has no
scan-order dependency: nothing here reads another coil's value, so there is no `__prev`
to get stale.

{{files: benchmarks/motor_control/g_failsafe_motor_latch/failsafe_motor_latch.xml | benchmarks/motor_control/g_failsafe_motor_latch/props.yaml}}

The property the textbook's own language suggests is an implication: if the
overload contact has opened, the motor must not be running.

```text
!THERMAL_OVERLOAD_NC -> !MOTOR_RUN
```

ESBMC's `--ld-props` parser does not accept it:

```text
ERROR: property 'P1': undeclared variable '!THERMAL_OVERLOAD_NC -> !MOTOR_RUN'
```

Not a spelling problem. `->` is not in the grammar at all, so the whole right-hand side
is swallowed as one malformed identifier. This is a different gap from the IEC-keyword
trap in lesson 1.3's [`NOT`/`AND` rejection](../interlock/index.md), which is about
spelling an operator the parser does have; `->` is an operator the parser does not have,
regardless of spelling, and no other property in this suite had exercised it before this
one.

{{show: benchmarks/motor_control/g_failsafe_motor_latch/props.yaml}}

De Morgan's law rewrites `A -> B` as `!A || B`, so `!THERMAL_OVERLOAD_NC -> !MOTOR_RUN`
becomes `THERMAL_OVERLOAD_NC || !MOTOR_RUN`, the same statement without an implication
in it.

{{record: g_failsafe_motor_latch__failsafe_motor_latch}}

k-induction closes at k = 2. The rewrite is not a weaker property standing in for the
original; it is the same formula, and the equivalence is checkable by hand from the truth
table, which is the standard the workaround has to clear before it goes in the suite
rather than around it.

## What the pair says together

Two textbook rungs, two different ways a formalism-blind transcription can go wrong. One
failure sits in the program: a relay-simultaneity assumption carried into a scan cycle
without checking whether the cycle preserves it. The other sits in the tool: a natural,
correct way to state a safety property that the property language cannot parse. Neither
would have surfaced from reading the ladder diagram alone, and both surfaced from trying
to prove something about it.

[Reproducing](../../reproducing.md) has the commands.
