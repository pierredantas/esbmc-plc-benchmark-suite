A milling spindle does not stop when its contactor drops. It coasts, for a second or
two, and anybody who has opened a guard early has heard it. ISO 14119 handles that with
guard locking: the door stays locked until the hazardous movement has actually stopped,
which is a different moment from the one when the drive command goes away.

Every machine in this part so far has been untimed. Lesson 7.2 said outright that the
0.5 s synchrony window it needed was not in the model, and lesson 7.3 pushed the dead
time into an input. This one puts a real timer in the rung.

## The rungs

```
Motor --|/|---[ TON  ]---| |--- ( Unlocked )
              [T#30ms]  OpenReq

RunCmd --| |---| |---|/|--- ( Motor )
             DoorClosed OpenReq
```

The timer runs while the drive is off. Its output is the permission to release the
lock, and `OpenReq` in series after it means the guard opens on a request, but only once
the rundown has elapsed. The drive rung drops `Motor` the moment a request arrives, so
the two are never on together whatever the timer does.

{{files: benchmarks/manufacturing/g_guard_lock/program.xml | benchmarks/manufacturing/g_guard_lock/no_rundown.xml | benchmarks/manufacturing/g_guard_lock/props.yaml | benchmarks/manufacturing/g_guard_lock/rundown_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/manufacturing/g_guard_lock/props.yaml}}

{{record: g_guard_lock__program}}

Check the ingestion gate column before the verdict column. It passes, and the scan body
carries `Rundown__ET` and `Rundown__Q`, so the timer reached the solver. That check is not
ceremonial here: a front end that skipped the `TON` would leave `Unlocked` unassigned and
prove this property about a program with the timer rung missing.

Now the variant with the timer deleted, where the guard releases on the request alone.

{{predict: g_guard_lock__no_rundown | The rundown timer is gone and the door opens as soon as somebody asks. Does the guard still stay locked while the drive is energised?}}

It does, with the gate passing. `OpenReq` drops `Motor` in the same
rung that raises `Unlocked`, so the two cannot coincide however impatient the release
is. The property is about coincidence, and coasting is not coincidence.

## The discriminator

{{show: benchmarks/manufacturing/g_guard_lock/rundown_check.props.yaml}}

{{record: guard_rundown_locked}}

{{record: guard_rundown_immediate}}

Master refutes it on the timed guard and proves it on the untimed one, which is the
pattern this part has been running since 7.1. What is new is the shape of the question.
The other six discriminators asked whether a program remembers something. This one asks
whether it waits.

## What the timer costs

A timer is the most expensive thing in this part to verify, and the reason is visible in
the scan body. `Rundown__ET` is an integer the solver has to reason about across scans,
so the state space stops being a handful of booleans. The Structured Text twin makes the
point plainly: through the C route it takes 41 seconds, against hundredths for every
untimed machine in this part.

That cost is why a rundown interlock is a good thing to have a benchmark for. It is not
exotic, it is on most guarded machines in the building, and it is exactly the shape of
logic that a verifier is tempted to skip.
