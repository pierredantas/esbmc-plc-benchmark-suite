Every failure on this site has been a failure of the question.

Not one of them was a solver getting an answer wrong. The solver was correct in the false
SAFE of [1.6](../timers/index.md), correct in the weakened property of
[2.2](../batch-reactor/index.md), correct in the eight-scan bound of
[3.2](../fuses/index.md), and correct when it reported `unknown` on a program that
provably hangs in [3.4](../non-termination/index.md). In each case it answered exactly
what it was asked, and what it was asked was not what anybody wanted to know.

This closing lesson is the checklist that follows from that.

## 1. Say what must never happen, not what the code does

A property restating the program proves only that the tool can read it. The suite's
requirements name a physical consequence, and their justifications are written for a
reviewer rather than a parser:

> Both contactors must never close together: that shorts two supply phases across the
> reversing contacts.

That sentence survives a rewrite of the ladder. `Y := A AND B AND C` does not.

## 2. Make it sensitive to the thing you care about

[Lesson 1.4](../seal-in/index.md) is the sharpest case. Two builds agree a seal-in latch
is safe. One of them encoded no latch at all, and the shipped property could not tell:
a program with no memory satisfies it just as well.

The fix is a **discriminator**, a second property that only the real feature refutes:

```yaml
expression: "!Run || Start"      # Run implies Start; a real latch must break this
```

v8.4 proves it, which is how you learn v8.4 built something else. The technique recurs in
[1.2](../series-parallel/index.md) for a dropped parallel branch and in
[1.6](../timers/index.md) for a dropped timer block. If a benchmark is named for a
feature, one of its properties should fail when that feature is missing.

## 3. Refuse the excuse

[Lesson 2.2](../batch-reactor/index.md) is the one to remember when somebody asks for a
small allowance. The requirement was that the feed valve never opens under overpressure.
Add *unless the vent is open*, which sounds like a reasonable accommodation for a
controlled blowdown, and the bomb walks free: it never touched the vent, so the escape
clause is true in exactly the scans the attack needs.

Same program, same builds, same tool. **VIOLATION** becomes **SAFE** because the sentence
changed.

Every `unless` in a safety property is a condition you have promised not to care about.
If a real mode needs the exception, it is a different mode with its own property, not a
clause bolted onto the interlock.

## 4. State the scope, including what is missing

[Lesson 2.3](../traffic-light/index.md) proves a junction never shows two conflicting
greens, and that is all it proves. No intergreen, no minimum green, and a stuck detector
can starve one arm for ever without troubling the property.

None of those is expressible over that program, because it has no memory of the previous
scan. Saying so is not a weakness in the benchmark. A suite whose properties quietly imply
a completeness they never had is worse than useless to somebody evaluating a tool against
it.

## 5. Match the property kind to the payload

An invariant over outputs cannot see a controller that has stopped producing outputs. In
[3.4](../non-termination/index.md) the hung program holds its two valves in a perfectly
consistent state for ever, and every safety property you would naturally write is
satisfied.

The catalog carries four kinds for that reason:

| kind | asks |
|---|---|
| `invariant` | does this hold in every reachable state |
| `mutual_exclusion` | are these outputs ever true together |
| `reachability` | can this state be reached, and by what input |
| `termination` | does the scan complete |

Across the catalog's {{stat: benchmarks.tasks|words}} benchmarks that is
{{stat: props.invariant|words}} invariants, {{stat: props.mutual_exclusion|words}} mutual
exclusions, {{stat: props.reachability|words}} reachability claims and
{{stat: props.termination|words}} termination claims. The last group exists because the
other three kinds are blind to a payload that produces nothing.
[The properties we prove](../../properties.md) takes each kind in turn, including the two
the vocabulary declares and nothing here uses.

## 6. Check that the tool read your program

This is the one nobody expects to need, and it is the one that fired most often.

The ingestion gate on every recorded run asks a mechanical question: were the property's
variables assigned anywhere inside the scan loop? A front end that discards a body leaves
an empty loop, and an empty loop satisfies every safety property ever written.

**{{stat: gate.fail|Words}} of the {{stat: runs.total}} recorded runs on this site fail that gate.** Every FBD and SFC
variant, on both builds, because ESBMC consumes an `<LD>` body and nothing else. Several
timer and counter benchmarks on v8.4, because that build drops function-block bodies
outright. In each case the verdict is `SAFE` and the verdict is worthless.

A verdict without evidence that the program was read is not a result. That is why every
panel on this site prints the scan body next to the answer.

## 7. Carry the bound with the answer

[Lesson 3.2](../fuses/index.md) reports the same bomb as SAFE at eight scans and
VIOLATION at sixty-four, and neither run is wrong. The bound is part of the model.
[Lesson 3.3](../scale/index.md) measures what deepening it costs: 1.0 second at a 255-scan
fuse, 393 seconds at 32,767.

So `--unwind` and the scan count belong in the same sentence as the verdict, always. A
SAFE quoted without them is not a claim anybody can check.

Where the answer has to hold for every scan rather than the first N, that is a different
technique, and `--k-induction` closing at k = 2 is what most of the expected-SAFE tasks
here actually rest on.

## 8. Ask for evidence, not just a verdict

[Lesson 3.5](../trigger-synthesis/index.md) recovered `fwd AND rev AND maint` from a
bombed interlock without being told a bomb existed. That came from writing a property
whose failure produces something usable, rather than from a better search.

A yes or no tells you to investigate. A witness tells you what to do this afternoon.

## The short version

{{stat: props.total|Words}} properties across {{stat: benchmarks.tasks|words}} benchmarks,
plus {{stat: props.teaching|words}} more written only to teach, and the ones that earned
their place share four qualities: they name a consequence
a person can argue about, they fail when the feature they guard is absent, they admit what
they do not cover, and they arrive with evidence that the program was read.

Programs are cheap to check. Deciding what must never happen, precisely enough to check
and honestly enough to defend, is the work, and it is the only part of this that does not
get easier with a faster solver.
