# Prompt for the second Grok review run

Give Grok only these files: `README.md`, `review_pack.md`, `review_sheet.csv` (blank), the `programs/` folder, and this prompt. Do not give it anything from `IEC61131_MultiPass_Review_Package/`, so the run stays blind to the first one.

## Prompt

You are an independent expert in IEC 61131-3 programming and PLC scan-cycle semantics. Follow `README.md` exactly: for each of the 47 rows of `review_sheet.csv`, decide `agree`, `disagree`, or `unsure` for the expected verdict, decide `yes` or `no` for whether the stated assumptions are the ones the verdict needs, and write a comment for every `disagree`, `unsure`, or `no`. Run no verifier and no model checker before you record a verdict.

Reading rules, because a first run marked 15 variants "source not present" although every source is in the package:

1. `review_pack.md` has 1,145 lines. Read it completely, in blocks of at most 250 lines, and do not stop at the first block.
2. Each benchmark has a `###` heading, its semantics, its properties, and one or more `Variant` entries. Thirty variants print the program inline. Seventeen print "Program has N lines; open `programs/...`", and the file is in the `programs/` folder.
3. The table below gives the location of the source of every row. Open it before you judge the row.
4. Enter `unsure` only when the program, the property, or the semantics is genuinely insufficient to decide. Name the missing item and the file or line you looked at. "Source not present" is acceptable only if the file in the table does not exist.
5. Judge each row from the program text, the property, and the stated semantics. Do not infer a verdict from the expected verdict alone.

Output: a copy of `review_sheet.csv` with the three reviewer columns filled, saved as `review_sheet_rerun.csv`, plus a count of agree, unsure, and disagree per stratum. Report every disagreement without filtering. Do not edit any other file.

## Where each source is

| Benchmark | Variant | Source |
|---|---|---|
| counter_scalability | bomb_N00255.st | inline, `review_pack.md` line 14 |
| counter_scalability | bomb_N01023.st | inline, `review_pack.md` line 59 |
| counter_scalability | bomb_N04095.st | inline, `review_pack.md` line 104 |
| counter_scalability | bomb_N16383.st | inline, `review_pack.md` line 149 |
| counter_scalability | bomb_N32767.st | inline, `review_pack.md` line 194 |
| fbd_counter_reset | program.xml | `programs/fbd_counter_reset/program.xml` |
| g_ctd_load | program.xml | inline, `review_pack.md` line 257 |
| g_guard_lock | program.xml | inline, `review_pack.md` line 289 |
| g_guard_lock | no_rundown.xml | inline, `review_pack.md` line 324 |
| g_ton_single | program.xml | inline, `review_pack.md` line 351 |
| g_tp_pulse | program.xml | inline, `review_pack.md` line 391 |
| il_counter_reset | counter_reset.il | inline, `review_pack.md` line 422 |
| ld_timer_latch_mix | timer_latch_mix.ld | inline, `review_pack.md` line 464 |
| ld_tof_hold | tof_hold.ld | inline, `review_pack.md` line 480 |
| ld_tp_pulse | tp_pulse.ld | inline, `review_pack.md` line 495 |
| st_guard_lock | guard_lock.st | inline, `review_pack.md` line 510 |
| st_swat_timer1 | sleg_timer1_0.st | `programs/st_swat_timer1/sleg_timer1_0.st` |
| st_swat_timer1 | smal_timer1_0.st | `programs/st_swat_timer1/smal_timer1_0.st` |
| conveyor_jam_lockout | clean.st | inline, `review_pack.md` line 565 |
| conveyor_jam_lockout | bomb.st | inline, `review_pack.md` line 612 |
| dosing_pump_lockout | clean.st | inline, `review_pack.md` line 671 |
| dosing_pump_lockout | bomb.st | inline, `review_pack.md` line 715 |
| fbd_seal_in | program.xml | `programs/fbd_seal_in/program.xml` |
| g_two_hand | program.xml | inline, `review_pack.md` line 779 |
| g_two_hand | type_i.xml | inline, `review_pack.md` line 798 |
| ld_latch_basic | latch_basic.ld | inline, `review_pack.md` line 824 |
| st_compressor_cycle | compressor_cycle.st | inline, `review_pack.md` line 839 |
| st_estop_reset | estop_reset.st | inline, `review_pack.md` line 869 |
| st_two_hand | two_hand.st | inline, `review_pack.md` line 907 |
| g_start_cycle | lstart_cycle.xml | `programs/g_start_cycle/lstart_cycle.xml` |
| g_tank_assignment | legitimate_lassignment.xml | `programs/g_tank_assignment/legitimate_lassignment.xml` |
| g_tank_assignment | malicious_massignment.xml | `programs/g_tank_assignment/malicious_massignment.xml` |
| g_tank_start_eq | legitimate_lstart_eq.xml | `programs/g_tank_start_eq/legitimate_lstart_eq.xml` |
| g_tank_start_eq | malicious_mstart_eq.xml | `programs/g_tank_start_eq/malicious_mstart_eq.xml` |
| g_tank_start_le | legitimate_lstart_le.xml | `programs/g_tank_start_le/legitimate_lstart_le.xml` |
| g_tank_start_le | malicious_mstart_le.xml | `programs/g_tank_start_le/malicious_mstart_le.xml` |
| g_tank_stop_ge | legitimate_lstop_ge.xml | `programs/g_tank_stop_ge/legitimate_lstop_ge.xml` |
| g_tank_stop_ge | malicious_mstop_ge.xml | `programs/g_tank_stop_ge/malicious_mstop_ge.xml` |
| g_tank_value_filtering | legitimate_lvalue_filtering.xml | `programs/g_tank_value_filtering/legitimate_lvalue_filtering.xml` |
| g_tank_value_filtering | malicious_mvalue_filtering.xml | `programs/g_tank_value_filtering/malicious_mvalue_filtering.xml` |
| g_bus_coupler_changeover | clean.xml | inline, `review_pack.md` line 1031 |
| g_bus_coupler_changeover | bomb.xml | inline, `review_pack.md` line 1050 |
| g_motor_interlock | clean.xml | `programs/g_motor_interlock/clean.xml` |
| g_motor_interlock | bomb.xml | `programs/g_motor_interlock/bomb.xml` |
| g_phase_hold_permissive | clean.xml | inline, `review_pack.md` line 1092 |
| g_phase_hold_permissive | bomb.xml | inline, `review_pack.md` line 1111 |
| ld_ftrig_edge | ftrig_edge.ld | inline, `review_pack.md` line 1137 |
