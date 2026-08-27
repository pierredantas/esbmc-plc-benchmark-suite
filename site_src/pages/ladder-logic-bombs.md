# Ladder logic bombs

Most attacks on industrial control systems in the public record went after the network,
the engineering workstation or the firmware. A ladder logic bomb goes after the control
logic itself: the rungs an engineer would open in the IDE and read.

The code is valid. It compiles, it downloads to the PLC, it passes a syntax check, and
for years it drives the plant correctly. Then a specific combination of inputs appears,
and it does something else.

## Where the term comes from

> Naman Govil, Anand Agrawal and Nils Ole Tippenhauer, *On Ladder Logic Bombs in
> Industrial Control Systems*, CyberICPS/SECPRE at ESORICS 2017, pages 110–126.
> [DOI 10.1007/978-3-319-72817-9_8](https://doi.org/10.1007/978-3-319-72817-9_8),
> preprint [arXiv:1702.05241](https://arxiv.org/abs/1702.05241).

Their abstract defines it directly: "we discuss ladder logic bombs, i.e. malware written
in ladder logic (or one of the other IEC 61131-3-compatible languages). Such malware would
be inserted by an attacker into existing control logic on a PLC, and either persistently
change the behavior, or wait for specific trigger signals to activate malicious
behaviour."

They abbreviate it LLB, place Stuxnet in the same lineage as a special case, and build
working examples on real PLCs in their lab.

Note the parenthesis in their own definition. The name says ladder because ladder is what
most plant logic is written in, but the idea is not confined to it, and a bomb in
Structured Text is the same object. This suite says **logic-level bomb** for that reason,
keeping the abbreviation and widening the expansion, because the catalog carries the same
attack in FBD, SFC and ST bodies as well as ladder.

## The three parts

<svg class="diagram" viewBox="0 0 620 120" role="img" aria-label="A correct rung: a normally closed stop contact in series with a run contact drives the pump coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V102"/><path d="M592 18 V102"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 60 H120"/><path d="M136 60 H290"/><path d="M306 60 H500"/><path d="M534 60 H592"/><path d="M120 48 V72"/><path d="M136 48 V72"/><path d="M116 74 L140 46"/><path d="M290 48 V72"/><path d="M306 48 V72"/><path d="M507 46 Q493 60 507 74"/><path d="M527 46 Q541 60 527 74"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="40">stop</text><text x="298" y="40">run</text><text x="517" y="40">pump</text></g></svg>

A pump runs when the operator commands it and stops when the stop button is pressed. The
stop contact is normally closed, so pressing the button breaks the path. This is the
shape every safety interlock in the standard takes.

<svg class="diagram" viewBox="0 0 620 175" role="img" aria-label="The same rung with an added parallel branch: stop in series with svc bypasses the normally closed stop contact and rejoins before the run contact"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V160"/><path d="M592 18 V160"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 60 H95"/><path d="M95 60 H120"/><path d="M136 60 H250"/><path d="M95 115 H120"/><path d="M136 115 H190"/><path d="M206 115 H250"/><path d="M95 60 V115"/><path d="M250 60 V115"/><path d="M250 60 H330"/><path d="M346 60 H450"/><path d="M484 60 H592"/><path d="M120 48 V72"/><path d="M136 48 V72"/><path d="M116 74 L140 46"/><path d="M120 103 V127"/><path d="M136 103 V127"/><path d="M190 103 V127"/><path d="M206 103 V127"/><path d="M330 48 V72"/><path d="M346 48 V72"/><path d="M457 46 Q443 60 457 74"/><path d="M477 46 Q491 60 477 74"/></g><circle cx="95" cy="60" r="3.5" fill="currentColor"/><circle cx="95" cy="115" r="3.5" fill="currentColor"/><circle cx="250" cy="60" r="3.5" fill="currentColor"/><circle cx="250" cy="115" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="40">stop</text><text x="338" y="40">run</text><text x="467" y="40">pump</text><text x="128" y="97">stop</text><text x="198" y="97">svc</text></g></svg>

One branch has been added around the stop contact, carrying `stop` and a service switch in
series. Written out:

```
pump := (NOT stop OR (stop AND svc)) AND run
```

Three things are worth naming separately, because defenses tend to address one and miss
the others.

| part | in this rung |
|---|---|
| **trigger** | `stop AND svc`, a combination no operator asserts on purpose |
| **payload** | the stop button stops working, and the pump keeps running |
| **dormancy** | with `svc` low the two programs are the same function, input for input |

Dormancy is the part that does the damage. The added branch conducts only when the stop
button is pressed *and* the service switch is on. Every other point in the input space,
which is to say every point reached in normal operation, produces exactly the output the
correct program produces.

## Why reading the code does not find it

Govil and colleagues make this point themselves: they "focus on stealthy LLBs, i.e. LLBs
that are hard to detect by human operators manually validating the program running in
PLCs."

The reason is structural rather than a matter of diligence. A reviewer reads a rung and
asks whether it looks like reasonable control logic, and the bombed rung does. Parallel
branches around a contact are ordinary. A service or maintenance input is ordinary. Nobody
holds the full input space in mind while reading, so the question "is there a combination
that defeats this interlock" is not the question a reader is actually answering.

Testing has the matching gap. A test suite covers the cases somebody thought of, and the
attacker picked a combination nobody would think of, which is the whole design criterion
for the trigger.

## A bomb is not a bug

The distinction matters for what you conclude when you find one.

A bug is a mistake, so ask what mistake produces this rung. Nobody types a series pair of
`stop` and `svc` by accident, and nobody wires that pair in parallel with precisely the
normally closed contact it cancels while leaving every other element of the interlock
untouched. The branch is deliberate, aimed at the one contact that carries the safety
function, and quiet until a chosen pattern appears.

That is why the catalog keeps a clean and a bombed variant of the same plant. The pair is
the evidence: same machine, same property, one added branch, and a verdict that flips.

## What the catalog carries

Thirty of the 68 benchmark tasks are tagged `llb`, spanning 63 program variants across ten
industrial domains. All thirty carry the `security` tag as well.

The paper sorts payloads into three classes, and the suite carries all three:

| payload class | what the attacker gets |
|---|---|
| actuator manipulation | a valve, contactor or breaker moves when it must not |
| sensor or HMI forgery | the operator is shown a plant state that is not the real one |
| denial of control | the controller stops producing output at all |

Denial of control is the one that looks least like a conventional bug, and fourteen
benchmarks carry the `non-termination` tag for it. A payload that never terminates never finishes a
scan, so the PLC stops updating outputs entirely, and no assertion about a variable's value
catches it. [Lesson 3.4](lessons/non-termination/index.md) works through that case.

Triggers in the catalog take three shapes: an input pattern, as in the rung above; a
counter that has to reach a threshold, so the bomb arms only after N scans; and a
comparison against a specific sensor value.

## Why a model checker is the right instrument

A bomb's defining property is that it hides everywhere except on a set the designer chose
to be small and strange. Searching that set by sampling is hopeless, and reading for it is
what the attacker already assumed you would do.

A bounded model checker does not sample. It asks whether *any* assignment of inputs, over
any reachable sequence of scans, reaches a state where the property is false, and it
answers by construction rather than by search over examples. When the answer is yes it
prints the assignment:

```
run  = 1
stop = 1
svc  = 1
pump = 1
```

That is the counterexample, and for a logic bomb it is also the trigger. The tool does not
report that something looks suspicious. It hands back the exact combination that opens the
hole, which is what [lesson 3.5](lessons/trigger-synthesis/index.md) means by recovering
the knock.

The limit is honest and worth stating: this finds a bomb only when you have written the
property it violates. A checker given no property to defend proves nothing, and
[lesson 3.6](lessons/what-a-property-says/index.md) is about that gap.

## Where to go next

[Part 3 of the lessons](lessons/what-is-an-llb/index.md) organizes these attacks by shape:
triggers, fuses that outrun the checker, denial of control, and trigger synthesis.
[Part 2](lessons/conveyor/index.md) fits the same attack to twelve plants in turn, starting
with a conveyor whose emergency stop is bypassed exactly as the rung above bypasses the
stop button.
