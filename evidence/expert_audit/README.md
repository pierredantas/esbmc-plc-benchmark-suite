# Expert audit package

No reviewer outside the author group has audited the expected verdicts. This package prepares that audit for the cases where
the verdict depends on the execution model: timers, counters, latches, and integer overflow.

## Sample

`build_sample.py` selects 30 of the 117 benchmarks (47 variants) with a fixed seed (20261123):

| Stratum | Benchmarks |
|---|---|
| Timer or counter model | 12 |
| Latch or seal-in | 8 |
| Integer overflow (assumption H1) | 6 |
| Control: validated benchmarks with no such dependence | 4 |

The control stratum lets the reviewer's disagreement rate on the dependent cases be read against a baseline.

## What the reviewer does

For each variant in `review_sheet.csv`, using `review_pack.md`:

1. Read the program and the property.
2. Decide, from the program and the stated assumptions alone, whether the expected verdict is correct. Enter `agree`, `disagree`, or `unsure`.
3. Decide whether the stated assumptions (scan order, retained state, timer or counter model, overflow) are the ones the verdict needs.
   Enter `yes` or `no`.
4. Write a comment for every `disagree`, `unsure`, or `no`.

The reviewer should not run the verifiers first and should not be an author of the suite. The sheet gives each tool's answer in
`sample.csv`; open it only after recording the verdicts.

## Reporting

The outcome is reported as counts per stratum, with every disagreement listed and resolved in the repository history.
Disagreements are not filtered: a label the reviewer rejects is a candidate for correction, and the paper reports the correction.

## Model review

No human expert had answered by November 26, 2026, so Grok 4.5 (xAI) reviewed the sample in two runs. The first run gave 32 agree, 15 unsure, and
0 disagree; the second, with the location of every source given, gave 46 agree, 1 unsure, and 0 disagree. It is one model and not an
independent human audit. `GROK_REVIEW_NOTES.md` states the counts and the limits.

## Files

- `sample.csv`: the sample with provenance, assumptions, and tool answers.
- `review_sheet.csv`: one row per variant with blank reviewer columns.
- `review_pack.md`: programs and properties for reading.
- `build_sample.py`: rebuilds the three files from the descriptors.
- `grok_run1_*review_sheet.csv`, `grok_run2_review_sheet.csv`, `grok_run2_prompt.md`, `GROK_REVIEW_NOTES.md`: the model review.
