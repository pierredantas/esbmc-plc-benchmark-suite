This benchmark is called `g_hvac_fan_delay`. There is no delay in it. That is worth a
lesson of its own, because a benchmark id is a label somebody chose, and the only
trustworthy description of a program is the program.

## The machine

An air handling unit: a heating coil, a cooling coil and a supply fan, with an enable
that says the unit is commissioned to run. Zone controls raise a heat call or a cool
call.

Driving both coils at once is a fault every control specification forbids. The two fight
each other, the unit never reaches setpoint, and the energy goes on being spent for as
long as nobody notices. It is not the kind of hazard that hurts somebody in the next
second, which is exactly why it can run for a season before anyone looks.

{{show: benchmarks/hvac/g_hvac_fan_delay/props.yaml}}

## The program

<svg class="diagram" viewBox="0 0 700 200" role="img" aria-label="Three rungs: a normally closed cool call with a heat call and enable drive the heat coil; a cool call with enable drives the cool coil; enable alone drives the fan"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V182"/><path d="M672 18 V182"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 48 H140"/><path d="M156 48 H300"/><path d="M316 48 H450"/><path d="M466 48 H571"/><path d="M605 48 H672"/><path d="M140 36 V60"/><path d="M156 36 V60"/><path d="M136 62 L160 34"/><path d="M300 36 V60"/><path d="M316 36 V60"/><path d="M450 36 V60"/><path d="M466 36 V60"/><path d="M578 34 Q564 48 578 62"/><path d="M598 34 Q612 48 598 62"/><path d="M28 100 H140"/><path d="M156 100 H300"/><path d="M316 100 H571"/><path d="M605 100 H672"/><path d="M140 88 V112"/><path d="M156 88 V112"/><path d="M300 88 V112"/><path d="M316 88 V112"/><path d="M578 86 Q564 100 578 114"/><path d="M598 86 Q612 100 598 114"/><path d="M28 152 H140"/><path d="M156 152 H571"/><path d="M605 152 H672"/><path d="M140 140 V164"/><path d="M156 140 V164"/><path d="M578 138 Q564 152 578 166"/><path d="M598 138 Q612 152 598 166"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="28">cool_call</text><text x="308" y="28">heat_call</text><text x="458" y="28">enable</text><text x="588" y="28">heat</text><text x="148" y="80">cool_call</text><text x="308" y="80">enable</text><text x="588" y="80">cool</text><text x="148" y="132">enable</text><text x="588" y="132">fan</text></g></svg>

```
heat := NOT cool_call AND heat_call AND enable
cool := cool_call AND enable
fan  := enable
```

Cooling wins ties. The interlock is the normally closed `cool_call` contact in the heat
rung, and nothing else prevents the conflict.

{{files: benchmarks/hvac/g_hvac_fan_delay/clean.xml | benchmarks/hvac/g_hvac_fan_delay/bomb.xml | benchmarks/hvac/g_hvac_fan_delay/props.yaml}}

{{record: g_hvac_fan_delay__clean}}

The bombed variant is the branch this part has now shown five times, and both builds
refute it:

{{record: g_hvac_fan_delay__bomb}}

```
heat_call = 1   cool_call = 1   enable = 1   maint = 1   ->   heat = 1   and   cool = 1
```

## Now look at the third rung

`fan := enable`. The fan runs whenever the unit is enabled and stops the instant it is
not. There is no timer in this program. Not a badly configured one: none.

```
$ grep -c '<block' clean.xml
0
```

The benchmark's own metadata says so plainly, `features: [contacts, coils]`, so nothing
here is being hidden. The name promises a delay and the description does not, which
means somebody reading the catalog by id would form an expectation the file never had.

## What a fan delay is actually for

An electric heating element carries heat after its contactor drops. If the fan stops at
the same instant, that heat has nowhere to go: the element cooks, the thermal cutout
trips, and on a bad day the cutout is the only thing between you and a duct fire. So the
fan runs on for a fixed period after the heat call clears. That period is the purge, and
it is why real AHU logic has a timer that this program does not.

Written properly it is an off-delay, which is exactly
[lesson 1.6](../timers/index.md)'s `TOF`: `IN` falls, `Q` holds for `PT`, then drops. The
suite has that block exercised in `g_tof_hold` and the requirement to go with it.

## Why it is not simply added here

Because time in this model is counted in scans. `PT` is a number of scan cycles, not
seconds, so a thirty second purge on a ten millisecond task is three thousand scans. A
bounded search will not reach the end of that purge, and proving anything about it means
k-induction over the counter or an abstraction that replaces the count with a bound.

That is a real cost, and it is the honest reason the timer benchmarks in this suite are
small and separate from the machine benchmarks. Combining them would produce a task that
is realistic and unverifiable, which helps nobody.

## What to take from this

Read the program. The id told you there was a delay, the property said nothing about
fans at all, and the only place the truth was written down was the ladder and the
`features` list beside it.

Two habits follow. Check that the feature a benchmark is named for is present before you
count it as coverage of that feature. And when you write a suite, let the metadata carry
the claim, because a name gets copied into a paper and a `features` list gets checked by
a script.
