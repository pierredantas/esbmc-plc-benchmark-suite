# Blind review of the semantics record by a language model (R1.1)

Reviewer 1 and the letter note that no second person has reviewed `semantics.yml`. This packet lets a language model
act as that second reader. It is a review by a model, not by a person, and the paper and letter must say so.

## What the reviewer gets, and what it does not get

- `PROMPT.md`: the definitions of the six fields, the decision rules, and the answer format.
- `programs/batch_01.md` to `batch_15.md`: for each of the 117 core benchmarks, the raw text of its first variant, its
  language, and its properties.
- `answers_template.csv`: one row per benchmark, to be filled in.
- It does **not** get `semantics.yml`, the descriptors' tags, expected verdicts, or any of our scripts. It decides from
  the program text and the definitions alone.

## How to run it

1. Give the reviewer `PROMPT.md` and one batch at a time (about 8 benchmarks, 35 to 40 KB), or all batches in sequence
   in one conversation. Ask it to return the CSV rows for that batch.
2. Concatenate the rows into `answers.csv` (keep the header from `answers_template.csv`).
3. Compare: `python3 compare_ai_review.py answers.csv out/review`. It prints agreement per field and writes
   `out/review_disagreements.csv`.
4. Adjudicate every disagreement by reading the program: mark it `reviewer right`, `record right`, or
   `both defensible` in the last two columns. Correct `semantics.yml` where the reviewer is right.

## Which model

- Prefer a model family that did not help write the record. Claude helped draft the manuscript, the scripts, and
  parts of this record, so a Claude review is not independent of our AI use. A different family (for example Gemini
  or GPT) gives a better second reading; DeepSeek and Gemini are already named in the AI-use statement for another
  purpose.
- Record the model name, version, date, and settings of the run, and keep the raw answers.
- Chosen reviewer: `gemini-3.8-flash` (name as given by the user; record the exact string shown by the interface, the date, and the settings). A Flash-tier model is a smaller, faster model, so treat its answers on graphical XML with extra care, run the second pass in reverse batch order, and adjudicate every disagreement by reading the program.
- Run it twice with different batch orders if you can. Disagreements that appear in only one run measure the
  reviewer's own noise.

## What to say in the paper and the letter (fill in after the run)

- In the letter (R1.1): "The semantics record was read blind by <model, version> on <date>, from the program text and
  the definitions of Section 4.5 alone. It agreed with the record on X of 117 benchmarks in every field; we
  adjudicated the Y differences and corrected Z entries. This is a review by a language model, not by a second
  person."
- In the manuscript (Section 4.5): replace "No second person has reviewed the entries" with the same statement,
  keeping the limit visible.
- In the AI-use statement (`submission-system-statements.txt` and the manuscript): add that a language model was used
  as a blind reviewer of the semantics record, with the model name and date.

## Limits to keep in view

- The reviewer reads the same raw text we wrote and applies definitions that we wrote, so it tests our record against
  our definitions, not against the standard.
- Language models are less reliable at following graphical XML wiring. Treat `low` confidence answers on graphical
  programs as unanswered and check them by hand.
- Agreement does not prove the record is right. It shows that a second reader, given the same definitions, reaches
  the same answers.
