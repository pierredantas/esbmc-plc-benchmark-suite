A reversing starter is one motor with two contactors. `KM_CW` closes to turn it
clockwise, `KM_CCW` counter-clockwise. Close both at once and you short two supply
phases straight through the reversing contacts, so the interlock here is wiring
protection rather than a process preference. Nobody gets a second chance to test it
on real switchgear.

## The ladder

```
Rung 1:  fwd ---| |----|/|--- ( KM_CW )       KM_CW  := fwd AND NOT rev
                       rev
Rung 2:  rev ---| |------------( KM_CCW )     KM_CCW := rev
```

Rung 1 carries the interlock. Its normally-closed `rev` contact drops `KM_CW` the
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

## What the two builds encoded

Compare the two tabs above. v8.4 writes `ASSIGN KM_CW=1 && fwd;` and moves on. master
builds a guarded accumulator, `pf10`, sets it to 1 only when the branch conducts, and
then assigns `KM_CW=1 && pf10`, which on this rung means exactly what v8.4 means,
because only one path runs through it. Put two paths in parallel and that difference
decides the verdict. Lesson 2 is [where it does](../seal-in/index.md).

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
