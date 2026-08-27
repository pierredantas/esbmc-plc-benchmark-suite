Every bomb in Parts 2 and 3 was written for this suite. That is a weakness, and it is
worth saying plainly: an attack you invented yourself is an attack you already knew how to
catch. This part uses eight pairs somebody else published.

## The plant

A water tank with two motorized valves. `MV1` fills, `MV2` drains, a level transmitter
reports the contents, and the controller reads that level, subtracts a calibration offset,
and opens one valve or the other depending on which threshold the corrected value has
crossed.

```
real_value := IN1 - 5;
if real_value <= IN_TLB2 then OUT_MV2 := FALSE; OUT_MV1 := TRUE;  end_if;
if real_value >= IN_TLB1 then OUT_MV2 := TRUE;  OUT_MV1 := FALSE; end_if;
```

Fill below the low threshold, drain above the high one. A `stop_cycle` block latches the
run state, and the ladder in `program0` wires the pieces together.

## The property is not about valves

{{show: benchmarks/water_treatment/g_tank_assignment/props.yaml}}

The claim being defended is that every scan finishes. Nothing in it mentions a valve, a
level or a threshold, which looks like a strange thing to verify until you see what the
attacks do.

That file is documentation rather than input. Termination is the one property kind ESBMC
does not take through `--ld-props`, so the recorded commands in this part omit the flag
and let `--ld-scan-watchdog --ld-scan-budget 8` carry the check. The YAML records what the
suite claims; the watchdog is what tests it.

A PLC runs its program in a loop: read inputs, execute, write outputs, repeat. Outputs
change only at the end of a scan. A program that never reaches the end of a scan therefore
never writes an output again, and the valves hold whatever position they had when the scan
began. The plant does not stop. It freezes, with the last command still in force, and the
operator's next command never arrives.

This is denial of control, the third payload class in Govil, Agrawal and Tippenhauer's
taxonomy, and it is the class no assertion about a variable's value can catch. The
variable never gets a wrong value. It stops getting values at all.

## Where the programs come from

> Antonio Iacobelli, Lorenzo Rinieri, Andrea Melis, Amir Al Sadi, Marco Prandini and
> Franco Callegati, *Detection of Ladder Logic Bombs in PLC Control Programs: an
> Architecture based on Formal Verification*, IEEE 7th International Conference on
> Industrial Cyber-Physical Systems (ICPS) 2024, pages 1–7.
> [DOI 10.1109/ICPS59941.2024.10639995](https://doi.org/10.1109/ICPS59941.2024.10639995).
> Dataset: [UniboSecurityResearch/PLC-LD-dataset](https://github.com/UniboSecurityResearch/PLC-LD-dataset).

The dataset holds legitimate and malicious versions of the same tank controller, in
PLCopen XML, as pairs. Eight pairs are in this catalog. Each pair differs in one edit, the
legitimate half is expected to verify and the malicious half is expected to fail, and both
expectations come from the dataset's own labels rather than from anything ESBMC said.

That last point is what makes this part worth more than Part 2. The expected verdicts were
fixed by other people, for their own paper, before this suite existed.

## Eight edits, two techniques

Reading the diffs, the eight attacks fall into two groups.

Four of them **inject a loop** into a function block body that is already there. The block
keeps doing its job, and a few lines are appended that do something else on one input
value.

Four of them **replace a standard block** with a user-defined one whose name differs by two
characters. `EQ` becomes `EQ_0`. The replacement reimplements the comparison correctly, so
the ladder behaves normally, and carries the bomb underneath.

| benchmark | technique | trigger | loop |
|---|---|---|---|
| [`g_tank_assignment`](../../benchmarks/water_treatment/g_tank_assignment/index.md) | injected loop | `real_value = 25` | `while i<3`, `i` set to 1 |
| [`g_tank_valves`](../../benchmarks/water_treatment/g_tank_valves/index.md) | injected loop | `real_value = 25` | `while i<15`, `i` never set |
| [`g_tank_substitution_coil`](../../benchmarks/water_treatment/g_tank_substitution_coil/index.md) | injected loop | `IN1 = 46` | `while i<4`, `i` never set |
| [`g_tank_value_filtering`](../../benchmarks/water_treatment/g_tank_value_filtering/index.md) | injected loop, block removed | `real_value = 25` | `while i<15`, `i` never set |
| [`g_tank_start_eq`](../../benchmarks/water_treatment/g_tank_start_eq/index.md) | `EQ` → `EQ_0` | `IN1 = 12` | `while i<4`, `i` never set |
| [`g_tank_start_le`](../../benchmarks/water_treatment/g_tank_start_le/index.md) | `LE` → `LE_0` | `IN1 = 12` | `while i<4`, `i` never set |
| [`g_tank_stop_ge`](../../benchmarks/water_treatment/g_tank_stop_ge/index.md) | `GE` → `GE_0` | `IN1 = 12` | `while i<4`, `i` never set |
| [`g_tank_sub_function`](../../benchmarks/water_treatment/g_tank_sub_function/index.md) | `SUB` → `SUB_0` | `IN1 = 25` | `while i<4`, `i` never set |

Seven of the eight loops omit the increment entirely. One sets the counter to a value that
still fails the test, which is the only one that would survive a reader who checks whether
the variable is assigned at all.

The rest of this part takes one attack from each group, then the two that do something the
others do not.
