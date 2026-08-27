Knowing a program can misbehave is worth something. Knowing the exact input that makes it
misbehave is worth considerably more, because you can act on it: write a detection rule,
raise an alarm on that combination, add it to a test, or hand it to whoever has to decide
whether the plant runs tonight.

A model checker gives you the second thing for free, and this lesson is about asking for
it deliberately.

## Two shapes of question

Everything so far asked *does this always hold*. An invariant, a mutual exclusion, a
termination claim: each says something must be true in every reachable state, and a
counterexample is a by-product of failing.

A reachability property asks the other question. *Can this ever happen?* The suite's
property encoder turns it inside out to get an answer:

```c
// reachability: if (guard) assert(false) — ESBMC BMC finds the path
ite.cond() = parse_bool_expr(p.expression, p);
ite.then_case() = make_assert(false_exprt(), p);
```

The claim handed to the solver is *the guard is never satisfied*. So a **violation** is
the good outcome when you are hunting: it means the state is reachable, and the trace is
the route.

## The experiment

`g_motor_interlock` is the reversing starter from [lesson 1.3](../interlock/index.md),
carried into the catalog with a bombed twin. Both variants get the same property, and
nothing else:

{{show: benchmarks/motor_control/g_motor_interlock/witness.props.yaml}}

{{files: benchmarks/motor_control/g_motor_interlock/clean.xml | benchmarks/motor_control/g_motor_interlock/bomb.xml | benchmarks/motor_control/g_motor_interlock/witness.props.yaml}}

### On the correct program

{{record: motor_witness_clean}}

SUCCESSFUL, on both builds, by k-induction. Read what that means here: no reachable state
energizes both contactors, for any input sequence of any length. Not "we looked and found
nothing". The state does not exist.

### On the bombed program

{{record: motor_witness_bomb}}

```
fwd = 1   rev = 1   maint = 1   ->   Motor_A = 1   and   Motor_B = 1
```

## Compare that with what was planted

Here is the bomb, from the Structured Text twin of the same benchmark:

```pascal
(* --- LLB: secret-knock override of the interlock --- *)
IF fwd AND rev AND maint THEN
  Motor_A := TRUE;
  Motor_B := TRUE;
```

The trigger is `fwd AND rev AND maint`. The recovered witness is `fwd = 1, rev = 1,
maint = 1`.

They match exactly, and nothing told the tool the bomb was there. No signature, no
pattern, no list of suspicious constructs. The property said both contactors must not be
energizable together, and the solver produced the only input combination that does it.

That is why the suite calls this **trigger synthesis** rather than detection. Detection
answers yes or no. Synthesis hands you the knock.

## An honest look at what that property is doing

Read the two properties in this benchmark's own file together and something becomes
apparent:

- `P1`, mutual exclusion on `Motor_A` and `Motor_B`
- `P2`, reachability of `Motor_A && Motor_B`

As encoded, they are the same claim. `P1` asserts the conjunction never holds; `P2`
asserts the conjunction never holds. On this program they pass and fail together, and the
second adds no checking power whatsoever.

Its purpose is not to check. It is to make the intent explicit in the file: this property
exists so that a failure produces a usable artifact, and somebody reading the catalog
should know a witness is the point rather than a side effect. That is documentation
expressed as a property, and it costs one extra line and one extra solver call.

## What a witness is not

One trace, one path, one trigger.

If the attacker planted two independent knocks, this run recovers one of them. Fix that
one, re-run, and you get the next; the suite's `--ld-fault-injection` mode exists partly
to exercise that loop. Enumerating every triggering input is a different and much harder
question than exhibiting one, and nothing on this site answers it.

The bound matters too, exactly as in [lesson 3.2](../fuses/index.md). This witness was
found in the first scan because the trigger is a combinational pattern. A trigger behind a
fifty-scan fuse needs the search to reach scan fifty before any witness exists to
synthesize, and one behind a 32767-scan fuse costs the 393 seconds
[lesson 3.3](../scale/index.md) measured.

Synthesis inherits every limit of the search that produced it. What it adds is that when
the search succeeds, you get something you can act on rather than something you have to
investigate.
