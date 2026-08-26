Part 1 closes by putting the two halves together: a timer decides when something is
wrong, a latch remembers it, and an operator clears it.

## The circuit

<svg class="diagram" viewBox="0 0 620 170" role="img" aria-label="Two rungs: a Trig contact into a TON block driving a set coil on Alarm, and an Ack contact driving a reset coil on Alarm"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V152"/><path d="M592 18 V152"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 56 H120"/><path d="M136 56 H250"/><path d="M370 56 H501"/><path d="M535 56 H592"/><path d="M120 44 V68"/><path d="M136 44 V68"/><rect x="250" y="28" width="120" height="56" rx="3"/><path d="M508 42 Q494 56 508 70"/><path d="M528 42 Q542 56 528 70"/><path d="M28 126 H120"/><path d="M136 126 H501"/><path d="M535 126 H592"/><path d="M120 114 V138"/><path d="M136 114 V138"/><path d="M508 112 Q494 126 508 140"/><path d="M528 112 Q542 126 528 140"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="36">Trig</text><text x="310" y="52">TON</text><text x="310" y="72">PT = T#30ms</text><text x="518" y="36">S</text><text x="546" y="36">Alarm</text><text x="128" y="106">Ack</text><text x="518" y="106">R</text><text x="546" y="106">Alarm</text></g></svg>

A door obstruction that persists for three scans sets a latched alarm. An operator
acknowledgement clears it. `S` and `R` are set and reset coils: unlike an output coil,
they write only when power reaches them, and leave the variable alone otherwise.

{{files: benchmarks/elevator/g_timer_latch_mix/program.xml | benchmarks/elevator/g_timer_latch_mix/props.yaml}}

## The property and the run

{{show: benchmarks/elevator/g_timer_latch_mix/props.yaml}}

{{record: timer_latch_mix}}

Acknowledgement is dominant: the alarm and the acknowledgement never hold together.

## Why it is dominant, and why that should worry you

Look at the encoding. A set coil is a guarded write:

```
IF !(1 && T0__Q) THEN GOTO 7
ASSIGN Alarm=1;
7: ...
IF !(1 && Ack) THEN GOTO 9
ASSIGN Alarm=0;
```

The set runs, then the reset runs, so the reset wins in any scan where both conduct.
Reverse those two statements and the set would win, the alarm would survive its own
acknowledgement, and the property would fail.

Nothing in the file asks for that order. As [lesson 1.5](../edges-and-scan-order/index.md)
showed, the graphical front end takes the order of coils from `std::unordered_map`
iteration whenever the right power rail does not enumerate them. This program happens to
come out with the reset last. A file with one more contact in it might not.

So the verdict here is correct and the reason it is correct is an accident. If you depend
on reset dominance, and safety circuits usually do, wire the right power rail so the
order is written down, and state a property that fails if the order flips. That is the
same discipline as lesson 1.2's discriminator, applied to time instead of topology.

## End of Part 1

Eight lessons, and the pattern behind them is one sentence: a verdict describes the
program the tool built, not the program you drew. Contacts and coils were safe ground.
Parallel branches, rung order, timers and counters each gave a case where the two came
apart, and in every one of them the encoding said so plainly while the verdict did not.
