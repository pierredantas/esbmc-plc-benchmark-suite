A wet well with two pumps in it. Level rises, a pump runs, level falls, the pump stops.
Duty-standby means one runs at a time so the other stays in reserve, and alternation
means duty changes hands each cycle so that both pumps get used. Skip the alternation and
you own a standby pump nobody has started since commissioning, which is the pump you find
out about on the night the duty one fails.

This is also the first benchmark in this part that the checker cannot finish.

## The rungs

<svg class="diagram" viewBox="0 0 700 400" role="img" aria-label="Four rungs: call or level high in parallel, gated by normally closed level low, latches call; duty with normally closed level low in series, in parallel with normally closed duty with level low in series, drives duty; call and normally closed duty drive pump A; call and duty drive pump B"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V382"/><path d="M672 18 V382"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H320"/><path d="M28 82 H140"/><path d="M156 82 H240"/><path d="M240 82 H320"/><path d="M320 52 V82"/><path d="M320 52 H396"/><path d="M412 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M140 70 V94"/><path d="M156 70 V94"/><path d="M396 40 V64"/><path d="M412 40 V64"/><path d="M392 66 L416 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 158 H140"/><path d="M156 158 H240"/><path d="M256 158 H320"/><path d="M28 188 H140"/><path d="M156 188 H240"/><path d="M256 188 H320"/><path d="M320 158 V188"/><path d="M320 158 H571"/><path d="M605 158 H672"/><path d="M140 146 V170"/><path d="M156 146 V170"/><path d="M236 146 L260 174"/><path d="M140 176 V200"/><path d="M156 176 V200"/><path d="M136 200 L160 172"/><path d="M578 144 Q564 158 578 172"/><path d="M598 144 Q612 158 598 172"/><path d="M28 254 H140"/><path d="M156 254 H270"/><path d="M286 254 H571"/><path d="M605 254 H672"/><path d="M140 242 V266"/><path d="M156 242 V266"/><path d="M270 242 V266"/><path d="M286 242 V266"/><path d="M266 268 L290 240"/><path d="M578 240 Q564 254 578 268"/><path d="M598 240 Q612 254 598 268"/><path d="M28 322 H140"/><path d="M156 322 H270"/><path d="M286 322 H571"/><path d="M605 322 H672"/><path d="M140 310 V334"/><path d="M156 310 V334"/><path d="M270 310 V334"/><path d="M286 310 V334"/><path d="M578 308 Q564 322 578 336"/><path d="M598 308 Q612 322 598 336"/></g><circle cx="320" cy="52" r="3.5" fill="currentColor"/><circle cx="320" cy="82" r="3.5" fill="currentColor"/><circle cx="320" cy="158" r="3.5" fill="currentColor"/><circle cx="320" cy="188" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Call</text><text x="148" y="112">LevelHigh</text><text x="404" y="32">LevelLow</text><text x="588" y="32">Call</text><text x="148" y="138">Duty</text><text x="248" y="138">LevelLow</text><text x="148" y="218">Duty</text><text x="248" y="218">LevelLow</text><text x="588" y="138">Duty</text><text x="148" y="234">Call</text><text x="278" y="234">Duty</text><text x="588" y="234">PumpA</text><text x="148" y="302">Call</text><text x="278" y="302">Duty</text><text x="588" y="302">PumpB</text></g></svg>

`Call := (Call OR LevelHigh) AND NOT LevelLow`. `Duty := (Duty AND NOT LevelLow) OR (NOT
Duty AND LevelLow)`. `PumpA := Call AND NOT Duty`, `PumpB := Call AND Duty`. The `Duty`
rung is an exclusive or against `LevelLow`, so the selector flips every time the well
empties.

{{files: benchmarks/water_treatment/g_pump_alternation/program.xml | benchmarks/water_treatment/g_pump_alternation/stuck_duty.xml | benchmarks/water_treatment/g_pump_alternation/props.yaml | benchmarks/water_treatment/g_pump_alternation/alternation_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/water_treatment/g_pump_alternation/props.yaml}}

{{record: g_pump_alternation__program}}

Now the defect, and it is a real one rather than an invented one. Somebody wires the
toggle's set branch in series instead of in parallel, so the rung reads `Duty := Duty AND
LevelLow`. Duty starts at zero and stays there for the life of the installation.

{{predict: g_pump_alternation__stuck_duty | Duty never leaves the lead pump. Do the two pumps still exclude each other?}}

They do, and more strictly than before, because one of them never runs at all. A station
that has quietly become single-pump satisfies every mutual-exclusion property you can
write about it.

## The discriminator, and where it stops

Ask about the selector rather than about pump B.

{{show: benchmarks/water_treatment/g_pump_alternation/alternation_check.props.yaml}}

{{record: pump_alternation_working}}

One scan with `LevelLow = 1` and duty has moved. Both builds find it.

{{record: pump_alternation_stuck}}

Neither build can discharge the same property on the stuck variant, and that is the
recorded result. The property is inductive by inspection: assume `Duty` is false, and
`Duty AND LevelLow` is false, so it stays false. k-induction should close it at k = 1.

We cut the program down to find out where the difficulty was, and it is not the program.
One rung, one input, one coil is enough to reproduce it:

```
Duty ---| |---| |--- ( Duty )     Duty := Duty AND LevelLow
             LevelLow
```

Against `!Duty`, the checker reports `The inductive step is unable to prove the property`
at every k from 2 to 50 and finish with `VERIFICATION UNKNOWN`. A bounded run to depth 20
finds no counterexample and fails only on the unwinding assertion, which is what an
infinite scan loop always does. So there is no trace refuting the property within 20
scans, and no proof either.

## What to take from it

Every pair before this one had a discriminator that refuted on one program and proved on
the other. That symmetry is what makes the pair informative, and it depends
on the checker being able to answer both halves. Here it answers one.

The pair is still worth shipping. It records what the tool did rather than what we wanted
it to do, the working alternation is confirmed, and the gap has a
five-line reproducer attached to it. An `unknown` that you can hand to somebody is a
better artifact than a benchmark quietly reshaped until the checker agreed with it.
