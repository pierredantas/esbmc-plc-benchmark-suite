(* ============================================================
   Freeze Stat Trip : CLEAN baseline
   Safety: A tripped freeze stat must stop the AHU supply fan
   and latch. It must require a manual reset_btn to clear,
   preventing the fan from auto-restarting if the coil warms up.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM freeze_protection
  VAR
    freeze_stat AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    freeze_latch AT %QX0.0 : BOOL;
    fan_run AT %QX0.1 : BOOL;
  END_VAR

  freeze_latch := freeze_stat OR (freeze_latch AND NOT reset_btn);
  fan_run := req_run AND NOT freeze_latch;
END_PROGRAM
