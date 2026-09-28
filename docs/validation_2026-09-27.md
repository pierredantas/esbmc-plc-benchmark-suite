# Two-route validation, September 27, 2026

Every variant in `benchmarks/` was re-checked by two routes that share no front end:

- **LD route**: `runner/record_all.py --route ld`, ESBMC's LD front end at
  pierredantas/esbmc `ws0-integration` (c35482d), with the ingestion gate.
- **via-C route**: `runner/record_via_c.py`, PLCopen XML to Beremiz to MatIEC C to ESBMC's C
  front end; plain-text LD converted by `tools/ld_text_to_xml.py` first.

`validation_2026-09-27.tsv` has one row per variant: expected verdict, the verdict on each
route, and the resulting category. A via-C violation counts only when the violated claim is a
property from `props.yaml`.

## Result

Of 281 variants, 165 agree with their expected verdict on both routes, 81 on via-C only, 20 on
the LD route only, 9 have no usable verdict, and 5 are `counter_scalability` bombs whose fuse
is deeper than the via-C scan bound. No expected verdict is contradicted.

## Promoted to `validated`

A `candidate` task is promoted when every one of its variants agrees on both routes and it
carries no known-issue tag for a defect that still reproduces on ESBMC master. #7577 (OR
branches into one coil) does not reproduce on master 2c5cffd98a, so its tag is removed from
the promoted tasks; tasks tagged with #7352, #7353, #7579 or #7580, whose fixes are not yet
upstream, stay `candidate`.

`building_automation/access_door_forced_gm` is included after its P1 was corrected: the old
invariant forbade the seal-in its own justification requires. P1 is now a `reachable`
property; the clean variant reaches it and the bomb does not, on both routes.

44 tasks:

- `building_automation/access_door_forced_gm`
- `building_automation/emer_light_transfer`
- `building_automation/fire_damper_interlock_gm`
- `building_automation/g_comb_mixed`
- `building_automation/g_comb_or`
- `building_automation/g_door_reversal`
- `building_automation/stairwell_pressurization_gm`
- `chemical_batch/agitator_temp_interlock_ds`
- `chemical_batch/agitator_temp_interlock_gm`
- `chemical_batch/dual_valve_containment_ds`
- `chemical_batch/dual_valve_containment_gm`
- `chemical_batch/g_independent_hp_trip`
- `chemical_batch/g_phase_hold_permissive`
- `chemical_batch/g_vessel_empty_permissive`
- `chemical_batch/nitrogen_purge_permissive`
- `chemical_batch/relief_valve_trip_gm`
- `elevator/buffer_switch_lockout_gm`
- `elevator/door_zone_interlock`
- `elevator/fire_service_recall_gm`
- `elevator/overload_weighing_hold`
- `elevator/overspeed_trip_latch_gm`
- `hvac/freeze_stat_trip_gm`
- `hvac/smoke_detector_shutdown`
- `motor_control/g_failsafe_motor_latch`
- `motor_control/thermal_overload_latch`
- `motor_control/vfd_bypass_interlock`
- `packaging/capper_torque_stop_gm`
- `packaging/case_sealer_jam_gm`
- `packaging/labeler_web_break_gm`
- `packaging/palletizer_light_curtain_gm`
- `power_substation/breaker_disconnect_interlock_gm`
- `power_substation/g_bus_coupler_changeover`
- `power_substation/g_dead_bus_close_check`
- `power_substation/g_trip_lockout_86`
- `power_substation/protection_lockout_cascade`
- `power_substation/sync_check_relay_gm`
- `power_substation/trip_lockout_relay_gm`
- `traffic/all_red_clearance_ds`
- `traffic/conflict_monitor_trip_gm`
- `traffic/rr_crossing_preempt`
- `traffic/train_preempt_lockout_gm`
- `water_treatment/backwash_valve_lockout`
- `water_treatment/chlorine_flow_interlock`
- `water_treatment/g_pump_alternation`
