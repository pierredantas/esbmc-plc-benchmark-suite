The first two machines in this part could hurt one person standing in the wrong place.
A junction hurts people who never see the controller and have no reason to distrust it.

## The machine

A two-phase signalized junction. North-south and east-west each have a demand input from
a loop detector, and each has a green. East-west holds priority: north-south greens only
when east-west is not asking.

Conflicting greens is the failure everyone means when they say a signal has failed. Two
streams of traffic are given right of way through the same conflict area at the same
time, at whatever speed the approach allows, and both drivers believe they have it.

{{show: benchmarks/traffic/g_traffic_light/props.yaml}}

This is the first `mutual_exclusion` property in this part. It takes a variable list
rather than an expression and becomes `assert(!(ns_green && ew_green))`, which is the
same claim the invariants in 2.1 and 2.2 made, written in the form that says what it is.

## The correct program

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed east-west request and a north-south request drive the north-south green; a plain east-west request drives the east-west green"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H150"/><path d="M166 52 H330"/><path d="M346 52 H571"/><path d="M605 52 H672"/><path d="M150 40 V64"/><path d="M166 40 V64"/><path d="M146 66 L170 38"/><path d="M330 40 V64"/><path d="M346 40 V64"/><path d="M578 38 Q564 52 578 66"/><path d="M598 38 Q612 52 598 66"/><path d="M28 110 H150"/><path d="M166 110 H571"/><path d="M605 110 H672"/><path d="M150 98 V122"/><path d="M166 98 V122"/><path d="M578 96 Q564 110 578 124"/><path d="M598 96 Q612 110 598 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="158" y="32">ew_req</text><text x="338" y="32">ns_req</text><text x="588" y="32">ns_green</text><text x="158" y="90">ew_req</text><text x="588" y="90">ew_green</text></g></svg>

```
ns_green := NOT ew_req AND ns_req
ew_green := ew_req
```

The conflict is prevented by one normally closed contact. East-west asking is enough to
hold north-south red, and there is no path by which both coils energize.

{{files: benchmarks/traffic/g_traffic_light/clean.xml | benchmarks/traffic/g_traffic_light/bomb.xml | benchmarks/traffic/g_traffic_light/props.yaml}}

{{record: g_traffic_light__clean}}

## The same junction, bypassed

The bomb is the shape you have now seen twice, and the third time it should be
recognizable before you read the caption: a parallel branch that conducts exactly when
the protective contact would have opened.

```
ns_green := (NOT ew_req OR (ew_req AND maint)) AND ns_req
```

{{record: g_traffic_light__bomb}}

```
ns_req = 1   ew_req = 1   maint = 1   ->   ns_green = 1   and   ew_green = 1
```

Both directions green, both detectors demanding, one maintenance input asserted.

## What this property does not say

Here is where a junction differs from a conveyor, and where an honest benchmark has to
be careful about what it claims.

`!(ns_green && ew_green)` is conflict-freedom and nothing else. Verify it and these
remain wide open:

**No intergreen.** Nothing stops `ns_green` dropping and `ew_green` rising in consecutive
scans, with no amber and no all-red between them. On a real junction that is the interval
that clears the conflict area, and it is measured in seconds, not scans.

**No minimum green.** A green can appear for exactly one scan and vanish.

**Starvation.** Hold `ew_req` high, by a stuck detector or a shorted loop, and
`ns_green` never comes up again. The safety property is perfectly content with a junction
that never serves one arm.

None of those three is expressible over this program, and that is not a limitation of the
verifier. The program has no memory of the previous scan and no notion of elapsed time,
so there is nothing to write the requirement over. Stating an intergreen means adding the
timer machinery from [lesson 1.6](../timers/index.md), and then stating it against a
model whose tick is a scan rather than a second.

## Why it is still worth proving

Because the three things it does not say cost delay, and the one thing it does say costs
lives. Conflict-freedom is the property that a signal engineer will not compromise, and
it is exactly the property this program is small enough to prove outright rather than
argue about.

The benchmark claims conflict-freedom and no more. A suite that says what it checks, and
is quiet about what it does not, is worth more to somebody validating a tool than one
whose properties imply a completeness they never had.
