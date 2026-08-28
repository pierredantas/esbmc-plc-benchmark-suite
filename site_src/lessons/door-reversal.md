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

Read the two builds against each other before reading on.

master refutes it, which is the right answer: a latched reversal outlives the beam.
v8.4 proves it at k = 2, and v8.4 is wrong. The reason is the one lesson 1.4 sets out.
For a coil fed by two parallel branches, v8.4 emits one assignment per branch:

```
ASSIGN Reversing = 1 && Reversing && !TopLimit;
ASSIGN Reversing = 1 && Beam && !TopLimit;
```

The second overwrites the first, the self-hold is gone, and what v8.4 verified is the
momentary door. Its proof is sound about the program it built. That program is not the
one in the file.

{{record: door_reversal_momentary}}

Here both builds agree, because on the momentary variant there is no latch for v8.4 to
lose.

## What to take from it

The discriminator was written to separate two designs. It separated two builds as well,
and nobody planned that, because any property sensitive to whether a latch still holds
its value after the set condition has gone away is equally sensitive to whether the front
end built a latch in the first place. So a check that catches this class of defect in a
plant program catches it in the verifier too. Write one even when you trust the code.
