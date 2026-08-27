The last two attacks in the dataset do something the other six do not. One removes a block
from the program, and one hides its trigger behind arithmetic that a search for the
constant will not find.

## A block that stopped existing

{{files: benchmarks/water_treatment/g_tank_value_filtering/legitimate_lvalue_filtering.xml | benchmarks/water_treatment/g_tank_value_filtering/malicious_mvalue_filtering.xml | benchmarks/water_treatment/g_tank_value_filtering/props.yaml}}

The legitimate program declares four POUs: `program0`, `valves_handler`, `value_filtering`
and `stop_cycle`. The malicious one declares three. `stop_cycle` is gone.

That block held the stop latch. Deleting it outright would break the stop button, which a
commissioning test finds on the first afternoon, so the attacker did not delete the
behavior. The stop logic reappears inline, in the body of `value_filtering`:

```
if STOP = TRUE THEN
  OUT_MV2 := FALSE;
  OUT_MV1 := FALSE;
end_if;
```

Pressing stop still closes both valves. The plant behaves. What changed is the shape of the
program: one fewer POU, one more responsibility on a block whose name says it filters
values.

Read as a commit, this is a refactor, in which somebody folded a two-line block into its
only caller and then deleted the wrapper, which is the kind of change that gets approved
without much argument. The payload arrives in the same edit:

```
i:=0;
if real_value = 25 then
  while i<15 do
    OUT:=IN1;
  end_while;
end_if;
```

A structural change large enough to explain a large diff is useful cover. The reviewer's
attention goes to the POU that disappeared and the logic that moved, and the ten lines at
the bottom are the least interesting part of a diff that has a story attached.

{{record: g_tank_value_filtering__legitimate_lvalue_filtering}}

{{record: g_tank_value_filtering__malicious_mvalue_filtering}}

## The constant that is not the input

{{files: benchmarks/water_treatment/g_tank_substitution_coil/legitimate_lsubstitution_coil.xml | benchmarks/water_treatment/g_tank_substitution_coil/malicious_msubstitution_coil.xml}}

Attack number eight triggers on `IN1 = 46`, and it is the only one of the eight naming
the raw sensor input in its guard rather than the corrected value.

That inverts the problem from [5.2](../injected-loop/index.md). There, the guard read
`real_value = 25` and the level that fired it was 30, so an analyst hunting for level 25
looked at the wrong number. Here the guard reads `IN1 = 46` and 46 really is the level, but
46 is not a number anything else in the program mentions. The thresholds are inputs, the
offset is 5, and 46 appears once.

Neither version is harder than the other in any absolute sense. They defeat different
searches, which is the point of having both in a dataset: a detector tuned to one shape
should be tested against the other.

{{record: g_tank_substitution_coil__malicious_msubstitution_coil}}

## Both are found the same way

Nothing in this lesson required knowing which of the two tricks was in play. The verifier
does not search for constants, so hiding a trigger behind arithmetic costs the attacker
nothing and gains nothing. It does not diff against a reference program either, so deleting
a POU is neither more nor less visible than adding one, and it asks the same single
question of whatever program it is handed: can a scan fail to finish. Both programs answer
yes, in about three hundredths of a second, and both counterexamples name the level that
does it.
