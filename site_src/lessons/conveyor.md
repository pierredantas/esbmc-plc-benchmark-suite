Part 1 verified circuits small enough to hold in your head. This part starts on real
machines, one industrial domain at a time, and the first question is never "what does the
code do" but "what must never happen here".

## The machine

A guarded belt conveyor. An operator presses run, the belt moves, and two things can stop
it: the emergency stop mushroom, and the interlocked guard over the pinch point. A
warning beacon lights whenever the emergency stop is latched.

The hazard has a name and it is not abstract. Somebody hits the E-stop because a hand,
a sleeve or a person is in the machine. If the belt keeps moving after that, the
protective device has been defeated and the thing it was protecting against happens.

{{show: benchmarks/manufacturing/g_conveyor_interlock/props.yaml}}

That is the whole requirement: `conveyor` and `estop` never true together. It says
nothing about the guard, nothing about the beacon, and nothing about how the logic gets
there. A property is the claim you are prepared to defend, not a description.

## The correct program

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed estop, a run command and a normally closed guard drive the conveyor coil; a plain estop contact drives the warning beacon"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H130"/><path d="M146 52 H280"/><path d="M296 52 H430"/><path d="M446 52 H571"/><path d="M605 52 H672"/><path d="M130 40 V64"/><path d="M146 40 V64"/><path d="M126 66 L150 38"/><path d="M280 40 V64"/><path d="M296 40 V64"/><path d="M430 40 V64"/><path d="M446 40 V64"/><path d="M426 66 L450 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H130"/><path d="M146 110 H571"/><path d="M605 110 H672"/><path d="M130 98 V122"/><path d="M146 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="138" y="32">estop</text><text x="288" y="32">run_cmd</text><text x="438" y="32">guard_open</text><text x="588" y="32">conveyor</text><text x="138" y="90">estop</text><text x="588" y="90">warn</text></g></svg>

`conveyor := NOT estop AND run_cmd AND NOT guard_open`. Three contacts in series, and the
two protective ones are normally closed, so either of them breaks the path. This is how
an interlock is supposed to look.

{{files: benchmarks/manufacturing/g_conveyor_interlock/clean.xml | benchmarks/manufacturing/g_conveyor_interlock/bomb.xml | benchmarks/manufacturing/g_conveyor_interlock/props.yaml}}

{{record: g_conveyor_interlock__clean}}

Proved, with the ingestion gate passing. Nothing surprising, which is the
point: you need to know what the correct program looks like before the other one means
anything.

## The same machine, with something added

<svg class="diagram" viewBox="0 0 700 210" role="img" aria-label="The same rung with an added parallel branch: estop in series with maint bypasses the normally closed estop contact and rejoins before the run command"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V192"/><path d="M672 18 V192"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H100"/><path d="M116 52 H300"/><path d="M28 100 H100"/><path d="M116 100 H200"/><path d="M216 100 H300"/><path d="M300 52 V100"/><path d="M300 52 H380"/><path d="M396 52 H470"/><path d="M486 52 H571"/><path d="M605 52 H672"/><path d="M100 40 V64"/><path d="M116 40 V64"/><path d="M96 66 L120 38"/><path d="M100 88 V112"/><path d="M116 88 V112"/><path d="M200 88 V112"/><path d="M216 88 V112"/><path d="M380 40 V64"/><path d="M396 40 V64"/><path d="M470 40 V64"/><path d="M486 40 V64"/><path d="M466 66 L490 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 160 H100"/><path d="M116 160 H571"/><path d="M605 160 H672"/><path d="M100 148 V172"/><path d="M116 148 V172"/><path d="M578 146 Q564 160 578 174"/><path d="M598 146 Q612 160 598 174"/></g><circle cx="300" cy="52" r="3.5" fill="currentColor"/><circle cx="300" cy="100" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="108" y="32">estop</text><text x="108" y="80">estop</text><text x="208" y="80">maint</text><text x="388" y="32">run_cmd</text><text x="478" y="32">guard_open</text><text x="588" y="32">conveyor</text><text x="108" y="140">estop</text><text x="588" y="140">warn</text></g></svg>

One branch, four elements, and the interlock is gone:

```
conveyor := (NOT estop OR (estop AND maint)) AND run_cmd AND NOT guard_open
```

The added path conducts precisely when the emergency stop *is* pressed and a maintenance
key is turned. Everywhere else in the input space the two programs behave identically.
Run the machine normally, for years, and you will never see the difference.

{{predict: g_conveyor_interlock__bomb | You have the rung and the property. Before scrolling, decide what the checker reports and whether the gate passes.}}

{{record: g_conveyor_interlock__bomb}}

## Read the counterexample

Both builds refute it, and the trace is the recipe:

```
run_cmd    = 1
estop      = 1
guard_open = 0
maint      = 1
conveyor   = 1
```

The emergency stop is pressed and the belt is running. Notice what the verifier handed
you: not a warning that something looks odd, but the exact input combination that opens
the hole. That combination is the trigger, and recovering it is what
[trigger synthesis](../../benchmarks/manufacturing/g_conveyor_interlock/index.md) means
in the suite's vocabulary.

## Why this is a bomb and not a bug

A bug is a mistake. Look at the added branch and ask what mistake produces it. Nobody
types a series pair of `estop` and `maint` by accident, and nobody wires it in parallel
with the normally closed contact that it exactly cancels. The branch is deliberate,
targeted at the one contact that matters, and dormant until a specific input pattern
appears.

That shape has a name in the literature, a logic-level bomb, and three parts you can
point at in the drawing:

| part | here |
|---|---|
| trigger | `estop AND maint`, an input pattern no operator asserts by accident |
| payload | bypass the interlock, energize the conveyor |
| dormancy | identical to the correct program until the pattern occurs |

Eleven more benchmarks in this suite carry the same attack fitted to a different plant:
a busbar, a batch reactor, a traffic junction, an elevator door. The plant changes and
the shape does not.

## Both routes reach this, eventually

Both programs now carry a verdict from the ladder front end and from the C route, which
is what an independent check is supposed to look like: the same conclusion arrived at
through Beremiz and MatIEC rather than through the front end under test.

{{record: g_conveyor_interlock__bomb__viac}}

Getting the second column took a detour worth recording. For a long time this page showed
one column here, because Beremiz crashed while rendering this ladder:

```
File "PLCGenerator.py", line 1079, in FactorizePaths
    factorized_paths.sort()
TypeError: '<' not supported between instances of 'list' and 'str'
```

`factorized_paths` holds strings and lists at once and Python 3 declines to order the
two, so the clean rung came through only because its branches are the same length, while
this one sets a one-element branch beside a two-element branch and mixes the types in
precisely the way that sort cannot handle.

The defect is a Python 3 porting bug in Beremiz rather than anything about the conveyor.
It is filed as [beremiz#83](https://github.com/beremiz/beremiz/issues/83) with a fix in
[PR #84](https://github.com/beremiz/beremiz/pull/84), and the record above names its
Beremiz as commit `df4370c`, which is that branch. Until the PR lands, reproducing this
column means building from it.

A benchmark suite that records what happened rather than what should have happened
collects these, and occasionally gets to fix one.

## What to take from this

The property did the work. It named a physical hazard, it was short enough to argue
about, and it was strong enough that a deliberately hidden branch could not satisfy it.
Nothing about the code review found this bomb; the requirement did.
