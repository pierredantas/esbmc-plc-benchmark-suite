A gas burner lights in a fixed order, and EN 298 fixes it: run the fan long enough to
sweep the chamber, open the pilot, prove the flame, and only then admit main gas. Get
the order wrong and you are igniting a chamber that has been filling with fuel.

The second requirement is about what happens after a failure. A burner that fails to
light must go to lockout, and lockout is non-volatile: it needs somebody to walk up and
press reset. A controller that retries on its own is doing unsupervised ignition
attempts on a chamber that has already proved it will not light.

## The rungs

<svg class="diagram" viewBox="0 0 700 400" role="img" aria-label="Four rungs: call for heat drives the fan; lockout or flame fail in parallel, gated by normally closed reset button, latches lockout; call for heat, purge done and normally closed lockout drive pilot; call for heat, purge done, flame proven and normally closed lockout drive main valve"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V382"/><path d="M672 18 V382"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H571"/><path d="M605 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 128 H140"/><path d="M156 128 H320"/><path d="M28 158 H140"/><path d="M156 158 H240"/><path d="M240 158 H320"/><path d="M320 128 V158"/><path d="M320 128 H396"/><path d="M412 128 H571"/><path d="M605 128 H672"/><path d="M140 116 V140"/><path d="M156 116 V140"/><path d="M140 146 V170"/><path d="M156 146 V170"/><path d="M396 116 V140"/><path d="M412 116 V140"/><path d="M392 142 L416 114"/><path d="M578 114 Q564 128 578 142"/><path d="M598 114 Q612 128 598 142"/><path d="M28 224 H140"/><path d="M156 224 H270"/><path d="M286 224 H400"/><path d="M416 224 H571"/><path d="M605 224 H672"/><path d="M140 212 V236"/><path d="M156 212 V236"/><path d="M270 212 V236"/><path d="M286 212 V236"/><path d="M400 212 V236"/><path d="M416 212 V236"/><path d="M396 238 L420 210"/><path d="M578 210 Q564 224 578 238"/><path d="M598 210 Q612 224 598 238"/><path d="M28 292 H140"/><path d="M156 292 H240"/><path d="M256 292 H340"/><path d="M356 292 H440"/><path d="M456 292 H571"/><path d="M605 292 H672"/><path d="M140 280 V304"/><path d="M156 280 V304"/><path d="M240 280 V304"/><path d="M256 280 V304"/><path d="M340 280 V304"/><path d="M356 280 V304"/><path d="M440 280 V304"/><path d="M456 280 V304"/><path d="M436 306 L460 278"/><path d="M578 278 Q564 292 578 306"/><path d="M598 278 Q612 292 598 306"/></g><circle cx="320" cy="128" r="3.5" fill="currentColor"/><circle cx="320" cy="158" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">CallForHeat</text><text x="588" y="32">Fan</text><text x="148" y="108">Lockout</text><text x="148" y="188">FlameFail</text><text x="404" y="108">ResetBtn</text><text x="588" y="108">Lockout</text><text x="148" y="204">CallForHeat</text><text x="278" y="204">PurgeDone</text><text x="408" y="204">Lockout</text><text x="588" y="204">Pilot</text><text x="148" y="272">CallForHeat</text><text x="248" y="272">PurgeDone</text><text x="348" y="272">FlameProven</text><text x="448" y="272">Lockout</text><text x="588" y="272">MainValve</text></g></svg>

`Lockout := (Lockout OR FlameFail) AND NOT ResetBtn`, `Pilot := CallForHeat AND PurgeDone
AND NOT Lockout`, `MainValve := CallForHeat AND PurgeDone AND FlameProven AND NOT Lockout`.

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
