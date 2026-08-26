# Example 2 — a seal-in latch

The example where the verdict tells you nothing and the encoding tells you everything.

```
ESBMC=/path/to/esbmc ./run.sh
```

## The rung (`sealin.ld`)

```
Start ---| |---+---|/|--- ( Run )      Run := (Start OR Run) AND NOT EStop
               |   EStop
Run   ---| |---+
```

The `Run` contact feeds the coil's own output back in. That is the seal-in: press
Start, release it, the motor keeps running until EStop. The parallel branch is a
wired-OR junction, expressed in PLCopen XML as two `<connection>` elements inside one
`<connectionPointIn>`.

## The property (`props.yaml`)

```yaml
- id: P1
  kind: invariant
  expression: "!(Run && EStop)"
```

The motor must never run while the emergency stop is pressed.

## The verdict, on two builds

| build | verdict |
|---|---|
| v8.4 `61172c6f` | SAFE |
| master `d88a9fa4` | SAFE |

Agreement. A results table would stop here, and it would be misleading.

## What each build actually encoded

**v8.4** emits one assignment per branch, and the second overwrites the first:

```
Run = 1 && Start && !EStop;
Run = 1 && Run   && !EStop;
```

The rung collapses to `Run = Start && !EStop`. There is no latch.

**master** synthesises an accumulator and a previous-scan snapshot:

```
Run__prev = Run                             snapshot of the last scan
pf11 = Run__prev                            the seal-in branch
pf10 = Start                                the Start branch
pf12 = 0
IF pf11 && !EStop  THEN pf12 = 1            (Run_prev AND NOT EStop)
IF pf10 && !EStop  THEN pf12 = 1         OR (Start    AND NOT EStop)
Run = 1 && pf12
```

which is `Run := (Run_prev OR Start) AND NOT EStop`. A genuine seal-in.

## The discriminator

The stated property cannot separate these, because a program with no latch also
satisfies it. So ask something only a real latch refutes: **can `Run` hold while
`Start` is released?**

```yaml
- id: P1
  kind: invariant
  expression: "!Run || Start"      # "Run implies Start"
```

| build | k-induction | meaning |
|---|---|---|
| v8.4 | VERIFICATION SUCCESSFUL | `Run` never outlives `Start`. **No latch was encoded.** |
| master | VERIFICATION FAILED | the latch is real |

master's counterexample is the seal-in doing its job:

```
Start = 1 ; EStop = 0  ->  Run = 1
Start = 0 ; EStop = 0  ->  Run__prev = 1, Run stays 1
```

## The lesson

Two builds agree on the safety verdict. Only one of them verified a seal-in. The
verdict alone could not tell you, and neither could the property, because the property
was insensitive to the very feature the benchmark is named for.

This is why a benchmark's ground truth needs the encoding beside it, not just the
label. It is also why the suite's own `g_seal_in`, marked `validated` on v8.4
evidence, needs rechecking: see `probe/FINDINGS.md`.
