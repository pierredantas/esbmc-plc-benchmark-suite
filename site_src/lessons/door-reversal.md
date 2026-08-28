A sectional door on a loading bay closes at about half a meter per second and weighs
enough to matter. A photo-eye across the opening catches anything in the way. What the
door does next is the whole of the safety function, and EN 13241 is specific about it:
the door reverses. Stopping is not enough.

The difference shows up when the obstruction clears. A door that paused resumes closing,
onto whatever moved.

## The rungs

```
Reversing --| |---+---|/|--- ( Reversing )   Reversing := (Reversing OR Beam) AND NOT TopLimit
Beam -------| |---+   TopLimit

CloseCmd ---| |---|/|---|/|--- ( MoveDown )  MoveDown := CloseCmd AND NOT Beam AND NOT Reversing
                 Beam  Reversing

OpenCmd ----| |---+--- ( MoveUp )            MoveUp := OpenCmd OR Reversing
Reversing --| |---+
```

`Reversing` latches on the beam and holds until the top limit. The latch is the safety
function. Everything else is plumbing.

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
