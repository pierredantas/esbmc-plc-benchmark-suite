A power press with two palm buttons a shoulder's width apart. Hold both and the ram
comes down. Let either one go and it stops. The reasoning is old and simple: while both
hands are on the buttons, neither is in the die.

ISO 13851 grades these devices. A Type I control is the plain conjunction of the two
signals. Types II and III add anti-tie-down, which is the requirement that both
actuators be released together before a new cycle can start, so that taping one down
buys the operator nothing.

## The rungs

<svg class="diagram" viewBox="0 0 700 340" role="img" aria-label="Three rungs: normally closed left hand and normally closed right hand in series drive both off; armed or both off in parallel, gated by normally closed stroke, latches armed; stroke or armed in parallel, then left hand and right hand in series, drives stroke"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V322"/><path d="M672 18 V322"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H270"/><path d="M286 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M136 66 L160 38"/><path d="M270 40 V64"/><path d="M286 40 V64"/><path d="M266 66 L290 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 128 H140"/><path d="M156 128 H320"/><path d="M28 158 H140"/><path d="M156 158 H320"/><path d="M320 128 V158"/><path d="M320 128 H396"/><path d="M412 128 H571"/><path d="M605 128 H672"/><path d="M140 116 V140"/><path d="M156 116 V140"/><path d="M140 146 V170"/><path d="M156 146 V170"/><path d="M396 116 V140"/><path d="M412 116 V140"/><path d="M392 142 L416 114"/><path d="M578 114 Q564 128 578 142"/><path d="M598 114 Q612 128 598 142"/><path d="M28 224 H140"/><path d="M156 224 H320"/><path d="M28 254 H140"/><path d="M156 254 H320"/><path d="M320 224 V254"/><path d="M320 224 H396"/><path d="M412 224 H460"/><path d="M476 224 H571"/><path d="M605 224 H672"/><path d="M140 212 V236"/><path d="M156 212 V236"/><path d="M140 242 V266"/><path d="M156 242 V266"/><path d="M396 212 V236"/><path d="M412 212 V236"/><path d="M460 212 V236"/><path d="M476 212 V236"/><path d="M578 210 Q564 224 578 238"/><path d="M598 210 Q612 224 598 238"/></g><circle cx="320" cy="128" r="3.5" fill="currentColor"/><circle cx="320" cy="158" r="3.5" fill="currentColor"/><circle cx="320" cy="224" r="3.5" fill="currentColor"/><circle cx="320" cy="254" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">LH</text><text x="278" y="32">RH</text><text x="588" y="32">BothOff</text><text x="148" y="108">Armed</text><text x="148" y="188">BothOff</text><text x="404" y="108">Stroke</text><text x="588" y="108">Armed</text><text x="148" y="204">Stroke</text><text x="148" y="284">Armed</text><text x="404" y="204">LH</text><text x="468" y="204">RH</text><text x="588" y="204">Stroke</text></g></svg>

`BothOff := NOT LH AND NOT RH`, `Armed := (Armed OR BothOff) AND NOT Stroke`,
`Stroke := (Stroke OR Armed) AND LH AND RH`. `Armed` is the memory of a release. It
comes up when both buttons are off, and the
stroke rung consumes it. Once a cycle has started, nothing rearms the press until the
operator takes both hands off, which is the behavior the standard is asking for.

{{files: benchmarks/manufacturing/g_two_hand/program.xml | benchmarks/manufacturing/g_two_hand/type_i.xml | benchmarks/manufacturing/g_two_hand/props.yaml | benchmarks/manufacturing/g_two_hand/tiedown_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/manufacturing/g_two_hand/props.yaml}}

The ram descends only while both actuators are held. That is the sentence in the risk
assessment, and the checker proves it.

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
