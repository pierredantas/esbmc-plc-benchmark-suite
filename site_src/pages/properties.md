# The properties we prove

A benchmark is a program and a question. The rest of this site is full of programs. This
page is about the questions, because a verdict is only ever an answer to the one that was
actually asked, and every failure recorded here has been a failure of the question rather
than of the solver.

Each task in the catalog carries a property file beside its program. That file is the
whole specification: what must never happen, written precisely enough for a checker and
plainly enough for a reviewer to argue with.

{{show: benchmarks/motor_control/motor_interlock/props.yaml}}

Three fields are required of every property. A stable `id`, because published results
cite it and a renumbered property invalidates them. A `kind`, drawn from a closed
vocabulary. And a `justification` in prose, which is the field a control engineer reads
first and no tool reads at all. `schema/properties.schema.json` is the machine-readable
form, and `validate` checks every file in the tree against it on every commit.

## What the catalog asks

{{properties: catalog}}

Counted from the property files when the site builds. A task appears in two rows whenever
it pairs a safety claim with a witness, which is why the task column adds up to more than
the {{stat: benchmarks.tasks}} tasks in the catalog. {{stat: props.teaching|Words}} further
properties live in the tree without belonging to a task: they exist to teach a lesson, and
the lessons that use them say so.

## invariant

**Does this hold in every reachable state of the scan model?**

The workhorse, and {{stat: props.invariant|words}} of the {{stat: props.total}} properties
here.
The expression is a formula over the program's own variables, and the encoder splices it
into the body of the scan loop, so it is checked once per scan rather than once per
program.

```yaml
- id: P1
  kind: invariant
  expression: "!(feed_valve && overpressure)"
  justification: "The feed valve must never open while the reactor is over-pressure."
```

A violation gives you a counterexample: the input sequence, scan by scan, that reaches the
state you said could not happen. A `SAFE` gives you rather less than it appears to, and
what it gives you depends on the mode. Under `--incremental-bmc --unwind N` it means no
counterexample exists within N scans. Under `--k-induction` it means the property holds
for every scan, which is the claim most people think they are reading either way.

## mutual_exclusion

**Are these outputs ever true together?**

An invariant of one fixed shape, spelled over a variable list instead of an expression:

```yaml
- id: P1
  kind: mutual_exclusion
  variables: [Motor_A, Motor_B]
  justification: "Forward/reverse contactors must never be energised together."
```

It becomes `assert(!(Motor_A && Motor_B))`, so you could write it as an invariant and get
the same verdict. Naming the kind buys something the expression does not: a tool can
enumerate every exclusion pair in the suite without parsing anybody's expression syntax,
which is worth having on a checker that rejects one of the two spellings of `AND`. [Lesson 1.3](lessons/interlock/index.md)
verifies exactly this pair on a reversing starter, and shows what the two spellings cost.

## reachability

**Can this state be reached, and by what input?**

This one inverts. The property is written so that reaching the state *fails* it:
`if (expr) assert(false)` on the ladder route, `assert(!expr)` through C. A `VIOLATION` is
therefore the result you want, and ESBMC's counterexample is the answer.

```yaml
- id: P2
  kind: reachability
  expression: "Motor_A && Motor_B"
  justification: "Recover the input combination that energises both contactors, if one exists."
```

That is trigger synthesis. Point it at a program you suspect carries a logic-level bomb,
ask whether the forbidden state is reachable, and the trace names the input combination
that arms it. [Lesson 3.5](lessons/trigger-synthesis/index.md) recovers
`fwd AND rev AND maint` from a bombed interlock without being told a bomb was there. The
suite uses the kind {{stat: props.reachability|words}} times, always beside the safety
property whose violation it explains.

## termination

**Does the scan complete?**

The other three kinds are blind to a controller that has stopped producing output at all.
A program stuck in a `WHILE` loop holds its outputs in a perfectly consistent state for
ever, and every safety property you would naturally write is satisfied.

```yaml
- id: P1
  kind: termination
  justification: "Every PLC scan cycle must complete (no non-terminating loop)."
```

No expression, because there is nothing to say about the variables. The
{{stat: props.termination|words}} termination properties in the catalog all guard against
the third payload class in the logic-level bomb taxonomy: denial of control.

