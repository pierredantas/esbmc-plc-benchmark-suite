# Independent review of a semantics record for PLC verification benchmarks

You are reviewing, blind, the *semantic assumptions* of 117 small PLC programs (IEC 61131-3). You see only each
program's text, its language, and the properties checked on it. You do not see the authors' record. For each program
you decide the fields below from the program alone, then give a confidence and a one-sentence reason. Do not guess
what the authors intended; decide from the text and the definitions.

## Background

A verification verdict on a PLC program is valid only under an execution model. A PLC runs the program in scans: it
reads inputs, runs the program once, writes outputs, and repeats. The record states, per program, what the verdict
assumes.

## Fields to decide (one answer per program)

1. **scan_order** (choose one)
   - `rung` : a ladder (LD) program, textual or graphical. Rungs run top to bottom within one scan. A rung that reads
     a coil written by an *earlier* rung sees the new value; a rung that reads a coil written by a *later* rung (or
     itself) sees the previous scan's value.
   - `statement` : a structured text (ST) or instruction list (IL) program. Statements run in written order.
   - `tool-defined` : a function block diagram (FBD) or sequential function chart (SFC) program, whose execution order
     the language leaves to the tool.
2. **retained_state** (`yes` / `no`): does any value survive from one scan to the next and influence the outputs? Count
   a coil or variable that is read before it is written in a scan, a self-holding (seal-in) rung, a set/reset coil, an
   edge detector (rising or falling), a timer, a counter, or a variable exchanged between program units. Answer `no`
   for a program whose outputs depend only on the inputs of the current scan.
3. **timers_or_counters** (`yes` / `no`): does the program use a timer (TON, TOF, TP) or a counter (CTU, CTD, CTUD)?
4. **overflow_possible** (`yes` / `no`): does the program do integer arithmetic (addition, subtraction, multiplication,
   increment, counter accumulation) on a bounded integer type such that the result could exceed the type's range for
   some input? Comparisons alone do not count.
5. **setreset_coils** (`yes` / `no`): does the program use set (latch) and reset (unlatch) coils or `S`/`R` statements?
6. **verdict_scope** (choose one)
   - `holds-under-stated-order` : the property's verdict would be the same under any reasonable timing model and
     overflow behavior; only the scan order matters.
   - `semantics-dependent` : the verdict could change under another timing model (timers or counters), under integer
     overflow, or under set/reset priority.

## Answer format

Write one CSV row per benchmark into `answers_template.csv` (keep the header and the first two columns):
`benchmark, language, scan_order, retained_state, timers_or_counters, overflow_possible, setreset_coils,
verdict_scope, confidence, reasoning` where `confidence` is `high`, `medium`, or `low` and `reasoning` is one
sentence naming the construct that decided the hardest field.

## Rules

- Decide each field from the program text and the definitions above. Do not look for or ask for the authors' record.
- Say `low` confidence when the program text is ambiguous or you could not read it (for example a graphical XML whose
  wiring you cannot follow); do not guess silently.
- Graphical programs are PLCopen XML. Follow `connection refLocalId` links to see which contacts feed which coil, and
  read coil order from the order of `coil` elements in the file.
- The properties are given only so that you can judge `verdict_scope`; do not evaluate whether they hold.
