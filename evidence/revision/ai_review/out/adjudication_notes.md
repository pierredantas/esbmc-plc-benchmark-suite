# Adjudication: blind review of semantics.yml by gemini-3.8-flash

Reviewer: gemini-3.8-flash, Google AI Studio. System instructions: PROMPT.md. Thinking level: Medium. Search grounding: off. Temperature: default (the interface offered no control). Date: 2026-10-30. One run, 15 batches, one chat per batch. Raw replies: ../replies/. Answers: answers.csv. Comparison: ../compare_ai_review.py.

## Result before correction
54 differing fields on 37 benchmarks: retained_state 23, verdict_scope 16, overflow_possible 11, setreset_coils 3, scan_order 1.

## Adjudication

| Field | Differences | Adjudication |
|---|---|---|
| retained_state | 23 (22 reviewer yes / record no; 1 reviewer no / record yes) | **Reviewer right on all 23.** Each was confirmed by running the program through Beremiz and MATIEC from two random input histories with the same final inputs (history_dependence.py, results in history_dependence.json, 110 programs). The record lacked retained state for 22 benchmarks (conveyor_jam_lockout, fbd_counter_reset, fbd_seal_in, g_start_cycle, g_stop_eq, g_tank_assignment, g_tank_start_eq, g_tank_start_le, g_tank_stop_ge, g_tank_sub_function, g_tank_substitution_coil, g_tank_value_filtering, g_tank_valves, g_two_hand_fb, il_counter_reset, il_seal_in, kiln_door_lockout, reactor_pressure_lockout, sfc_batch_fill_drain, sfc_counter_reset, sfc_elevator_door, st_counter_reset) and claimed it for sensor_forge, whose outputs are assigned unconditionally from current inputs. Corrected: 56 -> 77 benchmarks with retained state. |
| scan_order | 1 (g_traffic_light_pedestrian) | **Reviewer right.** The main program body is FBD (with an LD function block and an SFC); the order is tool-defined. Corrected: rung 73 -> 72, tool-defined 8 -> 9. |
| overflow_possible | 11, all reviewer yes / record no | **Both defensible; record kept.** The programs do bounded integer arithmetic that can overflow. The record flags H1 only where a SAFE verdict would become conditional on no overflow; for these 11 the property (a reset invariant, termination, or a violation reached before any overflow) does not depend on it. Rule now stated in Section 4.5. |
| verdict_scope | 16 (15 reviewer holds / record semantics-dependent; 1 reverse: counter_scalability) | **Both defensible; record kept.** The record marks a verdict semantics-dependent whenever the program uses a timer, a counter, or a set/reset coil (or H1 applies), whether or not the property would actually change. The reviewer judged whether the property's truth depends on the model. Conservative flagging stated in Section 4.5. |
| setreset_coils | 3 | **Not an error.** The record has no separate set/reset field; programs with set/reset coils and timers are flagged through the timer model. |

## Limits
- One run; the second run in reverse order recommended in README.md was not done. The objective history test replaces it for retained state.
- history_dependence.py cannot test 7 programs (5 SWaT ST programs that MATIEC cannot parse, g_traffic_light_pedestrian, g_ppu_evolution_1). For them the record and the reviewer agree, and the programs were read.
- st_swat_timer1: the test reports no history dependence because its timer cannot expire within the 7-scan histories; a TON retains internal state, so the record and the reviewer (both yes) stand.
- The reviewer applies definitions that we wrote to program text that we wrote (or took from others): the review tests the record against our definitions, not against a standard.
- This is a review by a language model, not by a second person.

## After correction
Agreement with the record: scan_order 117/117, retained_state 117/117, timers_or_counters 117/117, overflow_possible 106/117, setreset_coils 114/117, verdict_scope 101/117 (30 definitional differences on 28 benchmarks, review_after_disagreements.csv).
