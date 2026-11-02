# Changelog

## 1.3.3

- `validation_status`: 18 benchmarks change from `validated` to `candidate` (65 validated and 52 candidates become 47 and 70).
  The validation rule requires every variant on two ESBMC routes that share no front end, and the retained evidence files
  show both routes for 47 of the 65 benchmarks. The 18 benchmarks and the reason for each are in
  `evidence/validation_status_v1.3.3.csv`.
- Programs, properties, and expected verdicts are unchanged.
- `evidence/core_numbers.json`, `evidence/variants_302.csv`, and `evidence/structural.json` still record the v1.3.2 status of each benchmark.

## 1.3.2

- Corrects `evidence/semantics.yml` and the `g_two_hand` descriptor; adds `evidence/revision/`.
