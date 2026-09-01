A sectional door on a loading bay closes at about half a meter per second and weighs
enough to matter. A photo-eye across the opening catches anything in the way. What the
door does next is the whole of the safety function, and EN 13241 is specific about it:
the door reverses. Stopping is not enough.

The difference shows up when the obstruction clears. A door that paused resumes closing,
onto whatever moved.

## The rungs

<svg class="diagram" viewBox="0 0 700 340" role="img" aria-label="Three rungs: reversing or beam in parallel, gated by normally closed top limit, latches reversing; close command with normally closed beam and normally closed reversing drives move down; open command or reversing in parallel drives move up"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V322"/><path d="M672 18 V322"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H320"/><path d="M28 82 H140"/><path d="M156 82 H240"/><path d="M240 82 H320"/><path d="M320 52 V82"/><path d="M320 52 H396"/><path d="M412 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M140 70 V94"/><path d="M156 70 V94"/><path d="M396 40 V64"/><path d="M412 40 V64"/><path d="M392 66 L416 38"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 158 H140"/><path d="M156 158 H270"/><path d="M286 158 H400"/><path d="M416 158 H571"/><path d="M605 158 H672"/><path d="M140 146 V170"/><path d="M156 146 V170"/><path d="M270 146 V170"/><path d="M286 146 V170"/><path d="M266 172 L290 144"/><path d="M400 146 V170"/><path d="M416 146 V170"/><path d="M396 172 L420 144"/><path d="M578 144 Q564 158 578 172"/><path d="M598 144 Q612 158 598 172"/><path d="M28 234 H140"/><path d="M156 234 H320"/><path d="M28 264 H140"/><path d="M156 264 H320"/><path d="M320 234 V264"/><path d="M320 234 H571"/><path d="M605 234 H672"/><path d="M140 222 V246"/><path d="M156 222 V246"/><path d="M140 252 V276"/><path d="M156 252 V276"/><path d="M578 220 Q564 234 578 248"/><path d="M598 220 Q612 234 598 248"/></g><circle cx="320" cy="52" r="3.5" fill="currentColor"/><circle cx="320" cy="82" r="3.5" fill="currentColor"/><circle cx="320" cy="234" r="3.5" fill="currentColor"/><circle cx="320" cy="264" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">Reversing</text><text x="148" y="112">Beam</text><text x="404" y="32">TopLimit</text><text x="588" y="32">Reversing</text><text x="148" y="138">CloseCmd</text><text x="278" y="138">Beam</text><text x="408" y="138">Reversing</text><text x="588" y="138">MoveDown</text><text x="148" y="214">OpenCmd</text><text x="148" y="294">Reversing</text><text x="588" y="214">MoveUp</text></g></svg>

`Reversing := (Reversing OR Beam) AND NOT TopLimit`, `MoveDown := CloseCmd AND NOT Beam
AND NOT Reversing`, `MoveUp := OpenCmd OR Reversing`. `Reversing` latches on the beam and
holds until the top limit. The latch is the safety function. Everything else is plumbing.

{{files: benchmarks/building_automation/g_door_reversal/program.xml | benchmarks/building_automation/g_door_reversal/momentary.xml | benchmarks/building_automation/g_door_reversal/props.yaml | benchmarks/building_automation/g_door_reversal/reversal_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/building_automation/g_door_reversal/props.yaml}}

{{record: g_door_reversal__program}}

The variant beside it drops the self-hold branch, leaving `Reversing := Beam AND NOT
TopLimit`. Reversal now lasts exactly as long as the obstruction does.

{{predict: g_door_reversal__momentary | The reversal is momentary: it ends when the beam clears. Does the door still refuse to drive down through a broken beam?}}

`NOT Beam` sits in the drive-down rung directly, so the property holds whatever the
latch does. It is true of a door that reverses and true of a door that pauses and
resumes, which are different machines with different accident reports.

## The discriminator

{{show: benchmarks/building_automation/g_door_reversal/reversal_check.props.yaml}}

{{record: door_reversal_latched}}

Commit to an answer before reading on.

Refuted, which is the right answer: a latched reversal outlives the beam.

It is worth knowing what a wrong answer here would look like. Lesson 1.4 sets out the
flattening a ladder front end can apply to a coil fed by two parallel branches:

```
ASSIGN Reversing = 1 && Reversing && !TopLimit;
ASSIGN Reversing = 1 && Beam && !TopLimit;
```

The second assignment overwrites the first, the self-hold is gone, and what gets verified
is the momentary door. Such a proof is sound about the program it built. That program is
not the one in the file.

{{record: door_reversal_momentary}}

The momentary variant proves it, as it should, because here there is no latch to lose.

## What to take from it

The discriminator was written to separate two designs, and it separates two toolchains for
free, because any property sensitive to whether a latch still holds its value after the set
condition has gone away is equally sensitive to whether the front end built a latch in the
first place. A check that catches this class of defect in a plant program catches it in the
verifier too. Write one even when you trust the code.
