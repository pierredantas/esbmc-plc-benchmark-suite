A reversing starter is one motor with two contactors. `KM_CW` closes to turn it
clockwise, `KM_CCW` counter-clockwise. Close both at once and you short two supply
phases straight through the reversing contacts, so the interlock here is wiring
protection rather than a process preference. Nobody gets a second chance to test it
on real switchgear.

## The rung

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a forward command and a normally closed reverse contact drive the clockwise contactor; a plain reverse command drives the counter-clockwise contactor"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M296 66 L320 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H140"/><path d="M156 110 H571"/><path d="M605 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">fwd</text><text x="308" y="32">rev</text><text x="588" y="32">KM_CW</text><text x="148" y="90">rev</text><text x="588" y="90">KM_CCW</text></g></svg>

`KM_CW := fwd AND NOT rev`, `KM_CCW := rev`. Rung 1 carries the interlock. Its normally-closed `rev` contact drops `KM_CW` the
moment reverse is asked for, and rung 2 needs no guard of its own because rung 1
already breaks the pair.

!!! warning "The extension is load-bearing"
    The file is called `interlock.ld` and its content is PLCopen XML. ESBMC's LD
    front end keys off the extension, then XML-parses what it finds. Rename the file
    to `interlock.xml` and the front end rejects it. Hand it a textual LD DSL and it
    rejects that too.

{{files: demo/interlock.ld | demo/interlock_bug.ld | demo/props.yaml}}

{{code: demo/interlock.ld}}

## The property

{{show: demo/props.yaml}}

`mutual_exclusion` takes a variable list and nothing else. The justification is not
decoration: it is the line a reviewer reads to decide whether this property is the
right one for that hazard.

## Proving it

{{record: interlock_safe}}

k-induction is the mode for a program you expect to be safe. It proves the property
for every scan rather than for the first twenty, and the line naming the inductive
step at k = 2 is what tells you the proof closed.

## Breaking it

`interlock_bug.ld` is the same file with one element deleted. The `|/|` contact on
`rev` is gone from rung 1, so `KM_CW := fwd`, and nothing stops both contactors
closing.

{{record: interlock_viol}}

Read the trace in order. Both `fwd` and `rev` come up true in one scan, `KM_CCW`
follows `rev`, `KM_CW` follows `fwd` with nothing to block it, and the property fails
on the pair. Twelve milliseconds, one scan, one short circuit.

## What the front end encoded

Read the tab above. The front end builds a guarded accumulator, `pf10`, sets it to 1 only
when the branch conducts, and then assigns `KM_CW=1 && pf10`. On this rung that is just a
longhand spelling of `KM_CW = fwd`, because only one path runs through it. Put two paths in
parallel and the accumulator stops being ceremony and starts deciding the verdict. Lesson
1.2 is [where it does](../series-parallel/index.md).

Watch the ingestion gate column as well. It reports whether the property's variables
were assigned anywhere inside the scan loop. A front end that drops a body silently
leaves an empty loop behind, and an empty loop satisfies every safety property you can
write. The gate is what separates a proof from a shrug.

## Try it yourself

Open `interlock.ld`, find the `<contact negated="true">` element whose variable is
`rev`, and delete it. You have just written `interlock_bug.ld`. Or leave the program
alone and rewrite the property as `kind: invariant` with
`expression: "!(KM_CW && KM_CCW)"`, which says the same thing in C operators and is
accepted, while the IEC spelling of that same formula, `NOT (KM_CW AND KM_CCW)`, is
rejected by the property parser.

[Reproducing](../../reproducing.md) has the commands.