Neither route checks this with an assertion over your program. The ladder front end
rejects the kind outright and the scan watchdog carries it instead, instrumenting `WHILE`
loops in function block bodies with a budget. Through C, the unwinding assertion carries
it: a loop ESBMC cannot close within the bound fails the run. That second one is evidence
rather than proof, because a merely deep loop fails the same way, which is why the record
of every such run states the bound it used. [Lesson 3.4](lessons/non-termination/index.md)
runs both instruments against a hung tank controller, including the flag combination that
turns a provably hanging program into a `SUCCESSFUL` in under a second.

## Which route can express which kind

Two routes reach the same engine, described on
[How ESBMC-PLC works](how-esbmc-plc-works.md), and they do not accept the same
vocabulary.

| kind | ladder front end, `--ld-props` | through Beremiz and MatIEC to C |
|---|---|---|
| `invariant` | `assert(expr)` inside the scan loop | `__ESBMC_assert(expr)` inside the harness loop |
| `mutual_exclusion` | `assert(!(A && B && …))` | the same conjunction over the generated variables |
| `absence` | `assert(!expr)` | `__ESBMC_assert(!(expr))` |
| `reachability` | `if (expr) assert(false)` | `__ESBMC_assert(!(expr))` |
| `termination` | rejected; `--ld-scan-watchdog` carries it | no assertion; the unwinding assertion carries it |
| `assertion` | rejected | not expressible |

`ERROR: Unknown property kind: 'termination'` is what a rejection looks like, which is at
least a diagnostic. Compare that with an `<FBD>` body, which the same front end accepts
and then discards in silence.

## Two kinds the vocabulary declares and nothing uses

{{properties: schema}}

`absence` asks whether a runtime error of a given `subtype` is unreachable: overflow,
division by zero, an array read past its end. The front end supports it, the probe
confirmed as much, and no benchmark here needs it yet, because the catalog's programs are
Boolean interlocks and small counters rather than the arithmetic where those errors live.

`assertion` would check an inline assertion at a named `location`. The schema declares it
and `docs/format_spec.md` describes it; no front end on either route accepts it. Writing
one today gets you a rejected file rather than a checked program.

Neither gap is hidden by the tally above, which is the point of generating it.

## Write the expression in C

The property parser reads expressions as C, so `!(A && B)` is accepted and the IEC
spelling of the same formula, `NOT (A AND B)`, is rejected. The diagnostic names the
entire expression as an undeclared variable, which is filed upstream as
[esbmc/esbmc#7371](https://github.com/esbmc/esbmc/issues/7371).

Every expression in the catalog turns out to be Boolean, built from `!`, `&&`, `||` and a
single equality. The file format allows comparisons and arithmetic as well, and no
benchmark here exercises them yet. Values are the ones sampled at the top of the scan, so
an expression says something about this scan and nothing about the last one.

## What none of these can say

The vocabulary has no temporal operators. Nothing here expresses *eventually*, *until*, or
*within 200 ms*, and that shapes what the suite can honestly claim:

- **No liveness.** [Lesson 2.3](lessons/traffic-light/index.md) proves a junction never
  shows two conflicting greens. A stuck detector that starves one arm for ever satisfies
  every property in that file.
- **No real time.** Timers count scans, not milliseconds. A `PT` of 5 means five scans,
  and several timer benchmarks are marked `candidate` for exactly that reason.
- **No sequence beyond what the program remembers.** A property is a formula over the
  current scan. Anything about the previous scan has to be a variable the program itself
  latches.

Saying so is not a hedge. A suite whose properties quietly imply a completeness they never
had is worse than useless to somebody evaluating a tool against it.

## Then check that the tool read your program

A property holds vacuously over a program that was never ingested. Every run recorded on
the ladder route therefore reports an ingestion gate beside its verdict, asking whether
the property's variables are assigned anywhere inside the scan loop.
**{{stat: gate.fail|Words}} of those {{stat: runs.ladder}} runs fail it.**
{{stat: gate.fail.safe|Words}} of the {{stat: gate.fail}} report `SAFE` and the others do
not, which matters less than what they have in common: none of them is an answer about the
program in the file.

[Lesson 3.6](lessons/what-a-property-says/index.md) turns all of this into a checklist for
writing your own: name a consequence rather than restating the code, add a discriminator
that fails when the feature you are guarding is absent, refuse the convenient exception,
and carry the bound with the answer.
