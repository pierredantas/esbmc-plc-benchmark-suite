(* ============================================================
   Agitator Temp Interlock : CLEAN baseline
   Safety: The reactor heater must never be energized unless
   the agitator is actively running, preventing local boiling.
   It must also trip if the high_temp limit is reached.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM heater_interlock
  VAR
    req_heat AT %IX0.0 : BOOL;
    agitator_run AT %IX0.1 : BOOL;
    high_temp AT %IX0.2 : BOOL;
    heater_run AT %QX0.0 : BOOL;
  END_VAR

  heater_run := req_heat AND agitator_run AND NOT high_temp;
END_PROGRAM
