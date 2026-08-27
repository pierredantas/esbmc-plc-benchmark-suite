Twelve machines, ten industrial domains, one attack. This page is the family portrait,
and it exists so the three benchmarks that have not had a lesson of their own are still
accounted for.

## The whole set

| domain | benchmark | what must never happen | lesson |
|---|---|---|---|
| manufacturing | `g_conveyor_interlock` | belt runs with the E-stop pressed | [2.1](../conveyor/index.md) |
| chemical_batch | `g_batch_reactor` | feed opens under overpressure | [2.2](../batch-reactor/index.md) |
| traffic | `g_traffic_light` | two conflicting greens | [2.3](../traffic-light/index.md) |
| elevator | `g_elevator_door` | car moves with the door open | [2.4](../elevator-door/index.md) |
| hvac | `g_hvac_fan_delay` | heating and cooling drive together | [2.5](../hvac-fan/index.md) |
| power_substation | `g_busbar_interlock` | two feeders parallel the bus | [2.6](../substation/index.md) |
| power_substation | `g_substation_breaker` | breaker closes into a fault | [2.6](../substation/index.md) |
| power_substation | `g_transformer_protect` | transformer energizes hot | [2.6](../substation/index.md) |
| building_automation | `g_building_lighting` | master-off fails to win | [2.7](../lighting-override/index.md) |
| chemical_batch | `g_batch_mixer` | mixer runs with the lid open | this page |
| packaging | `g_packaging_filler` | fill valve opens on a full bottle | this page |
| motor_control | `g_motor_interlock` | both contactors close | this page |

The last three are the same construction and need no separate walk-through. The mixer
guards a person reaching into a vessel. The filler guards a bottle that is already full,
so the cost is product on the floor rather than a hand in a machine. The motor interlock
is the reversing starter from [lesson 1.3](../interlock/index.md), carried into this part
as a catalog benchmark with its own clean and bombed pair.

Every one of the twelve is `validation_status: validated`, every one has a clean variant
and a seeded variant, and every one is refuted by both ESBMC builds.

## What is identical across all twelve

```
output := (NOT protective_input OR (protective_input AND maint)) AND command AND ...
```

A parallel branch, conducting exactly when the protective contact would have opened,
gated on an input that no normal operation asserts. Trigger, payload, dormancy, in four
elements.

Nothing about the plant appears in that shape. Swap the variable names and the busbar
becomes the conveyor. That is what makes it worth studying as a family rather than as
twelve incidents: an attacker who has this pattern does not need to understand your
process, only to find the contact that stands between a command and the thing it must
not do.

## What changes across the twelve

**Who gets hurt, and how fast.** The conveyor and the mixer injure whoever is at the
machine, immediately. The reactor and the transformer damage plant over minutes. The
filler spills product. The lighting circuit costs energy and a complaint.

**Whether the mitigations still work.** The reactor's vent keeps venting and the
substation's lockout keeps locking out, so the HMI looks correct while the attack runs.
That was the subject of [2.2](../batch-reactor/index.md) and it recurs everywhere the
plant has more than one protection.

**Whether the branch is even wrong.** [2.7](../lighting-override/index.md) is the same
edit as a legitimate maintenance override, and only the property decides.

**Whether a tool can see it.** [2.4](../elevator-door/index.md) has the same hazard as a
chart, where a one-letter change to an action qualifier is invisible to ESBMC because the
SFC body is never read.

## What this part does not cover

Every trigger here is an input pattern. Assert `maint` with the right conditions and the
payload fires in the same scan.

That is one shape out of several. A trigger can be a counter that reaches a threshold
after fifty scans, so nothing happens during commissioning and everything happens in
week three. It can be a comparison against a sensor value that only occurs at a
particular tank level. It can be a loop that stops terminating, so the payload is not a
wrong output but a controller that never completes a scan at all.

The suite has all of those. Thirty benchmarks carry the `llb` tag, and the twelve
here are the simplest twelve. The eight `g_tank_*` programs never terminate,
`tank_overflow` and `sensor_forge` arm on a fifty-scan fuse, and `counter_scalability`
sweeps a threshold up to 32767 to find where bounded checking gives out.

Those are organized by attack rather than by plant, which is the next part.

## The one thing to carry forward

A property caught every bomb in this part, and no property was longer than a line. None
of them required understanding the attack, or anticipating the attacker, or knowing that
an attacker existed. They required knowing what the machine must never do.

That is a much easier thing to write down, and it is the only thing that scales: there
are more ways to attack a program than anyone can enumerate, and one way for a conveyor
to be unsafe.
