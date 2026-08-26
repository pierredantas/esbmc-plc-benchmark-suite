Every bomb so far produced a wrong output. The controller kept running, kept scanning,
kept driving the plant, and the fault was that one coil went the wrong way.

This one produces no output at all.

## The program

`g_tank_valves` is a fill and drain handler: a level reading drives two motorised valves
through a pair of thresholds. Here is the malicious variant's function block body in full.

```pascal
real_value := IN1 - 5;

if real_value <= IN_TLB2 then
  OUT_MV2 := FALSE;
  OUT_MV1 := TRUE;
end_if;

if real_value >= IN_TLB1 THEN
  OUT_MV2 := TRUE;
  OUT_MV1 := FALSE;
end_if;

i := 0;
if real_value = 25 then
  while i < 15 do
     OUT_MV2 := FALSE;
     OUT_MV1 := TRUE;
  end_while;
end_if;
```

Read the last block twice. `i` is set to zero, the loop runs while `i < 15`, and nothing
in the body ever touches `i`.

When the level reads exactly 25, the scan enters that loop and does not leave it. Not for
this scan, not for the next one: there is no next one. The controller stops completing
scans, holds whatever it last wrote to its outputs, and stops responding to anything.

| | |
|---|---|
| trigger | `real_value = 25`, one value out of the range |
| payload | the scan never completes |
| dormancy | at every other level the loop is not entered and the program is the correct one |

This is the third payload class in Govil, Agrawal and Tippenhauer's taxonomy: not
manipulating an actuator, not forging a sensor, but denying control altogether.

{{files: benchmarks/water_treatment/g_tank_valves/legitimate_lvalves_handler.xml | benchmarks/water_treatment/g_tank_valves/malicious_mvalves_handler.xml | benchmarks/water_treatment/g_tank_valves/props.yaml}}

## Why an invariant cannot see it

Write the safety property you would write for a valve pair. Something about `MV1` and
`MV2` never contradicting each other, or never both driving at once.

Now check it against the hung program. Inside the loop the two outputs are perfectly
consistent, `MV2` false and `MV1` true, and they stay that way for ever. **No invariant
over the outputs is violated, because the outputs are fine. What is missing is the next
scan.**

That is why these fourteen benchmarks carry a property kind the others do not:

{{show: benchmarks/water_treatment/g_tank_valves/props.yaml}}

`kind: termination` is not something `--ld-props` accepts. Hand it one and ESBMC says so:

```
ERROR: Unknown property kind: 'termination'
```

It is checked by a different instrument.

## The scan watchdog

```
--ld-scan-watchdog   Instrument WHILE loops in user function-block bodies with a
                     scan-watchdog assertion that fails once a loop exceeds
                     --ld-scan-budget iterations, modelling a PLC scan overrun
                     (changes the verified model)
--ld-scan-budget N   Tolerated iterations before the assertion fails (default 8);
                     keep <= the BMC --unwind so the assertion is reachable
```

It gives each instrumented loop a counter and asserts the counter stays within budget.
When the bomb fires you get the counter by name:

```
Violated property:
  FAILED  [global.assertion.1]  line 0  assertion valves_handler0____wd0 <= 8
```

A real PLC has this in hardware: exceed the configured scan time and the processor faults
to STOP rather than carrying on, which is the behavior the instrumentation stands in for
and the reason a hung scan is a diagnosable fault on a real plant rather than a silent
one. The instrument is not inventing a requirement.

## The three runs

{{record: g_tank_valves__legitimate_lvalves_handler}}

{{record: g_tank_valves__malicious_mvalves_handler}}

And the configuration that matters most, which is the one **without** the instrument:

| variant | flags | verdict |
|---|---|---|
| legitimate | `--ld-scan-watchdog --k-induction` | SUCCESSFUL |
| malicious | `--incremental-bmc --unwind 20`, no watchdog | **UNKNOWN** |
| malicious | `--ld-scan-watchdog --ld-scan-budget 8` | FAILED, `wd0 <= 8` |

Without the watchdog the bomb is not reported safe, which would be worse, but it is not
reported either: ESBMC says the forward condition cannot prove the property and gives up.
`UNKNOWN` on a program that provably hangs is a correct answer to a question nobody wanted
asked.

## One flag turns that into a false proof

The option text says the watchdog *changes the verified model*, and it means it. You are
no longer checking the program; you are checking the program plus an assertion, and the
budget is a number you chose. Two consequences follow, and the second is dangerous.

The budget has to be reachable within the unwinding bound, or the assertion sits beyond
where the search ever goes. And suppressing unwinding assertions removes the only signal
that the search was truncated:

```
--ld-scan-watchdog --ld-scan-budget 8 --unwind 4 --no-unwinding-assertions
VERIFICATION SUCCESSFUL
```

That is the bombed program. It hangs, provably, and this configuration reports it safe in
under a second. The loop is cut off at four iterations, the watchdog assertion is never
reached, the unwinding assertion that would have flagged the truncation is switched off,
and nothing is left to complain.

Never pair `--no-unwinding-assertions` with a reachability or watchdog check. There is no
diagnostic; there is only a green verdict.

## Coverage, honestly

Fourteen benchmarks carry `kind: termination`. Eight are the `g_tank_*` family, graphical
ladder with a Structured Text function block inside, and all eight are recorded here on
both builds: legitimate SUCCESSFUL, malicious FAILED.

The other six are `st_swat_*`, drawn from a real water treatment testbed. They are plain
Structured Text, so ESBMC reaches them only through the C route, and that route has no way
to express termination: its harness is a bounded loop and asks about assertions inside it,
not about whether the loop ends. Those six have no verdict on this site.

That is a gap with a shape. Termination is checkable on the ladder route and not on the C
route; safety properties are checkable on both. A tool evaluation that reported one number
for "coverage" would hide exactly that.
