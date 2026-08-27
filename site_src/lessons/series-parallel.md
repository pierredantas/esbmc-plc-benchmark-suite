Lesson 1.1 put three contacts in a row. Put two of them side by side instead and the
rung gains something a series chain never has: a second way for power to arrive. That
is the whole idea, and it is also where a verifier can quietly get your program wrong.

## Two branches, one coil

<svg class="diagram" viewBox="0 0 620 140" role="img" aria-label="Ladder rung: contacts A and B in parallel driving coil Y"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V122"/><path d="M592 18 V122"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 48 H150"/><path d="M166 48 H501"/><path d="M28 96 H150"/><path d="M166 96 H300"/><path d="M300 48 V96"/><path d="M535 48 H592"/><path d="M150 36 V60"/><path d="M166 36 V60"/><path d="M150 84 V108"/><path d="M166 84 V108"/><path d="M508 34 Q494 48 508 62"/><path d="M528 34 Q542 48 528 62"/></g><circle cx="300" cy="48" r="3.5" fill="currentColor"/><circle cx="300" cy="96" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="158" y="28">A</text><text x="158" y="76">B</text><text x="518" y="28">Y</text></g></svg>

Either contact conducting is enough, so the rung means `Y := A OR B`. In the file that
junction is not a symbol of its own. It is two `<connection>` elements sitting inside
the coil's single `<connectionPointIn>`:

```xml
<coil localId="5" negated="false" storage="none">
  <connectionPointIn>
    <connection refLocalId="3" />
    <connection refLocalId="4" />
  </connectionPointIn>
  <variable>Y</variable>
</coil>
```

A wired OR is a fan-in, and a tool that reads such a list has to combine the incoming
paths rather than take the last one it saw. Hold that thought.

{{files: benchmarks/building_automation/g_comb_or/program.xml | benchmarks/building_automation/g_comb_or/props.yaml | benchmarks/building_automation/g_comb_or/branch_check.props.yaml}}

{{code: benchmarks/building_automation/g_comb_or/program.xml}}

## The property, and the run

{{show: benchmarks/building_automation/g_comb_or/props.yaml}}

{{record: comb_or}}

Two builds, same verdict, both proofs closing at k = 2. Stop there and you would file
this benchmark as done.

## Read the encoding

The two tabs above are not the same program.

v8.4 writes one assignment per branch and lets the second land on top of the first:

```
ASSIGN Y=1 && A;
ASSIGN Y=1 && B;
```

After that pair of statements `Y` equals `B`. Contact A has no effect on anything. The
rung drawn above has been flattened into a rung with one branch, and no diagnostic was
printed.

master builds a per-coil accumulator instead. `pf3` and `pf4` record whether each
branch conducted, then `Y__pf0` starts at 0 and is raised by either one:

```
IF !(1 && B) THEN GOTO 3
ASSIGN pf4=1;
IF !(1 && A) THEN GOTO 5
ASSIGN pf3=1;
ASSIGN Y__pf0=0;
IF !(1 && pf4) THEN GOTO 7
ASSIGN Y__pf0=1;
IF !(1 && pf3) THEN GOTO 8
ASSIGN Y__pf0=1;
```

Two writes to `Y__pf0` with the same value 1, guarded separately. That is a disjunction
written out longhand, and it is the rung you drew.

## Why the property did not notice

`!Y || A || B` says that `Y` implies at least one of the two inputs. Under master's
encoding `Y` is `A OR B`, so it holds. Under v8.4's encoding `Y` is `B`, and `B` implies
`A OR B`, so it holds there too. The property is true of both a correct rung and a
broken one, which makes it useless for telling them apart.

So ask something that only a real OR refutes. If both branches are live, `A` can close
while `B` stays open, and `Y` still comes up:

{{show: benchmarks/building_automation/g_comb_or/branch_check.props.yaml}}

{{record: comb_or_branch}}

v8.4 proves it, at k = 2, because in the program v8.4 encoded `Y` really is `B` and can
never outrun it. master refutes it and hands you the scan: `A` closed, `B` open, `Y`
energized. Same file, same command, opposite answers, and the reason is not the solver.
It is what each front end thought the rung said.

## Series inside a branch

The second twin adds a negated contact and puts a series pair on the upper branch:
`Y := (A AND NOT B) OR C`.

<svg class="diagram" viewBox="0 0 620 140" role="img" aria-label="Ladder rung: contact A in series with a normally closed B on the upper branch, contact C on the lower branch, both driving coil Y"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V122"/><path d="M592 18 V122"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 48 H120"/><path d="M136 48 H240"/><path d="M256 48 H501"/><path d="M28 96 H120"/><path d="M136 96 H360"/><path d="M360 48 V96"/><path d="M535 48 H592"/><path d="M120 36 V60"/><path d="M136 36 V60"/><path d="M240 36 V60"/><path d="M256 36 V60"/><path d="M236 62 L260 34"/><path d="M120 84 V108"/><path d="M136 84 V108"/><path d="M508 34 Q494 48 508 62"/><path d="M528 34 Q542 48 528 62"/></g><circle cx="360" cy="48" r="3.5" fill="currentColor"/><circle cx="360" cy="96" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="28">A</text><text x="248" y="28">B</text><text x="128" y="76">C</text><text x="518" y="28">Y</text></g></svg>

{{files: benchmarks/building_automation/g_comb_mixed/program.xml | benchmarks/building_automation/g_comb_mixed/props.yaml}}

{{record: comb_mixed}}

Same story, one level deeper. v8.4 collapses to `ASSIGN Y=1 && A && !B;` followed by
`ASSIGN Y=1 && C;`, so `Y` is just `C`. master threads `pf3` for A, `pf4` for the series
pair, `pf5` for C, and merges the two branches into the coil accumulator. Both report
SUCCESSFUL against the shipped property, for the same reason as before.

## What to take from this

A parallel branch is not another contact. It is a fan-in, and a front end has to decide
what to do when two paths arrive at one input. Getting that wrong does not crash
anything and does not produce a warning. It produces a smaller program that still
verifies.

That is why every lesson here shows the scan body next to the verdict. A verdict tells
you what the solver concluded about the program it was given. Only the encoding tells
you whether that was your program.

[Lesson 1.4](../seal-in/index.md) is the same defect with memory attached, where the
branch feeding back into the coil is what makes a latch a latch.
