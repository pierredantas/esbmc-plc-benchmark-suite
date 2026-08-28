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

Refuted, which is the right answer: a latching lockout outlives the fault that set it. A
front end that flattened the two branches into `Lockout` would prove this instead, soundly,
about a lockout that is a plain copy of `FlameFail AND NOT ResetBtn`.

{{record: burner_lockout_selfclearing}}

## Two lockouts, one verdict

Put the four runs together. The property that was actually shipped, the light-off order,
says `SAFE` for the burner that latches and `SAFE` for the burner that does not. A results
table built from it would report a working lockout in both rows.

The pattern is worth naming because it generalizes past this benchmark. Wherever a
requirement reduces to "this memory outlives its cause", the check for it is a refutation,
and both a program without the memory and a front end that quietly drops it will pass
anything weaker.
