#!/usr/bin/env bash
# Example 2: a seal-in latch. Running it exposes an ESBMC-PLC v8.4 defect.
set -uo pipefail
ESBMC="${ESBMC:-$HOME/esbmc-toolchain/src/esbmc-src/build/src/esbmc/esbmc}"
cd "$(dirname "$0")"

echo "== the rung ESBMC actually encoded =="
"$ESBMC" sealin.ld --goto-functions-only 2>&1 | grep -E "ASSIGN Run"

echo
echo "== discriminator: Run := A OR B, then ask whether Run implies B =="
echo "   real OR  => FAILED (A=1,B=0 gives Run=1)"
echo "   last-wins => SUCCESSFUL (Run == B)"
"$ESBMC" or_discriminator.ld --ld-props or_discriminator.props.yaml --k-induction 2>&1 | grep -E "^VERIFICATION"
exit 0
