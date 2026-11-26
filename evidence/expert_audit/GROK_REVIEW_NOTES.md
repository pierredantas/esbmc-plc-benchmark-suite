# Explanation to the reviewer: how point R4.5 was handled

Reviewer 4 asked for an independent human review of a sample of the benchmarks, especially the timer, counter, latch, and overflow cases, with the outcome and any disagreements reported. This note says what we did, what came back, and what the result does and does not show.

## What we asked for

We prepared a sample of 30 benchmarks (47 variants) in four strata: 12 timer or counter, 8 latch or seal-in, 6 integer overflow, and 4 controls with no such dependence. The package holds a protocol (`README.md`), the programs and properties (`review_pack.md`, `programs/`), and a blank sheet (`review_sheet.csv`). Reviewers record `agree`, `disagree`, or `unsure` for each variant before they run any verifier.

## Outreach to human experts

On November 24, 2026, we sent the package to three groups with the same request and the same dates:

1. The OpenPLC project (a direct email to its maintainer), because OpenPLC implements the scan-cycle execution that the benchmarks assume. We also posted a volunteer call on the OpenPLC forum.
2. PLCopen (info@plcopen.org), with a request to forward it to the IEC 61131-3 committee.
3. The Chair of Automation and Information Systems at the Technical University of Munich, with a request to forward it to a researcher.

As of November 26, 2026, none of the three had replied, and no forum volunteer had come forward. The forum call asks for an answer by December 1, 2026, so a human review may still arrive after this resubmission.

## What we did instead

We could not wait for an answer and still respond to R4.5 in this revision, so we asked a language model to act as the expert. We used Grok 4.5 (xAI) in a remote sandbox on November 26, 2026, in two runs. Each run received the package as sent to the human experts, with the same protocol, and ran no verifier. The files are in this folder: the first run with its three simulated repeat passes and reports, and the second run (`GROK_RERUN_PROMPT.md`, `review_sheet_rerun.csv`, `RERUN_SUMMARY.md`). We did not edit any of them.

## Outcome, counted from the sheets

| Run | Variants | Agree | Unsure | Disagree |
|---|---|---|---|---|
| First run (pass 1) | 47 | 32 | 15 | 0 |
| Repeat pass 2 | 47 | 32 | 15 | 0 |
| Repeat pass 3 | 47 | 34 | 13 | 0 |
| Repeat pass 4 | 47 | 32 | 15 | 0 |
| Second run | 47 | 46 | 1 | 0 |

The model disagreed with no expected verdict in any run. It judged the stated semantics (scan order, retained state, timer and counter model, overflow) to be the ones each verdict needs, for every row.

The first run marked 15 variants unsure because it reported the source as missing. The source of each is in the package (30 variants inline in `review_pack.md`, 17 as files in `programs/`). For the second run we gave the location of every source, and 14 of the 15 rows became agree. The remaining unsure row is `fbd_seal_in`. The reviewer's copy of the package lacked its file. Its sandbox appears to have flattened `programs/` into one folder, where the two files named `program.xml` (`fbd_counter_reset` and `fbd_seal_in`) collide; we infer this and did not test it. The `fbd_counter_reset` row rests on the correct file, as its comment shows.

## Limits of this evidence

- **It is one model.** The repeat passes of the first run are simulated by the same model, and the second run is the same model again. They do not add independent evidence, and we count one reviewer.
- **It is not a human expert.** The model reads the semantics that we wrote in the package. A shared misreading of the scan-cycle model would pass unnoticed, and a model can agree with a plausible label without checking it. We therefore treat the result as a screen for gross labeling errors and as a trial of the protocol, not as the audit that Reviewer 4 asked for.
- **Some second-run comments are thin.** The five large tank programs (about 500 lines each) carry comments such as "Root file present. No infinite loop." That is a shallow basis for a termination verdict.
- **The first-run summary reports contain counts that the sheets do not support.** `REVIEW_REPORT.md` and `MULTI_PASS_REVIEW_REPORT.md` state 48 variants and 16 unsure. The sheets hold 47 variants and 15 unsure (13 in pass 3, where the report says 14). The counts above come from the sheets.
- **Controls.** The 4 control benchmarks give no disagreement-rate contrast, because the model disagreed with nothing in any stratum.

## Status of R4.5

Partly addressed. A model review of the 30-benchmark sample is done in two runs and reported without filtering, and it found no labeling error. The independent human review is not done, and the manuscript says so in the abstract, in Section 7.2, in the Conclusion, and in the Use of AI tools statement. If a human expert returns a sheet, we will report each review separately, with every disagreement listed.
