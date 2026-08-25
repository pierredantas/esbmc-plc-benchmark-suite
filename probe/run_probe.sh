#!/usr/bin/env bash
# =============================================================================
# run_probe.sh — frontend probe pack for ESBMC-PLC.
#
#   ESBMC=/path/to/esbmc ./run_probe.sh
#   TIMEOUT=120 ESBMC=... ./run_probe.sh
#
# Each probe is a SAFE/VIOLATION pair over the SAME logic and the SAME property.
# The bomb twin is the soundness gate: a frontend that silently ignores a body it
# does not understand finds nothing to check and reports VERIFICATION SUCCESSFUL.
# A probe whose bomb returns SUCCESSFUL is therefore VOID, not supported.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ESBMC="${ESBMC:-esbmc}"
TIMEOUT="${TIMEOUT:-120}"
WD=(--ld-scan-watchdog --ld-scan-budget 8)
LOGS="$HERE/logs"; mkdir -p "$LOGS"

if ! "$ESBMC" --version >/dev/null 2>&1; then
  echo "ERROR: ESBMC not runnable ('$ESBMC'). Set ESBMC=/path/to/esbmc-plc binary." >&2
  exit 1
fi
echo "ESBMC:   $("$ESBMC" --version 2>&1 | head -1)"
echo "timeout: ${TIMEOUT}s"
echo

# run <xml> <props> <expect:true|false> <tag>  -> echoes true|false|unknown|error
run () {
  local xml="$1" props="$2" expect="$3" tag="$4"
  local ld="$LOGS/$tag.ld" log="$LOGS/$tag.log"
  cp "$xml" "$ld"
  local mode=(--k-induction)
  [[ "$expect" == "false" ]] && mode=(--incremental-bmc --unwind 20)
  # macOS has no GNU `timeout`; ESBMC takes --timeout itself (as run_v84.py does).
  "$ESBMC" "$ld" --ld-props "$props" "${mode[@]}" "${WD[@]}" --timeout "${TIMEOUT}s" \
      >"$log" 2>&1
  if   grep -qi "verification successful" "$log"; then echo true
  elif grep -qi "verification failed"     "$log"; then echo false
  elif grep -qiE "PARSING ERROR|conversion error|unsupported|not supported|No document element|failed to figure out" "$log"; then echo error
  else echo unknown; fi
}

pair () {  # pair <name> <clean.xml> <bomb.xml> <props> <question>
  local name="$1" c="$2" b="$3" p="$4" q="$5"
  local gc gb verdict note
  gc=$(run "$c" "$p" true  "${name}_clean")
  gb=$(run "$b" "$p" false "${name}_bomb")
  if   [[ "$gc" == true  && "$gb" == false ]]; then verdict="SUPPORTED"; note="clean proved, bomb refuted"
  elif [[ "$gb" == true  ]];                     then verdict="VOID";    note="bomb returned SUCCESSFUL — body likely ignored"
  elif [[ "$gc" == error || "$gb" == error ]];   then verdict="REJECTED"; note="$(grep -im1 -E 'parse|conversion|unsupported|error' "$LOGS/${name}_clean.log" | cut -c1-64)"
  else verdict="INCONCLUSIVE"; note="clean=$gc bomb=$gb"; fi
  printf "%-14s %-12s %-6s %-6s %s\n" "$name" "$verdict" "$gc" "$gb" "$note"
  printf "%s\t%s\t%s\t%s\t%s\n" "$name" "$verdict" "$gc" "$gb" "$q" >> "$HERE/probe_results.tsv"
}

printf "name\tverdict\tclean\tbomb\tquestion\n" > "$HERE/probe_results.tsv"
printf "%-14s %-12s %-6s %-6s %s\n" PROBE VERDICT CLEAN BOMB NOTE
printf '%.0s-' {1..78}; echo

pair p0_sanity  p0_sanity/clean.xml      p0_sanity/bomb.xml      props.yaml \
     "Does this build reproduce the verdicts already in results/?"
pair p1a_st_xhtml p1_st/p1a_xhtml_clean.xml p1_st/p1a_xhtml_bomb.xml props.yaml \
     "Does ESBMC accept an ST body (TC6 xhtml wrapper) inside PLCopen XML?"
pair p1b_st_bare  p1_st/p1b_bare_clean.xml  p1_st/p1b_bare_bomb.xml  props.yaml \
     "Same, with bare text — disambiguates wrong-wrapper from no-ST-support."
pair p2_fbd     p2_fbd/p2_fbd_clean.xml  p2_fbd/p2_fbd_bomb.xml  props.yaml \
     "Does the FBD slice get an ESBMC baseline column?"
pair p3_sfc     p3_sfc/p3_sfc_clean.xml  p3_sfc/p3_sfc_bomb.xml  props.yaml \
     "Does the SFC slice get an ESBMC baseline column?"

echo
echo "P4 — property forms, all on the KNOWN-GOOD LD pair (frontend held constant):"
printf '%.0s-' {1..78}; echo
for y in p4_props/p4*.yaml; do
  n="p4_$(basename "$y" .yaml | cut -d_ -f2-)"
  pair "$n" p4_props/clean.xml p4_props/bomb.xml "$y" \
       "Does --ld-props accept $(basename "$y")?"
done

echo
echo "results: $HERE/probe_results.tsv    logs: $LOGS/"
