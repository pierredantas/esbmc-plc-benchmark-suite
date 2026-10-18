Tony Kuphaldt's *Lessons In Electric Circuits* teaches ladder logic the way most people
first meet it: a forward/reverse starter with a cross-interlock, a fail-safe stop wired
through normally-closed contacts. Both rungs are correct relay diagrams, drawn the way
an electrician reads them, contacts and coils resolving together. Transcribe them into a
scanned PLC program and both stay safe, but for a reason the relay diagram never needed,
and an earlier version of the verifier got that reason wrong.

## The interlock, as drawn

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a forward start in series with a normally closed reverse-run contact drives the forward contactor; a reverse start in series with a normally closed forward-run contact drives the reverse contactor"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H140"/><path d="M156 110 H300"/><path d="M316 110 H571"/><path d="M605 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M300 98 V122"/><path d="M316 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">START_FWD</text><text x="308" y="32">M2_REV (NC)</text><text x="588" y="32">M1_FWD</text><text x="148" y="90">START_REV</text><text x="308" y="90">M1_FWD (NC)</text><text x="588" y="90">M2_REV</text></g></svg>

`M1_FWD := START_FWD AND NOT M2_REV`, `M2_REV := START_REV AND NOT M1_FWD`. On a relay
panel this is airtight: the two coils and the two auxiliary contacts settle together, so
whichever direction's demand contact closes first, its own coil energizes and the other
direction's normally-closed contact opens before the second coil ever gets a chance.
There is no "before". Contacts and coils are simultaneous.

{{files: benchmarks/motor_control/g_fwd_rev_interlock/fwd_rev_interlock.xml | benchmarks/motor_control/g_fwd_rev_interlock/props.yaml}}

## The property, and the proof that it holds

{{show: benchmarks/motor_control/g_fwd_rev_interlock/props.yaml}}

{{record: g_fwd_rev_interlock__fwd_rev_interlock}}

k-induction proves the property at k = 2, and ESBMC proves it again, also at k = 2, on the C
that MatIEC generates from the same file. Two independent routes, one answer: the two
contactors are never closed together at the end of a scan.

## What the scan cycle changes

A scanned program cannot evaluate two coils at once, so it evaluates them in order. The
forward rung is drawn above the reverse rung, the runtime takes the drawing order, and the
reverse rung's normally-closed `M1_FWD` contact reads the value the forward rung wrote a
moment earlier in the same scan. Press both start buttons on one scan with the motor
stopped: the forward coil energizes, and the reverse rung sees it and stays off. The
interlock holds from the very first scan.

This benchmark used to carry the opposite label. An earlier ESBMC LD front end read every
coil's previous-scan value, so on the first scan both interlock contacts saw false and
both coils came on together. That counterexample was an artifact of the translator, not
of the program ([esbmc/esbmc#7352](https://github.com/esbmc/esbmc/issues/7352), fixed in
[#8036](https://github.com/esbmc/esbmc/pull/8036)), and the label was corrected once two
routes agreed that the property holds.

{{predict: g_fwd_rev_interlock__fwd_rev_interlock | If the reverse rung were drawn above the forward rung, which contactor would win when both start buttons are pressed on one scan with the motor stopped?}}

The reverse one. Safety does not depend on the order, but priority does. A relay panel
gives the race to whichever contact physically closes first; a scanned program gives it to
whichever rung comes first in the drawing, every time. That is a design decision the
transcription makes silently, and it is worth stating in the program's documentation.

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

Two textbook rungs, two different lessons. The interlock shows that a verifier's model of
the scan cycle has to match the runtime's: a translator that read previous-scan values
reported a hazard the program does not have, and the fix was in the tool, not in the
ladder. The fail-safe latch shows a natural, correct way to state a safety property that
the property language cannot parse. Neither would have surfaced from reading the ladder
diagram alone, and both surfaced from trying to prove something about it.

[Reproducing](../../reproducing.md) has the commands.
