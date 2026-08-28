A gas burner lights in a fixed order, and EN 298 fixes it: run the fan long enough to
sweep the chamber, open the pilot, prove the flame, and only then admit main gas. Get
the order wrong and you are igniting a chamber that has been filling with fuel.

The second requirement is about what happens after a failure. A burner that fails to
light must go to lockout, and lockout is non-volatile: it needs somebody to walk up and
press reset. A controller that retries on its own is doing unsupervised ignition
attempts on a chamber that has already proved it will not light.

## The rungs

```
CallForHeat --| |--- ( Fan )

Lockout -----| |---+---|/|--- ( Lockout )    Lockout := (Lockout OR FlameFail) AND NOT ResetBtn
FlameFail ---| |---+   ResetBtn

CallForHeat -| |---| |---|/|--- ( Pilot )    Pilot := CallForHeat AND PurgeDone AND NOT Lockout
                 PurgeDone Lockout

CallForHeat -| |---| |---| |---|/|--- ( MainValve )
                 PurgeDone FlameProven Lockout
```

{{files: benchmarks/hvac/g_burner_purge/program.xml | benchmarks/hvac/g_burner_purge/self_clearing.xml | benchmarks/hvac/g_burner_purge/props.yaml | benchmarks/hvac/g_burner_purge/lockout_check.props.yaml}}

## The property everyone writes

{{show: benchmarks/hvac/g_burner_purge/props.yaml}}

{{record: g_burner_purge__program}}

That is the light-off order, and it is the property a commissioning engineer would ask
for. It says nothing whatever about lockout, so a controller with no lockout at all
satisfies it.

{{predict: g_burner_purge__self_clearing | In this variant the lockout follows the flame-fault contact and clears itself. Does the light-off order still hold?}}

## The discriminator

{{show: benchmarks/hvac/g_burner_purge/lockout_check.props.yaml}}

{{record: burner_lockout_latched}}

master refutes it. v8.4 proves it at k = 2 and is wrong, for the same reason as the door
in lesson 7.4: the two branches into `Lockout` become two assignments, the second wins,
and the latch v8.4 verified is a plain copy of `FlameFail AND NOT ResetBtn`.

{{record: burner_lockout_selfclearing}}

## Two lockouts, one verdict

Put the four runs together. On the correct program the two builds disagree, and on the
defective one they agree. A results table reporting one build would show a burner that
either does or does not latch depending on which column somebody read, and both columns
say `SAFE` for the property that was actually shipped.

The pattern is worth naming because it generalizes past this benchmark. Wherever a
requirement reduces to "this memory outlives its cause", the check for it is a
refutation, and a front end that quietly drops memory will pass it.
