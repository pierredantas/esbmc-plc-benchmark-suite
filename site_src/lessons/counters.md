Counters are timers with the clock replaced by an event: a CTU counts rising edges on
its `CU` pin until the count reaches `PV` and then raises `Q`, while a CTD counts the
other way and raises `Q` when it hits zero. Both keep state across scans. That is what
puts them here, in the half of Part 1 where the order of things starts to matter.

## Counting up, with a reset

<svg class="diagram" viewBox="0 0 620 170" role="img" aria-label="Ladder rung: a Pulse contact into a CTU block with preset 2 and a Reset contact on the R pin, driving the Done coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V152"/><path d="M592 18 V152"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 56 H120"/><path d="M136 56 H250"/><path d="M370 56 H501"/><path d="M535 56 H592"/><path d="M120 44 V68"/><path d="M136 44 V68"/><path d="M28 118 H120"/><path d="M136 118 H250 V96"/><path d="M120 106 V130"/><path d="M136 106 V130"/><rect x="250" y="28" width="120" height="76" rx="3"/><path d="M508 42 Q494 56 508 70"/><path d="M528 42 Q542 56 528 70"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="36">Pulse</text><text x="128" y="98">Reset</text><text x="310" y="52">CTU</text><text x="310" y="72">PV = 2</text><text x="310" y="92">R</text><text x="518" y="36">Done</text></g></svg>

{{files: benchmarks/packaging/g_ctu_saturate/program.xml | benchmarks/packaging/g_ctu_saturate/props.yaml}}

{{record: ctu_saturate}}

`Done` and `Reset` never hold together, proved, with the gate passing and `CTU0__CV`
visible in the scan body. The counter is there, which is the precondition for the verdict
meaning anything.

The `R` pin is wired to a contact here, and the front end reads that contact's variable
straight through. Wire `R` to a chain of contacts instead and it prints a warning and
models no reset at all, which is the honest thing to do and worth knowing before you
draw one that way.

## Counting down, and a pin that is not read

The IEC count-down block reloads its preset through the `LD` pin. This program wires it:

{{files: benchmarks/elevator/g_ctd_load/program.xml | benchmarks/elevator/g_ctd_load/props.yaml}}

{{record: ctd_load}}

master reports a violation. It is right about the program it built, and the encoding
says why in three lines:

```
ASSIGN CTD0__CD=1 && pf3;
ASSIGN CTD0__CV=CTD0__CV + -1;
ASSIGN CTD0__Q=CTD0__CV <= 0;
```

`Load` appears once, as a nondeterministic input, and never again. The graphical block
reader looks for a pin named `R` and nothing else, so the `LD` wire is dropped on the
floor, and what remains is a counter that decrements every time its input conducts and
has no way back: `CV` runs negative, `Q` latches true, and `Empty` ends up true whatever
`Load` does. The load pin might as well not be there.

Under IEC semantics the requirement holds: a load restores the preset, `CV` is positive
again, and `Empty` goes low. The expected verdict stays SAFE and the task stays
`candidate`, because no tool has confirmed it and the one tool available here cannot.

## What to take from this

A wired pin that the tool ignores looks exactly like a wired pin that works. There is no
diagnostic, the file is schema-valid, and the verdict comes back with the confidence of
a proof. Only the encoding distinguishes them, which is why every panel on this site
prints it.
