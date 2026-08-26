Every bomb in this part is a branch that lets something through under a special input.
So is every override ever requested by a client. This lesson is about telling them apart,
and the answer is not in the ladder.

## The machine

Lighting control for a building. Occupancy or a switch raises `demand`, and the lights
come on. A building-wide `master_off` overrides everything: end of day, holiday shutdown,
a fire panel signal. A `setback` output tells the BMS the building is in its off state.

{{show: benchmarks/building_automation/g_building_lighting/props.yaml}}

Read that property twice. It is not "the lights must never be on", and it is not about a
hazard in the sense the substation was. It says the override must **win**. The thing being
protected is the guarantee itself: whoever holds `master_off` is promised that asserting
it de-energizes the lights, and the whole point of an override is that it has no
exceptions.

## The program

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed master off contact and a demand contact drive the lights coil; a plain master off contact drives the setback coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H150"/><path d="M166 52 H340"/><path d="M356 52 H571"/><path d="M605 52 H672"/><path d="M150 40 V64"/><path d="M166 40 V64"/><path d="M146 66 L170 38"/><path d="M340 40 V64"/><path d="M356 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H150"/><path d="M166 110 H571"/><path d="M605 110 H672"/><path d="M150 98 V122"/><path d="M166 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="158" y="32">master_off</text><text x="348" y="32">demand</text><text x="588" y="32">lights</text><text x="158" y="90">master_off</text><text x="588" y="90">setback</text></g></svg>

```
lights  := NOT master_off AND demand
setback := master_off
```

{{record: g_building_lighting__clean}}

## And the bomb

```
lights := (NOT master_off OR (master_off AND maint)) AND demand
```

{{record: g_building_lighting__bomb}}

```
demand = 1   master_off = 1   maint = 1   ->   lights = 1
```

## Now describe that branch without the word "bomb"

Try it. The added path lets the lights respond to demand even when the building is in its
off state, provided a maintenance input is asserted.

That is a cleaning crew working after the holiday shutdown. It is a contractor who needs
light in a plant room at 3am. It is the facilities manager who rang last winter because
the master-off left an engineer in the dark on a roof. Every one of those is a real
request, every one produces this branch, and a competent integrator would implement it
exactly this way.

The ladder cannot tell you which happened. Neither can the counterexample: ESBMC hands
you `master_off = 1, maint = 1, lights = 1` and that is equally the description of a
working feature and a working attack.

## What actually distinguishes them

Somebody wrote down that the override must always win, and did not write down an
exception for maintenance.

That is the entire difference, and it lives in `props.yaml` rather than in the program.
The property is the record of an intention. Where there is no property, there is no fact
of the matter about whether a branch is a feature: there is only whatever the last person
to touch the program believed.

This is why [lesson 2.2](../batch-reactor/index.md)'s weakened property matters so much.
If the requirement had read *the master-off de-energizes the lights unless maintenance is
asserted*, this same branch would verify, and it would be a feature. Not because anything
about the plant changed, but because somebody agreed to it in writing.

## The uncomfortable corollary

A verification result is only as trustworthy as the requirement it was checked against,
and requirements are written by people under pressure from other people who want the
lights on.

So the review that matters is not of the code. It is of the property: who asked for this
exception, what does it let through, and would they have asked if the consequence were
spelled out in the same sentence? On a lighting circuit that conversation is about
comfort and energy. On [the substation](../substation/index.md) it is the same
conversation about an arc flash, and the same maintenance key.

That is the argument this suite exists to support. Programs are cheap to check once you
have said what must never happen. Saying what must never happen, precisely enough to
check and honestly enough to defend, is the work.
