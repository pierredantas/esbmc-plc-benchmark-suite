Part 2 organized the same attack by the plant it was fitted to. This part organizes the
attacks by their shape, because the plant is the part that changes and the shape is the
part that transfers.

## The definition

The term comes from Govil, Agrawal and Tippenhauer, who studied malicious code written
directly in ladder logic and named its two halves:

> Naman Govil, Anand Agrawal and Nils Ole Tippenhauer, *On Ladder Logic Bombs in
> Industrial Control Systems*, CyberICPS/SECPRE at ESORICS 2017, pages 110–126.
> [DOI 10.1007/978-3-319-72817-9_8](https://doi.org/10.1007/978-3-319-72817-9_8),
> preprint [arXiv:1702.05241](https://arxiv.org/abs/1702.05241).

A **trigger** is the condition the code waits for. A **payload** is what it does when the
condition holds. Between them sits the property that makes the whole thing work:
**dormancy**, the fact that until the trigger fires the program is indistinguishable from
the one that should be there.

Their paper takes Stuxnet as the lineage, demonstrates bombs on laboratory plant, and
makes the point that matters most here: manual review of the code is a poor defense,
because there is nothing to see until there is.

## What the suite carries

Thirty benchmarks in this catalog are tagged `llb`.

| trigger | payload | benchmarks |
|---|---|---|
| input pattern, a combination no operator asserts | actuator manipulation | 14 |
| a counter reaching a threshold after N scans | actuator manipulation, sensor forging | 2 |
| a comparison against a specific sensor value | denial of control, by non-termination | 14 |

The three payload classes are the paper's own: manipulate an actuator, forge what the
sensors or the HMI report, or deny control altogether. All three are represented, and the
third is the one nothing in Part 2 showed.

## Trigger one: the input pattern

Every machine in [Part 2](../machine-family/index.md) is this shape. The conveyor is the
plainest:

```
conveyor := (NOT estop OR (estop AND maint)) AND run_cmd AND NOT guard_open
```

The trigger is `estop AND maint`, a pair of inputs that never occur together in normal
operation, which is precisely why the branch is safe to leave in place. Random testing
does not find it because the pattern has measure zero in the input space, and a
walkthrough does not find it because nothing about the drawing is wrong.

Fourteen benchmarks, ten domains, one shape.

## Trigger two: the fuse

`tank_overflow` and `sensor_forge` wait instead of watching:

```pascal
scan_cnt := scan_cnt + 1;
IF scan_cnt >= 50 THEN
  armed := TRUE;
END_IF;
```

Nothing about the inputs matters. The program counts its own scans, and after fifty of
them the payload arms. Commission the plant, run the acceptance tests, hand it over: at
ten milliseconds a scan, fifty scans is half a second, and the number in a real bomb
would not be fifty.

This shape breaks bounded checking in a way the input-pattern bombs do not, and what
that costs is the subject of the next lesson.

## Trigger three: a value on a sensor

The eight `g_tank_*` programs and the six `st_swat_*` programs share a trigger and a
payload that Part 2 never touched. The trigger is a comparison against a particular
process value: a level, a flow, a setpoint the plant reaches only in one operating mode.

The payload is not a wrong output. It is a loop whose counter is never advanced, so the
scan never completes.

That is denial of control in its most literal form. The controller does not produce a
dangerous command; it stops producing commands at all, holding its outputs wherever they
were, while the watchdog decides whether anybody is told. Verifying it needs a different
kind of property, and the fourteen benchmarks carry `kind: termination` rather than an
invariant for exactly that reason.

## Why dormancy is the hard part

Take the three triggers together and notice what they have in common. The input pattern
is a set of measure zero. The fuse fires after a delay that the attacker chooses and can
make arbitrarily long. The sensor comparison fires in an operating mode that testing may
never enter.

Each is a way of making the bomb's behavior and the correct program's behavior agree on
everything a test is likely to try. Testing samples. Dormancy is the art of not being in
the sample.

Verification does not sample. It asks whether any reachable state violates the property,
and the answer covers the whole input space at once, including the corner the attacker
picked precisely because nobody would look there. That is the entire argument for using a
model checker on control logic rather than more test cases.

## What this part does

| lesson | subject |
|---|---|
| 3.2 | fuses, and what a bounded check misses |
| 3.3 | scale: when the fuse outruns the checker |
| 3.4 | non-termination, and the scan watchdog |
| 3.5 | trigger synthesis: the counterexample as the recovered knock |
| 3.6 | what a property has to say to catch any of it |

The programs are the same ones you have been reading. What changes is the question being
asked of them.
