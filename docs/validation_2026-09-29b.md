# Two-route validation after the suite fixes, September 29, 2026

The check of `validation_2026-09-29.md` was repeated after four fixes to this repository, on the same ESBMC build (pierredantas/esbmc `ws0-integration` 4a9dbe2) and with the same routes and 60 s timeout. `validation_2026-09-29b.tsv` has one row per variant.

## What changed in the repository

- **Graphical block programs readable by Beremiz.** Nine graphical programs with timers, counters or a user function block never reached the via-C route. Beremiz reads the starting point of every wire that leaves a block, and these wires had none; their instances (`TON0 : TON`, ...) were also missing from the program interface, which PLCopen requires and MatIEC enforces.
- **Constant coils and property-only inputs.** A plain-text rung `OTE(x) := FALSE ;` became a coil fed by an `<inVariable>`, which carries no power flow, and ESBMC refused it as an undriven sink; the left rail now powers a reset coil (FALSE) or a plain coil (TRUE). A bomb variant that stops reading a sensor left the property's variable undeclared, and the ingestion gate refused the run; the text-LD conversion now declares such variables as inputs, as `runner/record_via_c.py` already did.
- **Timers, counters and set/reset coils in the text-LD DSL.** Eleven `ld_*` tasks never reached either route, because the converter refused TON, TOF, TP, CTU, CTD, OTL and OTU (and two edge tasks only because their comments mention R_TRIG and F_TRIG). Every file that converted before converts byte for byte as it did.
- **Two labels corrected against their syntax twins.** `ld_tp_pulse` has `g_tp_pulse`'s program and property but was labelled SAFE; a TP holds its output through the pulse after the trigger drops, so it is VIOLATION, as the twin says. `ld_tof_hold`'s property forbade the off-delay hold its own justification calls intended; it now uses `g_tof_hold`'s property.

## Result

292 variants (the 281 of the previous run plus the 11 `ld_*` tasks that now convert): 202 agree with their expected verdict on both routes, 53 on via-C only, and 24 on the LD route only, so 279 are corroborated. No expected verdict is contradicted by both routes. The 5 `counter_scalability` bombs are still deeper than the via-C scan bound, and 8 variants have no usable verdict.

31 variants moved from one route to both (29 plain-text variants from the constant-coil and property-input fixes, and both `g_two_hand_fb` variants); none moved the other way.

## Promoted to `validated`

Under the rule of `validation_2026-09-27.md`, 32 tasks: every one of their variants agrees on both routes and none carries a known-issue tag.

- `building_automation/access_door_forced_ds`, `fire_damper_interlock_ds`, `intrusion_dual_alarm`, `stairwell_pressurization_ds`, `stairwell_smoke_exhaust`
- `chemical_batch/relief_valve_trip_ds`
- `elevator/buffer_switch_lockout_ds`, `fire_service_recall_ds`, `ld_ctd_load`, `overspeed_trip_latch_ds`
- `hvac/freeze_stat_trip_ds`, `purge_fault_lockout`
- `manufacturing/two_hand_anti_tie_down`
- `motor_control/ld_latch_basic`
- `packaging/capper_torque_stop_ds`, `case_sealer_jam_ds`, `labeler_web_break_ds`, `ld_ctu_saturate`, `palletizer_light_curtain_ds`, `reject_gate_triple_output`
- `power_substation/breaker_disconnect_interlock_ds`, `bus_transfer_lockout`, `dead_bus_close_permissive_ds`, `dead_bus_close_permissive_gm`, `sync_check_relay_ds`, `trip_lockout_relay_ds`
- `traffic/all_red_clearance_gm`, `conflict_monitor_trip_ds`, `ped_conflict_interlock_ds`, `ped_conflict_interlock_gm`, `train_preempt_lockout_ds`
- `water_treatment/chemical_feed_fault_lockout`

The suite now has 122 validated and 53 candidate tasks.

## Still `candidate`

- **36 with no LD route** (ST, FBD, SFC, IL): their only route is via-C, so the two-route rule cannot be met.
- **14 LD tasks settled by the LD route only**, because the via-C run times out: the timer and counter programs, and the graphical tank programs. The cost is in the route, not the program: on MatIEC's generated C for `g_ctd_load`, an 8-scan harness does not finish in 900 s under k-induction nor in 300 s under plain unwinding, while a 3-scan harness finishes in 40 s but is too shallow to reach the preset.
- **2 graphical LD tasks with no verdict**: `g_fwd_rev_interlock`, and `g_traffic_light_pedestrian`, whose ST MatIEC rejects.
- **`manufacturing/g_two_hand_fb`**: both variants agree on both routes; it keeps `known-issue-esbmc-7580` until esbmc/esbmc#8034 is merged.
