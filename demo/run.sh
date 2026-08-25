#!/usr/bin/env bash
# Minimal end-to-end example: one ladder file, one property, one verification.
#   ESBMC=/path/to/esbmc ./run.sh
set -uo pipefail
ESBMC="${ESBMC:-$HOME/esbmc-toolchain/src/esbmc-src/build/src/esbmc/esbmc}"
cd "$(dirname "$0")"

echo "== 1. correct interlock, expect SAFE (prove it) =="
echo "\$ esbmc interlock.ld --ld-props props.yaml --k-induction"
"$ESBMC" interlock.ld --ld-props props.yaml --k-induction 2>&1 | grep -E "^VERIFICATION|Solution found"

echo
echo "== 2. interlock removed, expect VIOLATION (find the counterexample) =="
echo "\$ esbmc interlock_bug.ld --ld-props props.yaml --incremental-bmc --unwind 20"
"$ESBMC" interlock_bug.ld --ld-props props.yaml --incremental-bmc --unwind 20 2>&1 \
  | sed -n '/^State 1/,$p' | grep -E "= 1|Violated|P1|!\(|^VERIFICATION|Bug found"

exit 0
