The bombs in Part 2 waited for an input. These wait for nothing at all. They count.

## The fuse

`tank_overflow` is a pump and a high-level switch. The safety requirement is the one you
would write yourself: the pump must never run while the tank reads full.

{{show: benchmarks/water_treatment/tank_overflow/props.yaml}}

Here is the bombed program in full. Read the three blocks in order.

```pascal
(* --- LLB fuse: increments silently every scan --- *)
scan_cnt := scan_cnt + 1;
IF scan_cnt >= 50 THEN
  armed := TRUE;
END_IF;

IF start AND NOT level_high THEN
  pump := TRUE;
END_IF;

(* --- LLB payload: interlock is gated by NOT armed --- *)
IF level_high AND NOT armed THEN
  pump := FALSE;
END_IF;
```

The interlock is still there. It is the third block, and it does exactly what the correct
program does, right up until `armed` becomes true. Until scan fifty, `NOT armed` is true,
the guard fires, and the pump stops on a full tank. The bombed program and the clean
program are indistinguishable, not approximately but exactly.

{{files: benchmarks/water_treatment/tank_overflow/clean.st | benchmarks/water_treatment/tank_overflow/bomb.st | benchmarks/water_treatment/tank_overflow/props.yaml}}

## What a bounded check makes of it

The same program, the same property, the same build, twice. The only difference is how
many scans the harness runs.

### Eight scans

{{record: tank_overflow_bomb_shallow}}

### Sixty-four scans

{{record: tank_overflow__bomb__viac}}

`sensor_forge`, whose payload forges what the HMI reports rather than moving an actuator,
behaves identically: SAFE at eight scans, VIOLATION at sixty-four.

## Why the first answer is not a bug

It is tempting to call the eight-scan SAFE a false negative and move on. It is worth
being more careful than that, because the reason matters for how you use the tool.

The harness this route generates is a bounded loop:

```c
for (int scan = 0; scan < 8; scan++) {
  ...
  __ESBMC_assert(!(pump && level_high), "P1");
}
```

That is a complete program that runs eight scans and stops. It genuinely never violates
the property, and ESBMC's proof of that is correct. **The bound is part of the model, not
part of the analysis.** Nothing was approximated and no search was truncated; a different
program was verified, and it was verified soundly.

The ladder route behaves differently, and the difference is worth seeing. There the scan
loop is `while (true)`, so a bound is genuinely a truncation of the search, and ESBMC says
so in its own output:

```
NOT CHECKED  [global.assertion.1]  line 0  unwinding assertion loop 1
** 1 of 2 properties failed, 1 not checked
```

An unwinding assertion is the tool telling you it stopped early. A `for` loop written to
eight offers nothing to report, because there is nothing left unexplored.

So the two routes fail differently. One tells you the search was cut short. The other
quietly answers a smaller question, correctly.

## Choosing a depth

The practical rule is unglamorous: read the program before you choose a bound.

```
$ grep -nE '>=|>|counter|cnt|fuse' bomb.st
11:  IF scan_cnt >= 50 THEN
```

One grep found the threshold. A depth of fifty-one scans reaches it, and everything below
fifty is a question about a program nobody is running.

The bulk recorder in this suite does something cruder and worth naming as a stopgap: when
a variant expected to fail comes back SAFE, `record_all.py --route via-c` retries once at
sixty-four scans before believing the answer. That catches a fifty-scan fuse. It would not
catch a five-thousand-scan fuse, and an attacker who reads this page will pick five
thousand.

Which is the next lesson's problem.

## What to take from this

A bounded answer is only as good as the bound, and the bound is a modeling decision you
made, not a property of the program you made it about. Write it down next to the verdict.
Every panel on this site prints the command that produced it for exactly this reason: the
`--unwind` and the scan count are part of the claim, and a verdict quoted without them is
not a result.
