A power press with two palm buttons a shoulder's width apart. Hold both and the ram
comes down. Let either one go and it stops. The reasoning is old and simple: while both
hands are on the buttons, neither is in the die.

ISO 13851 grades these devices. A Type I control is the plain conjunction of the two
signals. Types II and III add anti-tie-down, which is the requirement that both
actuators be released together before a new cycle can start, so that taping one down
buys the operator nothing.

## The rungs

```
LH ---|/|---|/|--- ( BothOff )              BothOff := NOT LH AND NOT RH
           RH

Armed ---| |---+---|/|--- ( Armed )         Armed := (Armed OR BothOff) AND NOT Stroke
BothOff -| |---+   Stroke

Stroke --| |---+---| |---| |--- ( Stroke )  Stroke := (Stroke OR Armed) AND LH AND RH
Armed ---| |---+   LH    RH
```

`Armed` is the memory of a release. It comes up when both buttons are off, and the
stroke rung consumes it. Once a cycle has started, nothing rearms the press until the
operator takes both hands off, which is the behavior the standard is asking for.

{{files: benchmarks/manufacturing/g_two_hand/program.xml | benchmarks/manufacturing/g_two_hand/type_i.xml | benchmarks/manufacturing/g_two_hand/props.yaml | benchmarks/manufacturing/g_two_hand/tiedown_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/manufacturing/g_two_hand/props.yaml}}

The ram descends only while both actuators are held. That is the sentence in the risk
assessment, and both builds prove it.

{{record: g_two_hand__program}}

In the Type I variant the stroke rung reads `Stroke := LH AND RH` and no longer looks at
`Armed` at all, so nothing in the program remembers a release.

{{predict: g_two_hand__type_i | This is the device you can defeat with a strip of tape. Does the property above still hold?}}

Of course it does. `Stroke` is literally the conjunction, so the implication is trivial.
The property is true of the device the standard classifies as defeatable, and it is true
for a stronger reason than it is true of the good one.

## The discriminator

Tape changes nothing about the signals. It only changes how they got there. So ask the
question tape cannot survive: does holding both buttons always produce a stroke?

{{show: benchmarks/manufacturing/g_two_hand/tiedown_check.props.yaml}}

{{record: twohand_tiedown_ii}}

`LH = 1`, `RH = 1`, and the press stays up. That trace is the tie-down attempt: both
signals present, no release behind them, and a Type II device declining to run.

{{record: twohand_tiedown_i}}

The Type I device proves the property at k = 2, which is the formal statement of "both
signals high is sufficient", and therefore of "tape is sufficient".

## What the model does not carry

ISO 13851 also requires the two actuations to fall within 0.5 s of each other. Nothing
above expresses that, because the scan model here has no clock in it and the property
language speaks only about the current scan. The synchrony requirement is real and this
benchmark does not check it.

Worth being blunt about a second gap. A two-hand control that a risk assessment counts on
is wired to a safety relay, not to standard PLC inputs, because the relay is what gives
the redundancy and diagnostic coverage the performance level needs. What is verified here
is the program's logic, which is one layer of the argument and not the argument.
