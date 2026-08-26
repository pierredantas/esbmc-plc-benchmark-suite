The seal-in latch is the second circuit every PLC course teaches. It is also where a
verdict starts lying to you.

## The rung

```
Start ---| |---+---|/|--- ( Run )       Run := (Start OR Run) AND NOT EStop
               |   EStop
Run   ---| |---+
```

The coil's own output feeds back through the lower branch. Press Start, release it,
and the motor keeps running until EStop opens the path. In PLCopen XML that junction
is two `<connection>` elements inside one `<connectionPointIn>`, which is a wired OR.

{{files: demo2/sealin.ld | demo2/props.yaml | demo2/latch_check.props.yaml}}

{{code: demo2/sealin.ld}}

## The obvious property

{{show: demo2/props.yaml}}

The motor must never run while the emergency stop is pressed.

{{record: sealin_safety}}

Both builds prove it, at k = 2, in under a hundredth of a second. A results table
would stop here and it would be misleading.

## The discriminator

Look at the two scan bodies above before reading on.

v8.4 emits two assignments to `Run`, and the second overwrites the first, so the rung
collapses to `Run = Start && !EStop`. No latch. master builds `pf12` out of both
branches and reads `Run__prev`, a snapshot taken at the top of the scan, which gives
`Run := (Run_prev OR Start) AND NOT EStop`.

Both encodings satisfy `!(Run && EStop)`, and so does a program with no memory at
all, which is the whole difficulty: a property this shape cannot separate a latch from
a plain conjunction, so you have to ask for something that only a real latch refutes.
Can `Run` hold once `Start` is released?

{{show: demo2/latch_check.props.yaml}}

{{record: sealin_latch}}

Read the outcome column carefully before you read the verdicts. The expected verdict
is VIOLATION, because a working seal-in has to be able to hold `Run` with `Start` back
at 0. v8.4 does not merely fail to find that trace: it proves the trace cannot exist,
at k = 2. The proof is sound about the program v8.4 encoded, and that program has no
latch in it.

master's counterexample is the seal-in doing its job. States 1 to 3 are the first
scan, with `Start = 1` and `EStop = 0` driving `Run` to 1. States 5 to 9 are the next
scan, and `Start` has gone back to 0. `Run__prev` carries the 1 across the scan
boundary, `Run` stays up, and the property falls over.

!!! note "Why both runs used k-induction"
    `record.py --mode kinduction` forces it. Under incremental BMC v8.4 returns
    `unknown` here, which is a far weaker statement than a proof: no counterexample
    within twenty unwindings, and nothing said about the twenty-first. On a
    discriminator you want the proof, because the point is to make the absence of the
    latch provable rather than merely unwitnessed.

## Why this matters for the suite

Two builds agreed on the safety verdict. One of them verified a seal-in. Neither the
verdict nor the property could tell you which, because the property was insensitive to
the one feature the benchmark is named for.

That is the argument for publishing the encoding beside the label. It also puts the
suite's own `g_seal_in` in question, because that task carries
`validation_status: validated` on evidence produced by v8.4, and v8.4 encoded no latch
at all for the rung the task is named after. The recheck is in `probe/FINDINGS.md`.
