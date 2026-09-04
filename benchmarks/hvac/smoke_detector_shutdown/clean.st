(* ============================================================
   Smoke Detector Shutdown : CLEAN baseline
   Safety: Duct smoke detection must instantly latch and shut
   down the supply fan to prevent smoke distribution. A manual
   reset is required to clear the latch.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM smoke_shutdown
  VAR
    smoke_detect AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    smoke_latch AT %QX0.0 : BOOL;
    fan_run AT %QX0.1 : BOOL;
  END_VAR

  smoke_latch := smoke_detect OR (smoke_latch AND NOT reset_btn);
  fan_run := req_run AND NOT smoke_latch;
END_PROGRAM
