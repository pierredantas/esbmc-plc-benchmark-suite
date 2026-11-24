# Changelog

## 1.5.0

- Adds `independent/`, a tier of three programs that someone outside the author group wrote (public GitHub projects under GPL-2.0, Apache-2.0, and MIT) with
  ten properties that we wrote for them. Each has a descriptor, the normalized program, a properties file, and `independent/results.json` lists the answers of
  ESBMC 8.4, ESBMC 8.6, the C route, and PLCverif. The tier is outside `benchmarks/` and the 117 benchmarks and 186 variants of the paper.
- The schema accepts the source origin `github-public`. `runner/validate.py` and `runner/schema_check.py` cover `independent/`, so the validator now reports 120 descriptors.
- Programs, properties, and expected verdicts of the 117 benchmarks are unchanged.

## 1.4.2

- `g_two_hand_fb`: the witness text of both variants now matches the recorded runs. ESBMC 8.4 returns SAFE on both variants and fails the
  ingestion gate on `program.xml` only; ESBMC 8.6 passes the gate and returns SAFE on both, as does the C route.
  Programs, properties, and expected verdicts are unchanged.

## 1.4.1

- Terminology: the remaining uses of "ground truth" are replaced by "expected verdict", "verdict basis", or, in the language-model
  documentation (`ml/README.md`, `ml/scripts/build_dataset.py`), "reference" for the human-written `props.yaml`. The title in
  `CITATION.cff` now matches the current manuscript. The key `ground_truth` and its replacement `verdict_basis` are documented in the 1.4.0 entry only.
- Programs, properties, and expected verdicts are unchanged.

## 1.4.0

- Schema: every `benchmark.yml` now carries a required `semantics` block (`scan_order`, `verdict_scope`, and where they apply
  `retained_state`, `timer_counter_model`, `arithmetic`). The 117 descriptors are filled from `evidence/semantics.yml`.
- Schema: the per-variant key `ground_truth` is renamed `verdict_basis`. Files that use the old key no longer validate.
- `evidence/semantics.yml` mirrors the descriptors; the descriptors are authoritative.

## 1.3.4

- `validation_status`: `g_two_hand_fb` changes from `candidate` to `validated` (47 validated and 70 candidates become 48 and 69).
  The C-route rerun of October 30, 2026 already confirmed both variants, and the earlier count did not use it. A repeat on
  November 23, 2026 with ESBMC 8.6.0 built from its tag (commit 5836d7c4) gives the same verdicts. The nine records, and the log of the tenth variant (`g_ppu_evolution_1`, where the harness generator
  stops), are in `evidence/c_route_pinned_2026-11-23/`, the change in `evidence/validation_status_v1.3.4.csv`, and the list in `evidence/validated.json`.

## 1.3.3

- `validation_status`: 18 benchmarks change from `validated` to `candidate` (65 validated and 52 candidates become 47 and 70).
  The validation rule requires every variant on two ESBMC routes that share no front end, and the retained evidence files
  show both routes for 47 of the 65 benchmarks. The 18 benchmarks and the reason for each are in
  `evidence/validation_status_v1.3.3.csv`.
- Programs, properties, and expected verdicts are unchanged.
- `evidence/core_numbers.json`, `evidence/variants_302.csv`, and `evidence/structural.json` still record the v1.3.2 status of each benchmark.

## 1.3.2

- Corrects `evidence/semantics.yml` and the `g_two_hand` descriptor; adds `evidence/revision/`.
