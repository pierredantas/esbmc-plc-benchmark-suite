Parts 1 through 5 were ladder, with two exceptions nobody dwelt on. This part is about the
notations the suite ships and the ladder front end cannot read, starting with the one where
the tool says the least and means it the most.

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

`unknown`, on both builds, with the ingestion gate failing on `fan`.

Read the scan body in that panel. It assigns the three inputs a nondeterministic value and
stops. There is no `fan` in it, no AND, no NOT: the `<FBD>` body was dropped on the way in,
and what got verified was a program with no logic. `unknown` is the honest end of that,
since the harness has nothing to decide.

The clean variant is worth a glance for the same reason. This one is worth predicting
first, because the verdict and the expectation agree and that is exactly what makes it
misleading:

{{predict: fbd_fan_damper__clean | This is the correct air handler, expected SAFE. The ladder route agrees. Does that agreement mean the program was verified?}}

{{record: fbd_fan_damper__clean}}

`SAFE` on both builds, gate failing on both. That verdict is not a proof of anything about
the air handler. It is a proof about an empty scan loop, which satisfies every safety
property ever written, and the only reason the page can tell you so is that the gate ran
alongside it.

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

## Why this is the sharpest case in the suite

Everywhere else, a dropped body cost a verdict. Here it costs the distinction between a
working air handler and a broken one, and the tool reports the same word for both if you
only read the clean row.

[Issue #7354](https://github.com/esbmc/esbmc/issues/7354) is the defect: a program POU whose
body is not `<LD>` is discarded without a diagnostic. Six of the catalog's FBD variants sit
on it. The next lesson is the same defect producing the opposite error.
