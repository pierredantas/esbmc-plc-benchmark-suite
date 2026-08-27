#!/bin/bash
# Six via-C records that record_all.py does not produce.
#
# record_all.py names its output <benchmark>__<variant>__viac.json. These six carry
# hand-chosen names because pages refer to them by meaning rather than by benchmark:
# four spell one circuit in four notations, and two are deliberately shallow so the
# fuse outruns the scan count. A route-wide regeneration has to run this too, or the
# six keep whatever toolchain recorded them last.
#
#   PLC_TOOLS=/path/to/tools ESBMC=/path/to/esbmc runner/record_custom_via_c.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
B="$ROOT/benchmarks"
R="$ROOT/results/records"
PY="${PYTHON:-python3}"
: "${ESBMC:?set ESBMC to the binary to record}"

rec() { "$PY" "$ROOT/runner/record_via_c.py" "$@" --tool "master=$ESBMC"; }

rec "$B/manufacturing/g_comb_and/program.xml"   "$B/manufacturing/g_comb_and/props.yaml"   true  -o "$R/comb_and_ld_viac.json"
rec "$B/manufacturing/st_comb_and/comb_and.st"  "$B/manufacturing/st_comb_and/props.yaml"  true  -o "$R/comb_and_st_viac.json"
rec "$B/manufacturing/il_comb_and/comb_and.il"  "$B/manufacturing/il_comb_and/props.yaml"  true  -o "$R/comb_and_il_viac.json"
rec "$B/manufacturing/fbd_comb_and/program.xml" "$B/manufacturing/fbd_comb_and/props.yaml" true  -o "$R/comb_and_fbd_viac.json"

# --scans 8 is the point of these two: the bomb arms later than the harness runs.
rec "$B/water_treatment/sensor_forge/bomb.st"   "$B/water_treatment/sensor_forge/props.yaml"   false --scans 8 -o "$R/sensor_forge_bomb_shallow.json"
rec "$B/water_treatment/tank_overflow/bomb.st"  "$B/water_treatment/tank_overflow/props.yaml"  false --scans 8 -o "$R/tank_overflow_bomb_shallow.json"
