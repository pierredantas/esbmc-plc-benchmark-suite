The seal-in latch is the second circuit every PLC course teaches. It is also where a
verdict starts lying to you.

## The rung

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Start in series, or Run feeding back in parallel, joined and driving a normally closed EStop contact into the Run coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H320"/><path d="M28 98 H140"/><path d="M156 98 H240"/><path d="M240 98 H320"/><path d="M320 52 V98"/><path d="M320 52 H396"/><path d="M412 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M140 86 V110"/><path d="M156 86 V110"/><path d="M396 40 V64"/><path d="M412 40 V64"/><path d="M392 66 L416 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/></g><circle cx="320" cy="52" r="3.5" fill="currentColor"/><circle cx="320" cy="98" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Start</text><text x="148" y="128">Run</text><text x="404" y="32">EStop</text><text x="588" y="32">Run</text></g></svg>

`Run := (Start OR Run) AND NOT EStop`. The coil's own output feeds back through the lower branch. Press Start, release it,
and the motor keeps running until EStop opens the path. In PLCopen XML that junction
is two `<connection>` elements inside one `<connectionPointIn>`, which is a wired OR.

{{files: demo2/sealin.ld | demo2/props.yaml | demo2/latch_check.props.yaml}}

{{code: demo2/sealin.ld}}

## The obvious property

{{show: demo2/props.yaml}}

The motor must never run while the emergency stop is pressed.

{{record: sealin_safety}}

Proved at k = 2, in under a hundredth of a second. A results table would stop here and it
would be misleading.

## The discriminator

Look at the scan body above before reading on.

The front end builds `pf12` out of both branches and reads `Run__prev`, a snapshot taken at
the top of the scan, which gives `Run := (Run_prev OR Start) AND NOT EStop`. That is a
latch, and you can see that it is a latch.

Now notice what the property could not have told you. `!(Run && EStop)` is satisfied by
that encoding, by a plain conjunction with no memory in it, and by a program that never
assigns `Run` at all. A property of this shape cannot separate a latch from a program that
merely never runs the motor while the stop is pressed, so the verdict is compatible with a
front end that dropped the self-hold branch entirely and never told you.

To make that difference a verdict rather than an inspection, ask for something only a real
latch refutes. Can `Run` hold once `Start` is released?

{{show: demo2/latch_check.props.yaml}}

{{record: sealin_latch}}

Read the outcome column before the verdict. The expected result is VIOLATION, because a
working seal-in has to be able to hold `Run` with `Start` back at 0, and the counterexample
is the seal-in doing its job. States 1 to 3 are the first scan, with `Start = 1` and
`EStop = 0` driving `Run` to 1. States 5 to 9 are the next scan, and `Start` has gone back
to 0. `Run__prev` carries the 1 across the scan boundary, `Run` stays up, and the property
falls over.

A front end that had flattened the rung would answer this one `SAFE`, and the `SAFE` would
be sound about the program it built. That is the useful property of a discriminator: it does
not ask the tool to be honest about its own limitations, it asks a question whose answer
differs depending on what the tool actually encoded.

!!! note "Why the run uses k-induction"
    `record.py --mode kinduction` forces it. Under incremental BMC a missing latch comes
    back `unknown` rather than `SAFE`, which is a far weaker statement: no counterexample
    within twenty unwindings, and nothing said about the twenty-first. On a discriminator
    you want the proof, because the point is to make the absence of the latch provable
    rather than merely unwitnessed.

## Why this matters for the suite

The safety verdict was `SAFE` and the benchmark is named for a latch, and nothing about
that verdict established that a latch was ever encoded. The property was insensitive to the
one feature the task is named for.

That is the argument for publishing the encoding beside the label, and it sets a bar for
any task named after a feature: the recorded evidence has to show the front end encoded the
feature, not merely that a tool returned the verdict the task expected.

The bar is not hypothetical. [Lesson 7.9](../two-hand-fb/index.md) is a benchmark that fails
it today, where the front end returns a confident verdict about a function block whose body
never reached the scan loop.
