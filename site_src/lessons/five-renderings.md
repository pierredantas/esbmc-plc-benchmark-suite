Part 1 stayed inside ladder logic. Ladder is one of five notations the standard defines,
and a benchmark suite meant for validating tools has to say something about the other
four. This lesson takes one circuit you already know and writes it five ways.

The circuit is the seal-in latch from [lesson 1.4](../seal-in/index.md), with the names
the suite's own benchmark uses:

```
Run := (Start OR Run) AND NOT Stop
```

Press Start, release it, the motor keeps running until Stop. One line of logic, five
notations, and the differences between them are not cosmetic.

{{files: benchmarks/motor_control/ld_seal_in/seal_in.ld | benchmarks/motor_control/g_seal_in/program.xml | benchmarks/motor_control/st_seal_in/seal_in.st | benchmarks/motor_control/fbd_seal_in/program.xml | benchmarks/motor_control/il_seal_in/seal_in.il}}

## Ladder diagram, drawn

<svg class="diagram" viewBox="0 0 620 140" role="img" aria-label="Ladder rung: Start in parallel with Run, in series with a normally closed Stop contact, driving the Run coil"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V122"/><path d="M592 18 V122"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 48 H130"/><path d="M146 48 H300"/><path d="M316 48 H501"/><path d="M28 96 H130"/><path d="M146 96 H240"/><path d="M240 48 V96"/><path d="M535 48 H592"/><path d="M130 36 V60"/><path d="M146 36 V60"/><path d="M130 84 V108"/><path d="M146 84 V108"/><path d="M300 36 V60"/><path d="M316 36 V60"/><path d="M296 62 L320 34"/><path d="M508 34 Q494 48 508 62"/><path d="M528 34 Q542 48 528 62"/></g><circle cx="240" cy="48" r="3.5" fill="currentColor"/><circle cx="240" cy="96" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="138" y="28">Start</text><text x="138" y="76">Run</text><text x="308" y="28">Stop</text><text x="518" y="28">Run</text></g></svg>

This is what an electrician sees. Power leaves the left rail, finds a path through
`Start` or through the latched `Run` contact, is broken by the normally closed `Stop`,
and energizes the coil. Nothing is written down; the meaning is in the drawing.

## Ladder diagram, as text

{{show: benchmarks/motor_control/ld_seal_in/seal_in.ld}}

The same rung in the K-LD textual notation. `XIC` is a normally open contact,
*examine if closed*; `XIO` is normally closed; `OTE` is an output coil. Series becomes
`*`, parallel becomes `+`. It reads like Boolean algebra because that is what a rung is.

Compact, diffable and reviewable, and also not what any vendor tool on the market
actually exports, which is exactly why the suite carries both spellings as a syntax pair
rather than picking one and calling the other a detail.

## Ladder diagram, as PLCopen XML

{{code: benchmarks/motor_control/g_seal_in/program.xml}}

The same rung again, and now it is a graph. Every element carries a `localId`, and every
element names the elements it draws power from:

```xml
<coil localId="6" negated="false" storage="none">
  <connectionPointIn>
    <connection refLocalId="4" />
    <connection refLocalId="5" />
  </connectionPointIn>
  <variable>Run</variable>
</coil>
```

Two connections into one input is the parallel junction. There is no element for it and
no line in the file that says "OR". A tool has to work that out, which is the whole
subject of [lesson 1.2](../series-parallel/index.md).

## Structured text

{{show: benchmarks/motor_control/st_seal_in/seal_in.st}}

The shortest of the five, and the only one where the latch is visible as a latch, since
`Run` appears on both sides of the assignment and anyone who has written code in any
language reads that correctly on first sight. That matters when the reviewer is not a
control engineer.

## Function block diagram

{{code: benchmarks/motor_control/fbd_seal_in/program.xml}}

Three blocks and four wires: `Start` and `Run` into an OR, `Stop` through a NOT, both
into an AND, the result back to `Run`. FBD makes the data flow explicit where ladder
makes the current path explicit. On a Boolean latch the two say the same thing; on an
analog chain with filters and a PID, FBD is the readable one and ladder is not.

## Instruction list

{{show: benchmarks/motor_control/il_seal_in/seal_in.il}}

An accumulator machine. Load `Start`, OR in `Run`, AND with the negation of `Stop`, store
the result. Four instructions, each acting on one implicit register, in the order they
are written.

IL was deprecated in edition 3.0 of the standard in 2013 and removed in edition 4.0 in
2025. It is here because deployed plants still run it and because a tool that claims IEC
coverage is usually asked to parse it.

## What sequential function chart would say

Nothing useful, and that is worth stating. SFC structures a program into steps and the
transitions between them. A latch is not a sequence: it is one Boolean relation that
holds every scan. Writing it as a two-step chart would be a translation exercise rather
than a design.

Where SFC earns its place is a cycle with phases, which is what
`sfc_batch_fill_drain` in the catalog does: Idle, Filling, Reacting, Draining, and back.
Use the notation the process has, not the one the suite wants to tick off.

## Which of these can ESBMC read?

One.

{{record: seal_in_graphical}}

{{record: seal_in_fbd}}

Both report SUCCESSFUL. Only the first one verified a seal-in; watch the ingestion gate
column on the second. That column is the subject of the next lesson, which measures the
coverage of all five notations rather than asserting it.

The textual ladder, the structured text and the instruction list are not shown above with
verdicts at all, because ESBMC's front end XML-parses whatever file it is given and none
of those three is XML. They are in the download table all the same. A benchmark suite is
not only for the tool that happens to be at hand.
