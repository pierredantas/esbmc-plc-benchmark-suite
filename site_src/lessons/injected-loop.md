The first technique appends a few lines to a function block that is already in the program
and already doing useful work. Nothing is renamed, nothing is deleted, and the block's
existing behavior is untouched.

## The pair

{{files: benchmarks/water_treatment/g_tank_assignment/legitimate_lassignment.xml | benchmarks/water_treatment/g_tank_assignment/malicious_massignment.xml | benchmarks/water_treatment/g_tank_assignment/props.yaml}}

Both files declare three POUs: a `program0` with a ladder body, and two function blocks,
`valves_handler` and `stop_cycle`, whose bodies are Structured Text. The ladder is
identical in both, and the entire difference is ten lines at the end of `valves_handler`.

```
i:=0;
if real_value = 25 then
  while i<3 do
     OUT_MV2 := FALSE;
     OUT_MV1 := TRUE;
      i:=1;
  end_while;
end_if;
```

Read it as a maintainer would. It opens the fill valve and closes the drain, which is a
thing this block does in two other places, so the body of the loop is unremarkable, the
guard names an entirely plausible level, and even the indentation matches the rest of the
file apart from one stray space.

The defect is `i`. It starts at zero, the loop runs while `i` is under three, and the body
sets it to one. One is less than three, so it is set to one again, and again, which
means the counter is assigned on every pass and never advances at all, a bug pattern so
ordinary that it reads as a mistake rather than as a weapon.

## The corrected level, not the raw one

The guard is worth a second look, because it does not test the sensor. It tests
`real_value`, which the block computed earlier as `IN1 - 5`.

So the input that fires this is `IN1 = 30`, not `IN1 = 25`. An analyst grepping the
program for the constant in the trigger finds `25` and looks for a level of 25. The level
that does it is 30, and the arithmetic that connects them sits forty lines earlier in a
different statement.

## The legitimate half

{{record: g_tank_assignment__legitimate_lassignment}}

Proved on both builds. The scan loop terminates, so the property holds, and k-induction
closes it without a bound.

## The malicious half

{{record: g_tank_assignment__malicious_massignment}}

Refuted on both builds in under four hundredths of a second.

The counterexample is the part to read closely:

```
valves_handler0__IN1        = 5
valves_handler0__real_value = 0
valves_handler0__IN1        = 30
valves_handler0__real_value = 25
```

Two scans. In the first the tank reads 5 and the corrected value is 0, so the program
behaves exactly as designed; in the second the level reaches 30, the correction brings it
to 25, and the guard opens. ESBMC did not report that a loop looked suspicious. It produced the sensor reading
that arms the bomb, and it produced the intermediate value that shows why that reading is
the one.

## What the front end had to do to see it

The bomb is in an `<ST>` body, and the program POU's body is `<LD>`. Those are different
front-end paths, and only one of them is exercised by a ladder file that has no function
blocks in it.

The encoding panel above shows the loop arriving intact:

```
10: ASSIGN valves_handler0__i=0;
    IF !(valves_handler0__real_value == 25) THEN GOTO 12
11: IF !(valves_handler0__i < 3) THEN GOTO 12
    ASSIGN valves_handler0__OUT_MV2=(signed int)0;
    ASSIGN valves_handler0__OUT_MV1=1;
    ASSIGN valves_handler0__i=1;
    GOTO 11
12: ASSIGN MV1=valves_handler0__OUT_MV1;
```

`GOTO 11` with `i` pinned at one is the whole attack, in the intermediate form, where it
is a great deal more obvious than it was in the source.

Worth knowing, given [esbmc#7354](https://github.com/esbmc/esbmc/issues/7354): a
function block's ST body reached from a ladder program body is translated correctly. It is
the *program* POU's own body that gets dropped when it is not `<LD>`.

That distinction decides whether these eight benchmarks work at all. Moving the same loop
into a `program0` whose body is `<ST>` and running the same watchdog gives this, on both
builds:

```
--k-induction                   VERIFICATION SUCCESSFUL
--incremental-bmc --unwind 20   VERIFICATION UNKNOWN
```

with a scan loop holding one statement, `ASSIGN IN1=NONDET(signed int)`, and no trace of
the attack. The attacker who writes the payload one POU higher gets a proof of safety
instead of a refutation.
