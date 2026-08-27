This machine appears twice in the catalog: once as a ladder rung and once as a sequential
function chart. The same hazard is built into both, and the two bombs are not built the
same way. That difference is the lesson.

## The machine

An elevator car with a powered door and a drive. The door opens on request when the car
is level with a floor, and the drive runs when a move is commanded.

A car that travels with its door open exposes the running shaft to whoever is standing in
the doorway. It is the failure every lift interlock exists to prevent, and it is the
reason a lift has a door contact in series with the drive circuit rather than a signal
somewhere in software.

{{show: benchmarks/elevator/g_elevator_door/props.yaml}}

## As a ladder rung

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed move request, an open request and an at-floor contact drive the door open coil; a plain move request drives the drive coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H440"/><path d="M456 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M136 66 L160 38"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M440 40 V64"/><path d="M456 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H140"/><path d="M156 110 H571"/><path d="M605 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">move_req</text><text x="308" y="32">open_req</text><text x="448" y="32">at_floor</text><text x="588" y="32">door_open</text><text x="148" y="90">move_req</text><text x="588" y="90">drive</text></g></svg>

```
door_open := NOT move_req AND open_req AND at_floor
drive     := move_req
```

{{files: benchmarks/elevator/g_elevator_door/clean.xml | benchmarks/elevator/g_elevator_door/bomb.xml | benchmarks/elevator/sfc_elevator_door/clean.xml | benchmarks/elevator/sfc_elevator_door/bomb.xml}}

{{record: g_elevator_door__clean}}

The bombed rung is the branch you have seen three times now, and it puts the car in
motion with the door open:

{{record: g_elevator_door__bomb}}

```
open_req = 1   move_req = 1   at_floor = 1   maint = 1   ->   door_open = 1   and   drive = 1
```

Both builds catch it. Nothing new so far.

## As a sequential function chart

The same lift, written as the sequence it really is:

<svg class="diagram" viewBox="0 0 520 400" role="img" aria-label="Sequential function chart: Idle, then Opening with an N door_open action, Closing, and Moving with an N moving action, looping back to Idle"><defs><marker id="ar4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs><g stroke="currentColor" fill="none" stroke-width="1.5"><rect x="120" y="24" width="130" height="40" rx="2"/><rect x="124" y="28" width="122" height="32" rx="2"/><rect x="120" y="110" width="130" height="40" rx="2"/><rect x="120" y="196" width="130" height="40" rx="2"/><rect x="120" y="282" width="130" height="40" rx="2"/><rect x="290" y="114" width="130" height="32" rx="2"/><rect x="290" y="286" width="130" height="32" rx="2"/><path d="M185 64 V110"/><path d="M185 150 V196"/><path d="M185 236 V282"/><path d="M165 87 H205"/><path d="M165 173 H205"/><path d="M165 259 H205"/><path d="M185 322 V345"/><path d="M165 345 H205"/><path d="M250 130 H290"/><path d="M250 302 H290"/><path d="M185 345 V372 H60 V12 H185"/></g><path d="M179 14 L185 24 L191 14 Z" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="185" y="49">Idle</text><text x="185" y="135">Opening</text><text x="185" y="221">Closing</text><text x="185" y="307">Moving</text><text x="355" y="135">N  door_open</text><text x="355" y="307">N  moving</text></g><g fill="currentColor" font-size="12.5"><text x="216" y="92">call</text><text x="216" y="178">dwell_done</text><text x="216" y="264">door_closed</text><text x="216" y="350">at_floor</text></g></svg>

Four steps, four transitions, two actions. `door_open` is held while the chart sits in
Opening, `moving` while it sits in Moving, and since a chart is in one step at a time the
hazard is prevented by the structure rather than by a contact.

Now the bombed chart. Here is the entire difference between the two files:

```diff
-<action localId="40" qualifier="N"><reference name="door_open" /></action>
+<action localId="40" qualifier="S"><reference name="door_open" /></action>
```

One letter. `N` holds the action while its step is active and releases it on the way out.
`S` **stores** it: `door_open` is set on entry to Opening and no later step ever clears
it, so the car reaches Moving with the door still commanded open.

Nothing was added. The steps are the same steps, in the same order, with the same actions
attached to the same places. Print the two charts side by side and they are identical
drawings.

## What the verifier says about the chart

{{record: sfc_elevator_door__clean}}

{{record: sfc_elevator_door__bomb}}

Read the ingestion gate. It fails on both builds and on both variants, because ESBMC's
front end discards an `<SFC>` body without a diagnostic. The clean chart reports SAFE
having verified nothing, and the bombed chart reports `unknown`.

So the same hazard, in the same catalog, written by the same author: caught in ladder,
invisible in SFC. Not because the SFC bomb is subtler, but because the tool never read
the file. That is the coverage story from
[How ESBMC-PLC works](../../how-esbmc-plc-works.md) arriving where it costs something.

## Why the qualifier is a good place to hide

An attack does not have to add anything. Review by shape and you are looking for extra
branches, extra contacts, extra steps, and there are none here. The difference is an
attribute on an element that is supposed to be there, using a feature of the standard
that is entirely legitimate, and stored actions are common enough in real charts that
seeing one raises nothing.

The same trick exists in ladder: flip a `negated` attribute on a contact and the drawing
barely changes. `--ld-fault-injection` plants exactly that class of defect, negating
contact polarities and degrading Set and Reset coils to plain output coils, so you can
check your properties would notice.

## What to take from this

Two lessons, and they pull in opposite directions.

A benchmark suite has to carry the notations its tools cannot read. If this catalog held
only the ladder version, the SFC bomb would not exist to be missed, and the gap in
coverage would look like an absence of problems rather than an absence of evidence.

And a property is worth more than a review. Nothing about reading either chart finds the
`S`. The requirement `!(moving && door_open)` finds it the moment a tool can read the
body at all, which for this notation is a job still waiting to be done.
