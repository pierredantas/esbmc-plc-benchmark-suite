The conveyor bomb hurt whoever was standing at the machine. This one needs nobody
standing anywhere.

## The machine

A batch reactor with a feed valve, a pressure switch and a relief vent. The operator
commands a feed, an enable signal says the recipe permits it, and the pressure switch
says whether the vessel is already above its safe working limit. If pressure is high the
vent opens.

Feeding a vessel that is already over pressure adds mass to a system that cannot hold
what it has. Depending on the chemistry that is a relief lift, a rupture disc, or a
runaway that outruns the relief entirely. Nobody has to be nearby for it to matter, and
by the time an operator notices, the decision was made several minutes earlier.

{{show: benchmarks/chemical_batch/g_batch_reactor/props.yaml}}

## The correct program

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed overpressure contact, a feed command and an enable drive the feed valve coil; a plain overpressure contact drives the vent"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H130"/><path d="M146 52 H290"/><path d="M306 52 H430"/><path d="M446 52 H571"/><path d="M605 52 H672"/><path d="M130 40 V64"/><path d="M146 40 V64"/><path d="M126 66 L150 38"/><path d="M290 40 V64"/><path d="M306 40 V64"/><path d="M430 40 V64"/><path d="M446 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H130"/><path d="M146 110 H571"/><path d="M605 110 H672"/><path d="M130 98 V122"/><path d="M146 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="138" y="32">overpressure</text><text x="298" y="32">feed_cmd</text><text x="438" y="32">enable</text><text x="588" y="32">feed_valve</text><text x="138" y="90">overpressure</text><text x="588" y="90">vent</text></g></svg>

`feed_valve := NOT overpressure AND feed_cmd AND enable`, and separately
`vent := overpressure`. The pressure switch appears twice, once to block the feed and
once to open the relief. Remember that second rung.

{{files: benchmarks/chemical_batch/g_batch_reactor/clean.xml | benchmarks/chemical_batch/g_batch_reactor/bomb.xml | benchmarks/chemical_batch/g_batch_reactor/props.yaml | benchmarks/chemical_batch/g_batch_reactor/weakened.props.yaml}}

{{record: g_batch_reactor__clean}}

## The same machine, bypassed

<svg class="diagram" viewBox="0 0 700 210" role="img" aria-label="The same rung with an added parallel branch: overpressure in series with maint bypasses the normally closed overpressure contact and rejoins before the feed command"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V192"/><path d="M672 18 V192"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H100"/><path d="M116 52 H300"/><path d="M28 100 H100"/><path d="M116 100 H200"/><path d="M216 100 H300"/><path d="M300 52 V100"/><path d="M300 52 H380"/><path d="M396 52 H470"/><path d="M486 52 H571"/><path d="M605 52 H672"/><path d="M100 40 V64"/><path d="M116 40 V64"/><path d="M96 66 L120 38"/><path d="M100 88 V112"/><path d="M116 88 V112"/><path d="M200 88 V112"/><path d="M216 88 V112"/><path d="M380 40 V64"/><path d="M396 40 V64"/><path d="M470 40 V64"/><path d="M486 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 160 H100"/><path d="M116 160 H571"/><path d="M605 160 H672"/><path d="M100 148 V172"/><path d="M116 148 V172"/><path d="M578 146 Q564 160 578 174"/><path d="M598 146 Q612 160 598 174"/></g><circle cx="300" cy="52" r="3.5" fill="currentColor"/><circle cx="300" cy="100" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="108" y="32">overpressure</text><text x="108" y="80">overpressure</text><text x="208" y="80">maint</text><text x="388" y="32">feed_cmd</text><text x="478" y="32">enable</text><text x="588" y="32">feed_valve</text><text x="108" y="140">overpressure</text><text x="588" y="140">vent</text></g></svg>

The same four elements as the conveyor, fitted to a different plant:

```
feed_valve := (NOT overpressure OR (overpressure AND maint)) AND feed_cmd AND enable
```

{{record: g_batch_reactor__bomb}}

```
feed_cmd = 1   overpressure = 1   enable = 1   maint = 1   ->   feed_valve = 1
```

## The part that makes this one nastier

Look at the third rung in the bombed drawing. `vent := overpressure` is untouched.

So when the attack fires the vessel is over pressure, the vent is open, the alarm that
vent drives is sounding, and the feed valve is open as well, which means every indication
an operator has says the protection is working, because it genuinely is. The relief does
exactly its job. Something upstream keeps adding to what it has to relieve.

An attacker who leaves the mitigations intact buys two things: the HMI looks correct, and
anyone reviewing the logic sees a vent rung that plainly handles overpressure and stops
reading.

## Which is how a property gets weakened

Now imagine the review that follows. Someone points out that a controlled blowdown does
sometimes feed while venting, and asks for the requirement to allow it. The property
grows an escape clause:

{{show: benchmarks/chemical_batch/g_batch_reactor/weakened.props.yaml}}

It reads reasonably. It is also fatal:

{{record: batch_reactor_weakened}}

Same bombed program, same verifier. **SAFE.** The escape clause is true
in exactly the scans the attack needs, because the attack does not touch the vent, so
`vent` is high whenever `overpressure` is. The requirement now excuses the one behavior
it existed to forbid.

Nothing in the tooling can catch that. Both builds are answering correctly; they were
asked a different question. The gate passes, the encoding is right, the proof closes at
k = 2.

## What to take from this

A property is only as strong as its weakest excuse. Every `unless` you write into a
safety requirement is a condition you have promised not to care about, and an attacker
reads your requirements too.

If a real process needs feed-while-venting, that is a different mode with its own
permissive and its own property, not a clause bolted onto the interlock. The suite keeps
both spellings here so the difference is one click apart:
`props.yaml` catches the bomb, `weakened.props.yaml` does not, and the programs are
identical.
