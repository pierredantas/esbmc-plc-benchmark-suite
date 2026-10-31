# Model review of the 12 standard-anchored programs (R2.4)

Twelve benchmarks cite a clause of a machine-safety standard (ISO 13850, EN 298, ISO 14119, ISO 13851, EN 13241) or
an ISA-88 design. Nobody with domain knowledge has checked them against the standards. This packet has a language
model read them and say (1) whether each program implements the requirement as its author states it, and (2)
whether each fault that no property catches matters. It is a review by a model, not by a standards expert, and the
paper and letter must say so.

## Contents

- `PROMPT.md`: the task, the two answer files, the allowed values, and the rules.
- `programs/batch_1.md`, `batch_2.md`: six programs each, with the clause as the author states it, the safety
  intent, the program, its property and discriminator, and the 74 surviving mutants (each names the coils its
  contact feeds, or the source line it changes).
- `BATCH_MESSAGE.txt`: the message to send with each batch.
- `answers_programs_template.csv`, `answers_survivors_template.csv`: the row lists the replies must cover.
- `merge_standards_answers.py`: merges and validates the replies and summarizes them.

## How to run it (Google AI Studio, gemini-3.8-flash, as for the semantics record)

1. System instructions: paste `PROMPT.md`. Thinking level: Medium (High if offered). Search grounding: **off**. Code
   execution, function calling, URL context, structured outputs: off. Note the exact model string and the date.
2. New chat. Attach `programs/batch_1.md`, paste `BATCH_MESSAGE.txt`, and copy the reply to `replies/batch_1.txt`.
3. New chat. The same with `batch_2.md` into `replies/batch_2.txt`.
4. `python3 merge_standards_answers.py replies out/review` writes `out/review_programs.csv` and
   `out/review_survivors.csv`, checks values and coverage, and lists the mutants judged `required_by_clause`.
5. Optional but recommended: repeat in `replies2/` with the batches in the other order, and compare the two runs.

## What happens next

- Every mutant judged `required_by_clause` is a candidate gap in our properties. I read each one against the
  program and decide whether the property should be strengthened or the judgement rejected.
- A program judged `partly` or `no` is read against the clause as stated in the descriptor. If the reviewer is right,
  the descriptor's claim ("authored from ...") is corrected and the paper's counts follow.

## What must be said, and what the review cannot do

- The reviewer does not have the text of the standards; it relies on its memory of them and on the clause as the
  author states it. Treat its statements about what a standard requires as leads to check, not as facts. The packet
  asks it to mark such statements `(memory)`.
- It tests consistency between a program and a requirement stated by us, not conformity to the standard.
- Agreement is not proof; disagreement is not an error until the program has been read.
- The AI-use statement (manuscript and `submission-system-statements.txt`) must be extended to name this review, with
  the model, version, date, and settings.
