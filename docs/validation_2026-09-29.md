# Two-route validation, September 29, 2026

The two-route check of `validation_2026-09-27.md` was repeated on the build that the pinned image uses:

- **LD route**: `runner/record_all.py --route ld`, ESBMC's LD front end at pierredantas/esbmc `ws0-integration` (4a9dbe2), with the ingestion gate.
- **via-C route**: `runner/record_via_c.py`, PLCopen XML to Beremiz to MatIEC C to ESBMC's C front end; plain-text LD converted by `tools/ld_text_to_xml.py` first.

Both routes ran on this repository at 209abb9 with a 60 s timeout. `validation_2026-09-29.tsv` has one row per variant, in the format of the September 27 file.

## Result

Of 281 variants, 166 agree with their expected verdict on both routes, 82 on via-C only, and 20 on the LD route only. No expected verdict is contradicted by both routes. The 5 `counter_scalability` bombs are still deeper than the via-C scan bound, and 8 variants have no usable verdict.

Three variants differ from September 27:

- `access_door_forced_gm` clean and bomb now agree on both routes, after P1 was rewritten as a `reachable` property in #37.
- `g_tank_sub_function` legitimate is now refused on the LD route, which leaves via-C as its only route. ESBMC no longer drops an operator block that writes a variable through an `outVariable` (esbmc/esbmc#7389): `outVariable FILTERED_VALUE driven by SUB output OUT`.

## Known-issue tags

A tag stays only while its defect reproduces on ESBMC master (5fd48ec70f):

| Tag | Defect | Status on master | Tasks |
|---|---|---|---|
| `known-issue-esbmc-7577` | OR branches into one coil | does not reproduce | tag removed from 20 |
| `known-issue-esbmc-7578` | FBD body skipped | fixed by esbmc/esbmc#7365 | tag removed from 1 |
| `known-issue-esbmc-7352` | scan order | fixed by esbmc/esbmc#8036 | tag removed from 1 |
| `known-issue-esbmc-7579` | Boolean operators in FB bodies | fixed by esbmc/esbmc#8035 | tag removed from 1 |
| `known-issue-esbmc-7580` | FB input wiring | fix open as esbmc/esbmc#8034 | kept on `manufacturing/g_two_hand_fb` |

Removing a tag does not promote a task: it stays `candidate` unless every one of its variants agrees on both routes.

## Promoted to `validated`

Under the rule of `validation_2026-09-27.md`, one task: `packaging/guard_door_interlock`, which was held back only by #7352.

## Still `candidate`

85 tasks:

- **36 with no LD route** (19 ST, 5 FBD, 5 SFC, 3 IL, the 5 SWaT ST programs, and the ST `counter_scalability`): their only route is via-C, so the two-route rule cannot be met.
- **29 plain-text LD tasks** with variants that only the via-C route settled: 14 LD-route timeouts at 60 s, and 15 variants refused as an undriven sink because the converter renders a constant coil (`OTE(x) := FALSE`) as a coil with no power source.
- **9 graphical LD tasks** without a via-C verdict: 8 variants have no via-C record, and 2 timed out.
- **9 plain-text `ld_*` tasks** that neither route ran.
- **2 graphical LD tasks** with no verdict on either route: `g_fwd_rev_interlock`, `g_traffic_light_pedestrian`.
