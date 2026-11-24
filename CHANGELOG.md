# Changelog

## Unreleased

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
