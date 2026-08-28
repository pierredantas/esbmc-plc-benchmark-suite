Parts 1 through 5 were ladder, with two exceptions nobody dwelt on. This part is about the
notations the suite ships and the ladder front end cannot read.

It is also the part of this site with a date on it. Everything below used to describe a
tool that read nothing and said nothing about it. That defect was reported as
[esbmc#7354](https://github.com/esbmc/esbmc/issues/7354) and fixed on 28 August 2026, so
the runs on this page now show the front end refusing the file by name. The lesson is kept,
and rerecorded, because the interesting part was never the verdict. It was how long a
corpus can carry a silent one.

## An air handler permissive

A supply fan and a motorized damper. The fan may run only when the damper is open, because
a fan pulling against a shut damper puts the full static pressure on the duct as vacuum and
the duct can collapse. A duct smoke detector drops the fan, since a running fan distributes
smoke into every zone it serves.

Three inputs, one output, one AND:

<svg class="diagram" viewBox="0 0 600 180" role="img" aria-label="Function block diagram: fan_cmd, damper_open and the negation of smoke feed a three-input AND block whose output drives fan"><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="20" y="26" width="100" height="26" rx="2"/><rect x="20" y="70" width="100" height="26" rx="2"/><rect x="20" y="118" width="100" height="26" rx="2"/><rect x="170" y="118" width="56" height="26" rx="2"/><rect x="280" y="26" width="76" height="118" rx="2"/><rect x="420" y="70" width="90" height="26" rx="2"/></g><g stroke="currentColor" fill="none" stroke-width="1.4"><path d="M120 39 H280"/><path d="M120 83 H280"/><path d="M120 131 H170"/><path d="M226 131 H280"/><path d="M356 83 H420"/></g><g fill="currentColor" font-size="12.5" text-anchor="middle"><text x="70" y="43">fan_cmd</text><text x="70" y="87">damper_open</text><text x="70" y="135">smoke</text><text x="198" y="135">NOT</text><text x="318" y="90">AND</text><text x="465" y="87">fan</text></g></svg>

{{show: benchmarks/hvac/fbd_fan_damper/props.yaml}}

Two properties, one per hazard. Neither says anything about how the logic reaches its
answer.

## The defect

{{files: benchmarks/hvac/fbd_fan_damper/clean.xml | benchmarks/hvac/fbd_fan_damper/bomb.xml | benchmarks/hvac/fbd_fan_damper/props.yaml}}

One wire is gone. The `damper_open` input no longer reaches the AND block, so the fan
answers to the command and the smoke detector and nothing else:

<svg class="diagram" viewBox="0 0 600 180" role="img" aria-label="The same diagram with the damper_open input removed: only fan_cmd and the negation of smoke reach the AND block"><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="20" y="26" width="100" height="26" rx="2"/><rect x="20" y="118" width="100" height="26" rx="2"/><rect x="170" y="118" width="56" height="26" rx="2"/><rect x="280" y="26" width="76" height="118" rx="2"/><rect x="420" y="70" width="90" height="26" rx="2"/></g><g stroke="currentColor" fill="none" stroke-width="1.4"><path d="M120 39 H280"/><path d="M120 131 H170"/><path d="M226 131 H280"/><path d="M356 83 H420"/></g><g fill="currentColor" font-size="12.5" text-anchor="middle"><text x="70" y="43">fan_cmd</text><text x="70" y="135">smoke</text><text x="198" y="135">NOT</text><text x="318" y="90">AND</text><text x="465" y="87">fan</text></g></svg>

Both files declare the same four variables. `damper_open` is still an input on the
interface, still named, still typed. Only the line on the drawing is missing, which is the
part a variable list cannot show you.

## What the ladder front end says

{{record: fbd_fan_damper__bomb}}

It stops before verification starts:

```
ERROR: UnsupportedConstruct(FBD body of POU 'air_handler', tier=2)
ERROR: PARSING ERROR
```

That is the whole answer, and it is the right one. The front end cannot read a function
block diagram, so it declines the file and names the construct and the POU.

It did not always. Until #7354 was fixed, the same file came back `unknown` with the
ingestion gate failing on `fan`, because the `<FBD>` body was discarded on the way in and
what got verified was a program with no logic in it. The clean variant was worse:

{{predict: fbd_fan_damper__clean | This is the correct air handler. On the build this site now records, what does the ladder route report?}}

{{record: fbd_fan_damper__clean}}

It errors too, and that is the improvement. This file used to return `SAFE` with the
gate failing, and a reader who checked only the clean row saw a verdict
that matched the expectation exactly. The proof was about an empty scan loop, which
satisfies every safety property ever written.

## What the second route says

{{record: fbd_fan_damper__bomb__viac}}

`VIOLATION`, and it names the property:

```
FAILED  [main.assertion.1]  line 13  P1
```

P1 is `!(fan && !damper_open)`, the duct-collapse property. Beremiz rendered the function
block diagram as Structured Text, MatIEC compiled that to C, and ESBMC's C front end read
what the ladder front end could not. Same file, same property, same solver, opposite
outcome.

The clean variant comes back `SAFE` on that route too, and this time it means the thing it
appears to mean.

## What the fix changed, and what it did not

Before, the clean air handler and the broken one produced the same word on the ladder
route, and a results table would have shown two green rows. Now both produce an error, and
the distinction between them lives entirely on the C route, where it always did.

Notice what the ingestion gate did across that change. It failed on these files when the
tool was silent, and it fails on them now that the tool is loud. It was never measuring the
verdict; it was measuring whether the property's variables were assigned inside the scan
loop, and the answer to that did not move.

Two of the site's runs still fail the gate while returning a confident verdict rather than
an error, and both are in [lesson 7.9](../two-hand-fb/index.md). That is a different defect,
in a different place, and it is not yet reported.

The next lesson is the same #7354 body-dropping defect producing the opposite error.
