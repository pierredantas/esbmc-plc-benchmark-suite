# Review of 12 PLC programs against the safety standards they cite

You are reviewing 12 small PLC programs (IEC 61131-3) that cite a clause of a machine-safety standard (ISO 13850,
EN 298, ISO 14119, ISO 13851, EN 13241) or an ISA-88 design. You are not asked to certify anything. You are asked
for a careful reading, in two parts, with a clear statement of what you know and what you are unsure of.

## What you are given for each program

- the clause as the program's author states it, and the safety intent;
- the program (source text, and for graphical programs also its coils as Boolean equations, read mechanically);
- one property that a model checker proved on the program, and sometimes a *discriminator*: a second property that
  is not a requirement but separates a compliant program from a non-compliant one;
- a list of *mutants that no property kills*: each is the program with one small fault (a contact negated, a set or
  reset coil swapped, or one AND, OR, NOT, TRUE, or FALSE changed). The properties do not notice these faults.

You do not have the text of the standards. Use only what you know of them and what the packet states. When you rely
on your memory of a standard, say so and give a confidence; do not invent clause numbers.

## Part 1: one row per program (answers_programs.csv)

Columns: `benchmark, language, implements_cited_requirement, requirements_considered, requirements_not_covered,
confidence, reasoning`

- `implements_cited_requirement`: `yes`, `partly`, or `no`. Does the program implement the requirement as the
  author states it (the "clause cited" and "safety intent" lines)? Decide from the program's logic.
- `requirements_considered`: the requirements you checked, separated by semicolons, each in a few words.
- `requirements_not_covered`: well-known requirements of the cited standard that this program does not address (for
  example a reset requirement, a monitoring requirement, a timing limit), separated by semicolons; `none` if you know
  of none. Mark each as `(memory)` when it comes from your recall of the standard and not from the packet.
- `confidence`: `high`, `medium`, or `low`. Use `low` when you are unsure what the standard requires.
- `reasoning`: one or two sentences naming the construct that decided your answer.

## Part 2: one row per surviving mutant (answers_survivors.csv)

Columns: `benchmark, mutant_id, mutant, classification, reasoning`

For each listed mutant decide whether the fault matters:

- `required_by_clause`: the fault breaks behavior that the cited clause requires, so a complete set of properties
  should have caught it;
- `harmless`: the fault leaves every safety-relevant behavior unchanged (for example a redundant contact, or a rung
  that does not affect any safety output);
- `unclear`: you cannot tell from the packet and your knowledge.

Write one sentence of `reasoning` per mutant, naming the rung or output that decides it. Copy `benchmark`,
`mutant_id`, and `mutant` exactly from the packet.

## Rules

- Judge each program on its own text. Do not assume a program is correct because it is in a benchmark suite.
- Prefer `partly` and `unclear` to a guess. A false `yes` is worse than an honest `low` confidence.
- Do not search the web or ask for external documents; answer from the packet and your knowledge.
- Keep the two CSV files separate and keep the exact column order.
