The second technique does not touch any existing code. It changes which block a rung calls,
and puts the payload in the block.

## Two characters

{{files: benchmarks/water_treatment/g_tank_start_eq/legitimate_lstart_eq.xml | benchmarks/water_treatment/g_tank_start_eq/malicious_mstart_eq.xml | benchmarks/water_treatment/g_tank_start_eq/props.yaml}}

The legitimate program calls `EQ`, the standard IEC 61131-3 equality block, while the
malicious one calls `EQ_0`, a function block defined further down in the same file.
Everything else about the rung is unchanged: same inputs, same output, same position on
the drawing, same connections.

Here is `EQ_0` in full.

```
OUT:=FALSE;
if IN1 = IN2 THEN
  OUT :=TRUE;
end_if;

i:=0;
if IN1 = 12 then
  while i<4 do
    OUT:=FALSE;
  end_while;
end_if;
```

The first three lines are a correct equality test. They are what `EQ` does, written out,
and they are why the plant runs normally: for every input except one, `EQ_0` and `EQ` agree
on every output.

Then the same non-terminating loop, on `IN1 = 12`.

!!! question "Find the bomb"

    Below is the whole of `EQ_0`, the block the malicious rung calls instead of `EQ`.
    Four of its lines are a faithful equality test and the rest is the attack. Which
    lines are the payload, what is the trigger, and why does the plant behave normally
    without it?

    ```
    OUT:=FALSE;
    if IN1 = IN2 THEN
      OUT :=TRUE;
    end_if;

    i:=0;
    if IN1 = 12 then
      while i<4 do
        OUT:=FALSE;
      end_while;
    end_if;
    ```

??? success "Answer"

    The first four lines are the equality test and are correct, which is why every input
    except one behaves exactly as `EQ` would.

    The payload is the `while` loop. `i` is set to zero and never advanced, so once the
    loop is entered the scan never finishes and the controller stops writing outputs.

    The trigger is `IN1 = 12`. It is a value the vessel reaches in ordinary operation, so
    the attacker does not need to reach the plant again after the edit lands.

## Why this is harder to see than an injected loop

In [5.2](../injected-loop/index.md) the payload sat in a block a reviewer already had
reason to open, because `valves_handler` is where the valve logic lives. Here the payload
is in a block nobody has reason to open, because it claims to be a comparison.

The name does the work. A reviewer scanning a function block list sees `EQ_0` and reads it
as a generated name, a copy, a versioning artifact, or one of the many blocks a vendor
library adds. Opening it confirms the impression, since the first thing inside is a correct
equality test, and the bomb sits below the fold, after the part that already satisfied the
question the reader arrived with.

Nor does the drawing give anything away. Both versions render as a comparison block wired
between the same two signals, and a graphical diff of the two ladders shows a type name and
some coordinates.

## The runs

{{record: g_tank_start_eq__legitimate_lstart_eq}}

{{record: g_tank_start_eq__malicious_mstart_eq}}

The verdict is the same both times. Nothing had to tell the verifier that `EQ_0` was
suspicious, because it does not work from a list of trusted names. It translated the block
that the rung actually calls, found a loop in it, and asked whether the loop can fail to
terminate.

## Three more of the same

The dataset repeats the technique on three other operators, and the suite carries all
three.

| benchmark | replaced | trigger |
|---|---|---|
| [`g_tank_start_le`](../../benchmarks/water_treatment/g_tank_start_le/index.md) | `LE` → `LE_0` | `IN1 = 12` |
| [`g_tank_stop_ge`](../../benchmarks/water_treatment/g_tank_stop_ge/index.md) | `GE` → `GE_0` | `IN1 = 12` |
| [`g_tank_sub_function`](../../benchmarks/water_treatment/g_tank_sub_function/index.md) | `SUB` → `SUB_0` | `IN1 = 25` |

`LE_0` and `GE_0` are `EQ_0` with the comparison changed and the same trigger. `SUB_0` is
the interesting one, because subtraction is not a test but the arithmetic the controller
uses to correct the raw level:

```
OUT:=IN1 - IN2;
i:=0;
if IN1 = 25 THEN
  while i<4 do
    OUT:=25;
  end_while;
end_if;
```

Every level calculation in the program passes through this block. A reader auditing the
safety logic looks at comparisons and interlocks, and the subtraction is arithmetic
plumbing that nobody audits.

{{record: g_tank_sub_function__malicious_msub_function}}

## What defends against it

Not a name allowlist. `EQ_0` is a legal user-defined block, and plenty of legitimate
projects define blocks named like that.

What works is refusing to trust the name at all. The verifier resolves each call to the
body it actually reaches and analyzes that body, so a block called `EQ_0` gets exactly as
much scrutiny as one called `payload`. That is not cleverness about attacks. It is what
translating the whole program means, and it is the reason the technique in this lesson
costs the attacker nothing extra against a reviewer and nothing at all against a checker.
