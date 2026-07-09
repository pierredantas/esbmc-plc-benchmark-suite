# P6 — Finalized 50-program selection (v1.0)

**Composition:** 25 textual LD · 20 graphical LD · 5 ST — across **10 industrial domains**.
**Distinct programs:** 41 (9 provided in BOTH textual + graphical form as deliberate
*syntax-coverage pairs* — a differential-testing feature, labeled as such, not padding).

**Status:** `drop-in` = program + props exist · `props-needed` = program exists, write YAML ·
`convert` = graphical twin of a textual program (inherits props) · `author` = new program
(native graphical, written clean + fault-injected mutant + props).
**GT:** `expert` · `consensus` · `fault-inj` (legit/malicious pair, witness ready).

---

## Full list (50 tasks)

### Textual LD (25)
| # | id | domain | source | status | GT |
|---|---|---|---|---|---|
| 1 | motor_start_cycle | motor_control | PLC-LD | props-needed | fault-inj |
| 2 | motor_start_eq | motor_control | PLC-LD | props-needed | fault-inj |
| 3 | motor_stop_ge | motor_control | PLC-LD | props-needed | fault-inj |
| 4 | motor_subst_coil | motor_control | PLC-LD | props-needed | fault-inj |
| 5 | motor_interlock | motor_control | PLC-Sec S2 | drop-in | fault-inj |
| 6 | ld_latch_basic | motor_control | K-LD | drop-in | expert |
| 7 | ld_seal_in | motor_control | K-LD | drop-in | expert |
| 8 | tank_overflow | water_treatment | PLC-Sec S1 | drop-in | expert |
| 9 | valve_handler | chemical_batch | PLC-LD | props-needed | fault-inj |
| 10 | value_filter | chemical_batch | PLC-LD | props-needed | fault-inj |
| 11 | sub_function | chemical_batch | PLC-LD | props-needed | fault-inj |
| 12 | assignment | chemical_batch | PLC-LD | props-needed | fault-inj |
| 13 | counter_scalability | manufacturing | PLC-Sec S5 | drop-in | expert |
| 14 | ld_comb_mixed | building_automation | K-LD | drop-in | expert |
| 15 | ld_ton_single | hvac | K-LD | drop-in | expert |
| 16 | ld_tof_hold | hvac | K-LD | drop-in | expert |
| 17 | ld_tp_pulse | packaging | K-LD | drop-in | expert |
| 18 | ld_ctu_saturate | packaging | K-LD | drop-in | expert |
| 19 | ld_ctd_load | elevator | K-LD | drop-in | expert |
| 20 | ld_edge_counter | traffic | K-LD | drop-in | expert |
| 21 | ld_timer_latch_mix | elevator | K-LD | drop-in | expert |
| 22 | motor_start_le | motor_control | PLC-LD | props-needed | fault-inj |
| 23 | motor_stop_gt | power_substation | PLC-LD | props-needed | fault-inj |
| 24 | motor_stop_eq | power_substation | PLC-LD | props-needed | fault-inj |
| 25 | sensor_forge | water_treatment | PLC-Sec S3 | drop-in | fault-inj |

### Graphical LD (20)
| # | id | domain | source | status | GT |
|---|---|---|---|---|---|
| 26 | g_ppu_evolution_1 | manufacturing | PPU LD_EVOLUTION_1 | props-needed | expert |
| 27 | g_ppu_evolution_4 | manufacturing | PPU LD_EVOLUTION_4 | props-needed | expert |
| 28 | g_ppu_evolution_5 | manufacturing | PPU LD_EVOLUTION_5 | props-needed | expert |
| 29 | g_ppu_evolution_6 | manufacturing | PPU LD_EVOLUTION_6 | props-needed | expert |
| 30 | g_ppu_evolution_7 | manufacturing | PPU LD_EVOLUTION_7 | props-needed | expert |
| 31 | g_traffic_light | traffic | **authored** | author | fault-inj |
| 32 | g_hvac_fan_delay | hvac | **authored** | author | fault-inj |
| 33 | g_elevator_door | elevator | **authored** | author | fault-inj |
| 34 | g_packaging_filler | packaging | **authored** | author | fault-inj |
| 35 | g_building_lighting | building_automation | **authored** | author | fault-inj |
| 36 | g_substation_breaker | power_substation | **authored** | author | fault-inj |
| 37 | g_motor_interlock | motor_control | pair of #5 | convert | fault-inj |
| 38 | g_ld_latch_basic | motor_control | pair of #6 | convert | expert |
| 39 | g_ld_seal_in | motor_control | pair of #7 | convert | expert |
| 40 | g_tank_overflow | water_treatment | pair of #8 | convert | expert |
| 41 | g_valve_handler | chemical_batch | pair of #9 | convert | fault-inj |
| 42 | g_ld_ton_single | hvac | pair of #15 | convert | expert |
| 43 | g_ld_ctu_saturate | packaging | pair of #18 | convert | expert |
| 44 | g_ld_edge_counter | traffic | pair of #20 | convert | expert |
| 45 | g_counter_scalability | manufacturing | pair of #13 | convert | expert |

### ST (5)
| # | id | domain | source | status | GT |
|---|---|---|---|---|---|
| 46 | st_water_eq1 | water_treatment | SWaT EQ1 | props-needed | fault-inj |
| 47 | st_water_level1 | water_treatment | SWaT level1 | props-needed | fault-inj |
| 48 | st_water_timer1 | water_treatment | SWaT timer1 | props-needed | fault-inj |
| 49 | st_if_assignment | chemical_batch | PPU ST_IF | props-needed | expert |
| 50 | st_for_case | manufacturing | PPU ST_FOR_CASE | props-needed | expert |

---

## Domain distribution (10 domains, every domain has a real or authored anchor)

| domain | count | anchor |
|---|---|---|
| motor_control | 8 | PLC-LD + S2 (real) |
| water_treatment | 6 | SWaT + S1/S3 (real) |
| manufacturing | 7 | PPU + S5 (real) |
| chemical_batch | 6 | PLC-LD valve/filter (real) |
| hvac | 4 | authored + timers |
| packaging | 4 | authored + counters |
| elevator | 3 | authored + counters |
| traffic | 3 | authored + edge counter |
| building_automation | 3 | authored + comb logic |
| power_substation | 6 | authored breaker + PLC-LD |

## Work tally (final)

| bucket | count | task |
|---|---|---|
| drop-in (program + props exist) | 13 | verify only |
| props-needed (write YAML) | 22 | property authoring |
| convert (graphical twin, inherit props) | 9 | GraphPLC XML re-authoring |
| author (new program + mutant + props) | 6 | native graphical authoring |

**Property files to write:** ~28 (22 props-needed + 6 authored). Syntax-pairs inherit.
**Ground truth:** ~24 tasks fault-injection (witness ready); 26 expert/consensus.

## Transparency notes for the paper
1. **50 tasks over 41 distinct programs**; 9 are textual/graphical syntax-coverage pairs —
   framed as a differential-testing feature (does a tool handle both PLCopen encodings of
   identical logic?). State this plainly in §Suite Composition.
2. **6 authored programs** carry the thin domains (traffic, hvac, elevator, packaging,
   building_automation, power_substation) with genuine domain logic — no analogy-labeling.
3. Every domain has ≥1 **real or authored** anchor; feature benchmarks only supplement.
