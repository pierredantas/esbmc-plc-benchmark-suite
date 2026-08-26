# The five IEC 61131-3 languages

Ask how many languages IEC 61131-3 defines and you will be told five. That answer was
right for twenty years and is now out of date, so it is worth getting the current shape
of the standard straight before looking at the syntax.

Edition 4.0, published 2025-05-22, describes its suite as "the textual language
structured text (ST), and the graphical languages, ladder diagram (LD) and function
block diagram (FBD)". Sequential function chart sits outside that suite: "An additional
set of graphical and equivalent textual elements named sequential function chart (SFC)
is defined for structuring the internal organization of programs and function blocks".
Instruction list was deprecated in edition 3.0 in 2013 and removed outright in edition
4.0.

Those edition facts come from the IEC catalogue entries for
[IEC 61131-3:2025](https://webstore.iec.ch/en/publication/68533), edition 4.0 of
2025-05-22, and [IEC 61131-3:2013](https://webstore.iec.ch/en/publication/4552),
edition 3.0 of 2013-02-20.

So the standard today names three languages plus a structuring notation. Five names
still matter, because IL runs in installed plants that will outlive the standard that
dropped it, and because every tool you will benchmark still parses it. All five are
below.

| language | form | in Ed 4.0 (2025) | what it is for |
|---|---|---|---|
| LD | graphical | yes | boolean interlocks, drawn as relay contacts and coils |
| FBD | graphical | yes | signal flow, reusable blocks, analog chains |
| ST | textual | yes | arithmetic, loops, anything with structure |
| SFC | graphical, with textual equivalents | yes, as structuring elements | sequences: steps and the transitions between them |
| IL | textual | removed; deprecated since 2013 | legacy code you still have to read |

The first four examples below are the same program written four ways:

```
Run := (Start OR Run) AND NOT EStop
```

Press Start and the motor runs. Release Start and it keeps running, because `Run`
feeds itself. Press EStop and it drops out. That is a seal-in latch, and
[lesson 2](lessons/seal-in/index.md) verifies exactly this circuit.

## Ladder diagram

LD draws the program as a relay schematic, so power flows from the left rail to the
right through contacts, and a coil at the end of the rung energizes the moment some
path through them conducts. A normally-open contact `-| |-` conducts when its variable
is true. A normally-closed contact `-|/|-` conducts when it is false.

<svg class="diagram" viewBox="0 0 620 150" role="img" aria-label="Ladder rung: Start in parallel with Run, in series with a normally closed EStop contact, driving the Run coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V132"/><path d="M592 18 V132"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H120"/><path d="M136 52 H380"/><path d="M396 52 H501"/><path d="M28 104 H120"/><path d="M136 104 H250"/><path d="M250 52 V104"/><path d="M535 52 H592"/><path d="M120 40 V64"/><path d="M136 40 V64"/><path d="M120 92 V116"/><path d="M136 92 V116"/><path d="M380 40 V64"/><path d="M396 40 V64"/><path d="M376 66 L400 38"/><path d="M508 38 Q494 52 508 66"/><path d="M528 38 Q542 52 528 66"/></g><circle cx="250" cy="52" r="3.5" fill="currentColor"/><circle cx="250" cy="104" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="128" y="32">Start</text><text x="128" y="86">Run</text><text x="388" y="32">EStop</text><text x="518" y="32">Run</text></g></svg>

The lower branch is the seal-in. Both branches feed one junction, which is a wired OR,
and the closed EStop contact sits after the junction so it breaks both paths at once.

**How it is stored.** As geometry, not text. Each contact and coil carries a position
and a list of connections, which is why two ladders that look identical can differ in
the file. The suite ships both flavors: a textual LD notation and PLCopen XML.

## Function block diagram

FBD draws the same logic as signal flow through boxes. Where LD thinks in current
paths, FBD thinks in operands and results, so it suits analog chains, filters, and PID
loops far better than a rung of contacts does.

<svg class="diagram" viewBox="0 0 620 190" role="img" aria-label="Function block diagram: Start and Run into an OR block, EStop into a NOT block, both into an AND block driving Run"><g stroke="currentColor" fill="none" stroke-width="1.6"><rect x="150" y="36" width="96" height="64" rx="3"/><rect x="150" y="128" width="96" height="44" rx="3"/><rect x="340" y="76" width="96" height="80" rx="3"/><path d="M74 56 H150"/><path d="M74 84 H150"/><path d="M74 150 H150"/><path d="M246 68 H293 V96 H340"/><path d="M246 150 H293 V136 H340"/><path d="M436 116 H520"/></g><g fill="currentColor" font-size="13"><text x="198" y="73" text-anchor="middle">OR</text><text x="198" y="155" text-anchor="middle">NOT</text><text x="388" y="121" text-anchor="middle">AND</text><text x="66" y="61" text-anchor="end">Start</text><text x="66" y="89" text-anchor="end">Run</text><text x="66" y="155" text-anchor="end">EStop</text><text x="530" y="121">Run</text></g></svg>

**How it is stored.** Geometry again: blocks with positions, pins, and connections
between them. LD and FBD are close enough underneath that most tools translate one
into the other, and PLCopen XML gives them sibling elements in the same schema.

## Structured text

ST is a Pascal-descended textual language, and it is the one that scales. Loops,
arrays, functions, and structured types all belong here; anything you would find
painful to draw belongs here too.

```pascal
IF EStop THEN
    Run := FALSE;
ELSE
    Run := Start OR Run;
END_IF;
```

Written as one expression, it is the line at the top of this page:

```pascal
Run := (Start OR Run) AND NOT EStop;
```

**How it is stored.** Plain text, so it diffs, greps, and reviews like ordinary source
code. That property is worth more than it sounds when a change has to be audited.

## Sequential function chart

SFC is the odd one, and the standard treats it that way: it structures a program
rather than replacing the language inside it. You draw steps, the transitions between
them, and the condition that fires each transition. The actions inside a step are
written in one of the other languages.

A latch is the wrong example for SFC, because a latch is not a sequence. A tank cycle
is the right one:

<svg class="diagram" viewBox="0 0 460 400" role="img" aria-label="Sequential function chart: Idle step, transition on Start, Filling step, transition on level reached, Draining step, transition on empty, looping back to Idle"><g stroke="currentColor" fill="none" stroke-width="1.6"><rect x="130" y="30" width="120" height="44" rx="2"/><rect x="134" y="34" width="112" height="36" rx="2"/><rect x="130" y="146" width="120" height="44" rx="2"/><rect x="130" y="262" width="120" height="44" rx="2"/><path d="M190 74 V146"/><path d="M190 190 V262"/><path d="M190 306 V360 H60 V20 H190 V30"/><path d="M170 110 H210"/><path d="M170 226 H210"/><path d="M170 336 H210"/></g><path d="M184 22 L190 32 L196 22 Z" fill="currentColor"/><g fill="currentColor" font-size="13"><text x="190" y="57" text-anchor="middle">Idle</text><text x="190" y="173" text-anchor="middle">Filling</text><text x="190" y="289" text-anchor="middle">Draining</text><text x="222" y="115">Start AND NOT EStop</text><text x="222" y="231">Level &gt;= Setpoint</text><text x="222" y="341">Level &lt;= 0</text></g></svg>

The double border on Idle marks the initial step. Each short horizontal bar is a
transition, and the text beside it is the condition that has to hold for the chart to
move on. Control leaves Draining and returns to Idle, which is the cycle.

**How it is stored.** Graphically in most tools, though the standard also defines
textual equivalents for the same elements.

## Instruction list

IL is an accumulator machine written as assembly, one instruction to a line, each of
them operating on a single implicit result register, and it reads the way it does
because it was written to be typed on a handheld programmer with a two-line display.
Nobody chose this for elegance.

```
      LD    Start
      OR    Run
      ANDN  EStop
      ST    Run
```

Load Start, OR in Run, AND with the negation of EStop, store the result to Run. That
is the same seal-in, four instructions deep.

**How it is stored.** Plain text. Do not write new IL: edition 4.0 removed it, and the
committee's stated reason was that an assembler-like language is not up to date in a
modern development environment. Read it, because plants that were commissioned in 1998
are still running it.

## The interchange format

Vendor project files are proprietary and mutually unreadable, which is why PLCopen
TC6 defined an XML interchange format. A program becomes a `<pou>` holding an
`<interface>` that declares the variables and a `<body>` holding exactly one language
element: `<LD>`, `<FBD>`, `<ST>`, `<SFC>`, or `<IL>`.

For a graphical body that means every element carries an identity and its wiring:

```xml
<contact localId="10" negated="false" storage="none" edge="none">
  <position x="20" y="10"/>
  <connectionPointIn><connection refLocalId="0"/></connectionPointIn>
  <variable>Start</variable>
</contact>
```

Two `<connection>` elements inside one `<connectionPointIn>` is how a wired OR is
written, and that is the seal-in junction drawn above.

Textual bodies are simpler: the source sits inside the element as text.

Every graphical program in this suite is PLCopen XML. The files carry a `.ld`
extension while their content is XML, because the verifier keys its front end off the
extension. [Lesson 1](lessons/interlock/index.md) has the full file to read.

## What this suite covers today

{{coverage: benchmarks}}

Those counts are generated from the catalog when the site builds, so they cannot drift
from it. FBD and SFC entered the suite on 2026-08-26 for language coverage: two tasks
each, a clean and a seeded variant apiece, with ground truth established by
construction rather than by a tool run, which is why they carry
`validation_status: candidate`. IL has none and none is planned, since edition 4.0
removed it. The [benchmarks catalog](benchmarks/index.md) lists every task.
