The fuse in [lesson 3.2](../fuses/index.md) was fifty scans, which is half a second on a
ten millisecond task. An attacker chooses that number, and it costs them nothing to
choose a larger one.

`counter_scalability` is the benchmark that asks what that costs the defender. Five
programs, identical apart from one constant:

```pascal
scan_cnt := scan_cnt + 1;
IF scan_cnt >= 255 THEN        (* 255, 1023, 4095, 16383, 32767 *)
  armed := TRUE;
END_IF;
```

Everything else is the tank from 3.2: the same interlock, the same payload gating, the
same one-line property.

{{files: benchmarks/manufacturing/counter_scalability/bomb_N00255.st | benchmarks/manufacturing/counter_scalability/bomb_N32767.st | benchmarks/manufacturing/counter_scalability/props.yaml}}

## The measurement

Each program was unwound to two scans past its own fuse and handed to ESBMC. Every one
is found. The seconds are the recorded runs below; the condition counts come from
ESBMC's own console output for the same commands.

| fuse | scans unwound | verdict | seconds | verification conditions |
|---|---|---|---|---|
| 255 | 257 | VIOLATION | 1.0 | 15,214 |
| 1,023 | 1,025 | VIOLATION | 1.6 | 60,526 |
| 4,095 | 4,097 | VIOLATION | 6.8 | 241,774 |
| 16,383 | 16,385 | VIOLATION | 80.8 | 966,766 |
| 32,767 | 32,769 | VIOLATION | 393.4 | 1,933,410 |

{{record: counter_scalability__bomb_N00255__viac}}

{{record: counter_scalability__bomb_N32767__viac}}

## Read the two columns

The verification conditions grow **linearly**, about fifty-nine per scan, which is what
you would expect: each scan contributes a fixed slab of constraints and the slabs are
just stacked.

The time does not. Four times the fuse costs between four and twelve times the runtime,
and the last doubling costs five times. Somewhere past a hundred thousand scans this
stops being a benchmark and starts being an overnight job, and a hundred thousand scans
is seventeen minutes of plant time.

Nothing about that is a defect. It is what bounded model checking is: the formula
describes every one of those scans at once, and the solver has to reason about all of
them to conclude anything. The attacker adds a digit to a constant. The defender adds an
order of magnitude to a solve.

## The asymmetry is the point

This is the one place in the suite where the cost of attack and the cost of defense are
directly comparable, and they are not close.

Writing `32767` instead of `255` is one edit and costs nothing to run: the plant does not
care, the scan time does not change, and the program is not larger. Finding it took 393
seconds. A fuse of a million scans is three hours of plant time, entirely
plausible for something meant to survive commissioning, and it is out of reach of this
approach on this hardware.

So a defense that consists of "unwind further" loses by construction. It is a race the
defender can only lose, because the attacker sets the distance.

## What wins instead

You stop reasoning about the counter's value.

The property being checked here says nothing about `scan_cnt`. It says the pump must
never run into a full tank. A proof of that ought not to care whether the fuse is fifty
or fifty million, and it does not have to: an inductive invariant over the program's
state proves the property for **every** scan at once, rather than for a fixed number of
them one after another. That is what `--k-induction` does, and it is why the expected-SAFE
tasks throughout this site are proved with it and close at k = 2 regardless of how long
they run.

The catch is that these five benchmarks cannot use it today. They are Structured Text, so
they reach ESBMC only through the C route, where the harness this suite generates is a
bounded `for` loop. A bounded loop has nothing to induct over. Proving an unbounded claim
about them means either a ladder rendering, where the scan loop is genuinely `while
(true)`, or a harness that models the scan loop as unbounded and lets k-induction work.

That is honest open work rather than a limitation of ESBMC, and it is the most useful
thing anybody could add to this suite next.

## A defect this benchmark found in the tooling

The catalog's own records for these five said `unknown` until today, and the reason was
mine, not the benchmark's.

The via-C adapter ran expected-VIOLATION tasks with `--incremental-bmc`. That mode raises
its bound step by step and stops when its forward condition cannot prove the loop has
been fully covered, reporting UNKNOWN. On a bounded harness the forward condition has
nothing useful to say, so the run gave up in two seconds while plain unwinding found the
same violation in one.

```
--incremental-bmc --unwind 259   ->  VERIFICATION UNKNOWN   2.7 s
--unwind 259                     ->  VERIFICATION FAILED    0.9 s
```

The adapter now uses plain unwinding for this route, and the five records above are the
result. Worth recording because it is the exact failure this part is about: a verdict of
`unknown` that looks like a hard limit and is actually a wrong flag.
