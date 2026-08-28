Three benchmarks in one lesson, because reading them apart misses the thing they say
together.

A substation has layers. The busbar has an interlock, the breaker has a protection
interlock, the transformer has a thermal one. They were designed by different people at
different times against different failures, and that independence is the whole argument
for defense in depth.

| benchmark | what must never happen |
|---|---|
| `g_busbar_interlock` | two feeders energize the bus in parallel |
| `g_substation_breaker` | the breaker closes into an active fault |
| `g_transformer_protect` | the transformer energizes with the oil over temperature |

The person these protect is the operator standing at the panel doing a switching
operation, holding a written procedure that assumes every one of them works.

{{files: benchmarks/power_substation/g_substation_breaker/clean.xml | benchmarks/power_substation/g_substation_breaker/bomb.xml | benchmarks/power_substation/g_substation_breaker/props.yaml}}

## The breaker

<svg class="diagram" viewBox="0 0 700 150" role="img" aria-label="Two rungs: a normally closed fault contact, a close command and a normally closed lockout drive the breaker closed coil; a plain fault contact drives the alarm"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M672 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H140"/><path d="M156 52 H300"/><path d="M316 52 H450"/><path d="M466 52 H556"/><path d="M590 52 H672"/><path d="M140 40 V64"/><path d="M156 40 V64"/><path d="M136 66 L160 38"/><path d="M300 40 V64"/><path d="M316 40 V64"/><path d="M450 40 V64"/><path d="M466 40 V64"/><path d="M446 66 L470 38"/><path d="M563 38 Q549 52 563 66"/><path d="M583 38 Q597 52 583 66"/><path d="M28 110 H140"/><path d="M156 110 H556"/><path d="M590 110 H672"/><path d="M140 98 V122"/><path d="M156 98 V122"/><path d="M563 96 Q549 110 563 124"/><path d="M583 96 Q597 110 583 124"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="148" y="32">fault</text><text x="308" y="32">close_cmd</text><text x="458" y="32">lockout</text><text x="573" y="32">breaker_closed</text><text x="148" y="90">fault</text><text x="573" y="90">alarm</text></g></svg>

```
breaker_closed := NOT fault AND close_cmd AND NOT lockout
alarm          := fault
```

Two protective contacts in series, both normally closed. The fault contact says the
protection has picked up. The lockout says a human has to reset something before this
breaker closes again.

{{record: g_substation_breaker__clean}}

The bombed rung is the branch this part has shown five times, wrapped around the fault
contact:

```
breaker_closed := (NOT fault OR (fault AND maint)) AND close_cmd AND NOT lockout
```

{{record: g_substation_breaker__bomb}}

## Read what the attacker left alone

```
close_cmd = 1   fault = 1   lockout = 0   maint = 1   ->   breaker_closed = 1
```

`lockout = 0`. The `NOT lockout` contact is still in series and still doing its job. The
bomb bypasses one of the two protective contacts and leaves the other untouched.

That is not the attacker running out of ideas. It is a choice between two layers that
behave very differently:

- **`fault`** is asserted by protection relays. Nobody clears it by hand, so a program
  that ignores it looks normal from outside.
- **`lockout`** is reset by an operator, as a routine step in restoring supply after a
  trip. Bypassing it changes what the operator sees on the panel.

Defeat the layer nobody touches and the plant behaves normally. Defeat the layer the
operator drives and somebody notices the first time the panel disagrees with the
procedure. The attack survives *because* it left a protection working.

## The other two

The transformer is the same rung with different names:

```
transformer_on := (NOT oil_temp_high OR (oil_temp_high AND maint)) AND energize_cmd AND NOT lockout
```

{{record: g_transformer_protect__bomb}}

```
energize_cmd = 1   oil_temp_high = 1   lockout = 0   maint = 1   ->   transformer_on = 1
```

The busbar has no lockout to leave alone, so the bypass is bare:

{{record: g_busbar_interlock__bomb}}

```
feeder_a_cmd = 1   feeder_b_cmd = 1   maint = 1   ->   feeder_a = 1   and   feeder_b = 1
```

Both feeders energizing the bus in parallel, which is the paralleling fault the interlock
exists to make impossible.

## What the three say together

Defense in depth assumes the layers fail independently. That assumption is doing all the
work, and it is a statement about *failures*: a relay sticks, a contact welds, a sensor
drifts, and each is unlucky on its own schedule.

A logic bomb is not a failure. It is one edit, in one program, that reaches every layer
implemented in that program. Here it is literally one input name, `maint`, appearing in
three interlocks that were never meant to have anything in common. An operator who
believes three independent protections stand between a command and an arc flash is
counting three things that are one thing.

Nothing about that is exotic. The three programs live in the same controller, were
written by the same integrator, and are maintained by whoever has the programming cable.
Independence of design does not survive shared implementation.

## And the verifier does not care

All three bombs are refuted in milliseconds, from properties short enough
to read aloud. The verifier has no notion of substations, layers or operators. It was
handed a claim about two Booleans and it found the assignment that breaks it.

That is worth stating because the argument above is the part a person has to make. The
tool tells you the property fails and hands you the inputs. Deciding that three
interlocks sharing one input is a structural problem rather than three separate bugs is
the reader's job, and it is the reason a benchmark suite is more useful than a bug list.
