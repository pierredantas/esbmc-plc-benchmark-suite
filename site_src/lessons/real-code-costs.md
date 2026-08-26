Six benchmarks in this catalog come from SWaT, a working water treatment testbed, by way
of the PLC_Defuser dataset. Twelve program variants, legitimate and malicious in pairs,
and the plant they control is real.

**Not one of them has a verdict on this site.**

This lesson is why, measured rather than asserted, because the reasons are the honest
answer to what it costs to verify code that arrived from somewhere else.

## What the programs are

Each file holds four POUs and a configuration that runs three of them as separate tasks:

```
FUNCTION_BLOCK check_pumps
PROGRAM PLC1        level, request  ->  pumps_state, pumps, valve
PROGRAM PLC3        level           ->  pump
PROGRAM PLC2        level           ->  request

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms, PRIORITY := 0);
    ...
    PROGRAM instance0 WITH task0 : PLC1;
    PROGRAM instance1 WITH task1 : PLC2;
    PROGRAM instance2 WITH task2 : PLC3;
```

Three controllers, one plant, wired to each other: `PLC2` computes a `request` that
`PLC1` consumes. Nothing in Parts 1 to 3 looks remotely like this, where every benchmark
was a single program with a handful of Booleans.

{{files: benchmarks/water_treatment/st_swat_timer1/sleg_timer1_0.st | benchmarks/water_treatment/st_swat_timer1/smal_timer1_0.st | benchmarks/water_treatment/st_swat_timer1/props.yaml}}

## The bomb

Inside the function block, in the malicious variant:

```pascal
i := 0;
while i < 4 do
    OUT := FALSE;
end_while;
```

The same shape as [lesson 3.4](../non-termination/index.md): a loop whose counter is never
advanced, so the scan never completes. What makes this one different is where the trigger
sits.

```pascal
TON0(IN := TRUE, PT := T#10000s);
check_pumps0(EN := TON0.Q, IN1 := level, IN2 := high_1);
```

The function block is enabled by an on-delay timer with a preset of **ten thousand
seconds**. The controller runs correctly for close to three hours and then stops
responding.

## Obstacle 1: ten of twelve are not IEC

```pascal
VAR
  exc : __SYSTEM.ExceptionCode;
END_VAR
__TRY
  real_value := IN1 - 5;
__CATCH(exc)
  real_value := 0;
__ENDTRY;
```

`__TRY`, `__CATCH` and `__SYSTEM.ExceptionCode` are CODESYS extensions. They are not in
IEC 61131-3, and MatIEC rejects them at the declaration:

```
error: invalid specification in variable declaration.
```

Ten of the twelve files use them. Only the `timer1` pair is portable Structured Text, and
those two do compile.

This is not a defect in anything. It is what production code looks like: written against a
vendor's toolchain, using that vendor's error handling, because the plant had to work.

## Obstacle 2: four POUs and three tasks

The via-C harness this suite generates instantiates one POU and drives one scan loop.
These files need three program instances stepped together, with `PLC2`'s output reaching
`PLC1`'s input in whatever order the configuration implies.

That is a real extension rather than a hard problem, and it is the one obstacle here that
straightforward work would remove.

## Obstacle 3: the trigger is behind a clock

MatIEC compiles `TON` against a real time source:

```c
__DECLARE_VAR(TIME,CURRENT_TIME)
```

Nothing in a generated harness advances that clock. Leave it alone and `TON0.Q` never
rises, `check_pumps0` is never enabled, and the bomb is unreachable no matter how deep the
search goes. Verifying this program means modeling time, not just scans.

## Obstacle 4: and then the depth

Suppose obstacles one to three were solved. The preset is `T#10000s` on a `T#20ms` task:

```
10000 s / 20 ms = 500,000 scans
```

[Lesson 3.3](../scale/index.md) measured a 32,767-scan fuse at 393 seconds of solving.
This one is fifteen times deeper, and the cost was growing faster than linearly at that
point.

The attacker wrote `T#10000s`. It took no longer to type than `T#1s`.

## What would actually work

Not a deeper bound. Two things, both of which the suite already demonstrates elsewhere.

**The ladder route's scan watchdog.** [Lesson 3.4](../non-termination/index.md) catches
this exact payload in the eight `g_tank_*` benchmarks, in milliseconds, because it does
not chase the trigger at all. It instruments the loop and asserts the iteration count
stays in budget, which is true or false regardless of how the program got there. Those
eight have verdicts on this site and these six do not, and the difference is the
instrument rather than the difficulty.

**An inductive argument.** A proof that never mentions the timer's value holds for every
scan at once, which is what `--k-induction` does for the expected-SAFE tasks throughout
this site, closing at k = 2 whatever the program's horizon.

Both amount to the same advice: stop reasoning about when the trigger fires, and reason
about what the program does when it does.

## Why these stay in the catalog

A benchmark suite that only contains programs its tools can verify is a suite that
measures nothing. These six are the ones that say what the gap actually is: not
"Structured Text is unsupported", but four specific obstacles, three of which are ordinary
engineering and one of which is a genuine research question.

They also keep the rest of the catalog honest. Everything in Parts 1 to 3 is small enough
to hold in your head, and a reader who saw only those would leave with a very comfortable
impression of how much of a real plant a model checker can currently take on.
