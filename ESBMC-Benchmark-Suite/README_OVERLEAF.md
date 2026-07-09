# EMSE submission — Overleaf setup

Target journal: **Empirical Software Engineering** (Springer, journal 10664).
Class: **svjour3** (the class EMSE's FAQ points to). Springer does **not** distribute
svjour3/spbasic via CTAN, so you get them from Overleaf's template — one click.

## Files in this folder
- `main.tex`   — svjour3 preamble, title, authors, abstract, keywords, declarations, bibliography.
- `body.tex`   — the 8 sections in EMSE order (Intro, Related Work, Design Principles,
                 The Benchmark Suite, Ground-Truth Methodology, Evaluation, Threats, Conclusion).
- `refs.bib`   — references (best-effort; entries marked `% VERIFY` need confirming — most
                 already exist in your prior papers' .bib files).

## Steps
1. In Overleaf: **New Project → Templates**, search **"Springer SVJour3"** (or open the
   template linked from the EMSE FAQ, https://emsejournal.github.io/faq.html). This creates a
   project that already contains `svjour3.cls` and `spbasic.bst`.
2. In that project, **replace `main.tex`** with this folder's `main.tex`, and **upload**
   `body.tex` and `refs.bib`.
3. Set the compiler to **pdfLaTeX** (Menu → Compiler). Recompile.
4. Bibliography: `\bibliographystyle{spbasic}` + `\bibliography{refs}` are already in `main.tex`.

## Before submitting — checklist
- [x] Author names, emails, ORCIDs, affiliations — filled from the group metadata
      (Dantas, Cordeiro, Junior). **Confirm Waldir Junior is a P6 co-author** (carried over from
      the K-LD paper) or remove him from `main.tex`.
- [ ] Fill the remaining `% TODO` items in `main.tex`: acknowledgements, Zenodo DOI
      (Data availability), competing-interests statement.
- [ ] Verify every `% VERIFY` entry in `refs.bib` (authors, venue, year, pages, DOI) — pull the
      authoritative versions from your ESBMC-PLC / Arduino / PLC-Sec `.bib` files.
- [ ] Reposition the `Evaluation` section if you prefer it after `Threats` — currently it is
      before Threats (standard empirical-paper order); both are fine.
- [ ] EMSE wants **all editable source files** at submission (main.tex, body.tex, refs.bib, and
      any figures) — upload the full set, not just the PDF.
- [ ] Optional: add a Figure 1 architecture/pipeline diagram; the paper is currently table-only.
- [ ] Consider EMSE's **open-science** expectations: link the GitHub artifact
      (github.com/pierredantas/esbmc-plc-benchmark-suite — make public at submission) and a
      Zenodo DOI.

## Notes on content status
The draft is complete and internally consistent; every number is verified against the built
suite and the ESBMC-PLC v8.4 evaluation (43/45 graphical variants, 0 wrong). Plain terms are
used instead of `\gls{}` macros. The Related-Work `\cite`s resolve against `refs.bib`.
