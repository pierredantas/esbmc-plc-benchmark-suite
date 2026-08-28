A wet well with two pumps in it. Level rises, a pump runs, level falls, the pump stops.
Duty-standby means one runs at a time so the other stays in reserve, and alternation
means duty changes hands each cycle so that both pumps get used. Skip the alternation and
you own a standby pump nobody has started since commissioning, which is the pump you find
out about on the night the duty one fails.

This is also the first benchmark in this part that the checker cannot finish.

## The rungs

```
Call ------| |---+---|/|--- ( Call )        Call := (Call OR LevelHigh) AND NOT LevelLow
LevelHigh -| |---+   LevelLow

Duty ------| |---|/|---+--- ( Duty )        Duty := (Duty AND NOT LevelLow)
                LevelLow |                       OR (NOT Duty AND LevelLow)
Duty -----|/|---| |-----+
               LevelLow

Call ------| |---|/|--- ( PumpA )           PumpA := Call AND NOT Duty
                Duty

Call ------| |---| |--- ( PumpB )           PumpB := Call AND Duty
                Duty
```

The `Duty` rung is an exclusive or against `LevelLow`, so the selector flips every time
the well empties.

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
