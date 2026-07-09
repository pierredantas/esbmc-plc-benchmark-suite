#!/usr/bin/env bash
# =============================================================================
# run_all.sh — run every P6 benchmark variant through ESBMC-PLC+ and check the
# result against its expected_verdict. Reproduces the suite's baseline column.
#
#   ESBMC=/path/to/esbmc/build/src/esbmc/esbmc ./run_all.sh
#   TIMEOUT=300 ESBMC=... ./run_all.sh                 # per-variant timeout (s)
#   DRY_RUN=1 ./run_all.sh                             # print commands, run nothing
#   ./run_all.sh benchmarks/motor_control/motor_interlock   # a subset (dirs)
#
# Mode per expected verdict (matches the ESBMC-PLC-Sec run scripts):
#   expected SAFE  (true)  -> --k-induction         (prove the property)
#   expected VIOL  (false) -> --incremental-bmc     (find the counterexample)
# The --ld-scan-watchdog flags make non-terminating-loop LLBs (the `termination`
# property) observable as a VIOLATION.
#
# NOTE: this passes each benchmark's props.yaml straight to `--ld-props`. The suite
# schema evolved from the ESBMC-PLC props format, but if your build rejects a kind
# (e.g. `termination`, which is enforced by the scan-watchdog rather than a property
# assertion), the run still exercises termination via the watchdog — check one such
# case first and add a props translation step here if needed.
# =============================================================================
set -uo pipefail

SUITE_DIR="$(cd "$(dirname "$0")" && pwd)"
ESBMC="${ESBMC:-esbmc}"
TIMEOUT="${TIMEOUT:-120}"
EXTRA_FLAGS="${EXTRA_FLAGS:---ld-scan-watchdog --ld-scan-budget 8}"
UNWIND="${UNWIND:-12}"
DRY_RUN="${DRY_RUN:-0}"
ROOTS=("$@"); [[ ${#ROOTS[@]} -eq 0 ]] && ROOTS=("$SUITE_DIR/benchmarks")

if [[ "$DRY_RUN" != "1" ]]; then
  if ! "$ESBMC" --version >/dev/null 2>&1; then
    echo "ERROR: ESBMC not runnable ('$ESBMC'). Set ESBMC=/path/to/esbmc-plc+ binary." >&2
    exit 1
  fi
  echo "ESBMC: $("$ESBMC" --version 2>&1 | head -1)"
  echo "timeout=${TIMEOUT}s  extra='${EXTRA_FLAGS}'"
fi

mkdir -p "$SUITE_DIR/results/logs"
TSV="$SUITE_DIR/results/summary.tsv"
printf "id\tdomain\tlanguage\tvariant\texpected\tgot\tstatus\tcpu_s\n" > "$TSV"

# Enumerate (id, domain, language, variant_abs, props_abs, expected) as TSV.
tasks=$(python3 - "${ROOTS[@]}" <<'PY'
import sys, os, glob, yaml
seen = []
for root in sys.argv[1:]:
    bps = ([os.path.join(root, "benchmark.yml")] if os.path.isfile(os.path.join(root, "benchmark.yml"))
           else glob.glob(os.path.join(root, "**", "benchmark.yml"), recursive=True))
    for bp in sorted(bps):
        b = yaml.safe_load(open(bp)); d = os.path.dirname(bp)
        props = os.path.normpath(os.path.join(d, b.get("properties_file", "props.yaml")))
        for v in b["variants"]:
            print("\t".join([b["id"], b["domain"], b["language"],
                             os.path.join(d, v["file"]), props,
                             "true" if v["expected_verdict"] else "false"]))
PY
)

total=0; correct=0; wrong=0; unknown=0
while IFS=$'\t' read -r bid domain lang vfile props exp; do
  [[ -z "${bid:-}" ]] && continue
  total=$((total+1))
  if [[ "$exp" == "true" ]]; then mode=(--k-induction); else mode=(--incremental-bmc --unwind "$UNWIND"); fi
  cmd=("$ESBMC" "$vfile" --ld-props "$props" "${mode[@]}" $EXTRA_FLAGS --timeout "${TIMEOUT}s")

  if [[ "$DRY_RUN" == "1" ]]; then printf '%q ' "${cmd[@]}"; echo; continue; fi

  start=$(date +%s)
  out=$("${cmd[@]}" 2>&1); rc=$?
  cpu=$(( $(date +%s) - start ))
  echo "$out" > "$SUITE_DIR/results/logs/${bid}__$(basename "$vfile").log"

  if   grep -qiE "verification successful"          <<<"$out"; then got="true"
  elif grep -qiE "verification failed|counterexample" <<<"$out"; then got="false"
  else got="unknown"; fi

  if   [[ "$got" == "unknown" ]]; then status="UNKNOWN"; unknown=$((unknown+1))
  elif [[ "$got" == "$exp"     ]]; then status="OK";      correct=$((correct+1))
  else                                  status="WRONG";   wrong=$((wrong+1)); fi

  printf "%-7s %-24s %-16s exp=%-5s got=%-7s %ss\n" "$status" "$bid" "$(basename "$vfile")" "$exp" "$got" "$cpu"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$bid" "$domain" "$lang" "$(basename "$vfile")" "$exp" "$got" "$status" "$cpu" >> "$TSV"
done <<< "$tasks"

[[ "$DRY_RUN" == "1" ]] && exit 0
echo ""
echo "==== SUMMARY: ${total} variants | ${correct} correct | ${wrong} WRONG | ${unknown} unknown ===="
echo "per-variant results: $TSV   (logs in results/logs/)"
if [[ $wrong -eq 0 && $unknown -eq 0 ]]; then
  echo "All verdicts match expected ground truth."
else
  echo "Investigate:  awk -F'\\t' '\$7==\"WRONG\"||\$7==\"UNKNOWN\"' \"$TSV\""
fi
exit $(( wrong > 0 ? 1 : 0 ))
