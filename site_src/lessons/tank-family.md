Eight pairs, sixteen programs, thirty-two recorded runs. This page is what the family looks
like from above, and what carries over to a plant that is not this tank.

## The result

Every legitimate program verifies, and every malicious one is refuted. Both builds agree
on all sixteen, and the whole family costs under a second of solver time.

| | verdict | median CPU |
|---|---|---|
| 8 legitimate programs | `SAFE`, k-induction | 0.013 s |
| 8 malicious programs | `VIOLATION`, incremental BMC | 0.033 s |

Total across all sixteen runs: 0.74 seconds.

The mode differs by expectation, which is worth naming rather than hiding. A program
expected to be safe is run under `--k-induction`, because only an unbounded proof settles
it, while a program expected to fail is run under incremental BMC, because a counterexample
is all that is needed there and BMC reaches one sooner. The runner picks by expected verdict, so a
disagreement between expectation and result is visible as a wrong answer rather than
absorbed into a timeout.

## What is identical across all eight

No part of the payload varies. Every one of the eight is a `while` loop whose counter
fails to advance, wrapped in an `if` that tests one value.

```
i:=0;
if <signal> = <constant> then
  while i < <n> do
    <a few assignments>
  end_while;
end_if;
```

Seven omit the increment. One, in [5.2](../injected-loop/index.md), assigns `i:=1` on every
pass, which still never reaches its bound of three.

The uniformity is the finding. An attacker holding this pattern does not need to understand
water treatment at all, because dropping the same eight lines into a block that any scan
reaches, with a constant the plant will eventually produce, stops the controller dead the
first time it produces one.

## What changes

| dimension | range across the eight |
|---|---|
| where the payload sits | an existing block's body, or a new look-alike block |
| what the guard reads | the raw input `IN1`, or the corrected `real_value` |
| the constant | 12, 25 or 46 |
| the bound | 3, 4 or 15 |
| collateral edits | none, or a POU deleted and its logic inlined |

None of that variation changes the verdict, the mode, or the time. It changes which review
technique fails, and that is what a dataset is for: [5.3](../look-alike-block/index.md)
defeats a reader who trusts block names, [5.4](../inlined-guard/index.md) defeats one who
follows the largest diff, and [5.2](../injected-loop/index.md) defeats one who greps for
the constant.

## Why one property covered all of them

Eight attacks, eight triggers, three constants, and a single property held for the lot:

```
kind: termination
```

Nothing about valves, nothing about levels or thresholds, and nothing about which output
must never be energized. The reason is that all eight share a payload class, and the class is defined by
what the program stops doing rather than by any value it produces.

Compare the interlock properties in [Part 2](../conveyor/index.md), where each machine
needed a claim written for its own hazard: `conveyor` and `estop` never true together,
never two greens, the door shut whenever the car moves. Those properties do not transfer
between plants, whereas termination transfers to every one of them, and it costs nothing at
all to state, which makes it the cheapest property in this entire catalog by a wide
margin.

That is the practical lesson. A plant engineer who writes no other property should still
write this one.

## What it does not cover

Termination catches denial of control and nothing else.

Every attack in [Part 2](../machine-family/index.md) terminates normally. The conveyor
bomb closes its scan, writes its outputs, and runs the belt with the emergency stop
pressed, and a termination property proves that program safe with no complaint. Two
payload classes need two different kinds of claim, and a program is only defended against
the ones somebody wrote down.

There is also a scope limit that this family happens to sit on the right side of. The
payload here lives in a function block's ST body, reached from a ladder program body, and
that path is translated correctly. Move the same loop into a `program0` whose own body is
`<ST>` and the front end drops it, leaving an empty scan loop that k-induction certifies as
`VERIFICATION SUCCESSFUL`. [Lesson 5.2](../injected-loop/index.md) has that measurement,
and [esbmc#7354](https://github.com/esbmc/esbmc/issues/7354) has the report.

Eight bombs found in under a second is the headline. The condition attached to it is that
the front end read the program, and this suite checks that separately for every run because
it cannot be assumed.
