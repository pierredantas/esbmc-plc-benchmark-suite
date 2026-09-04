(* ============================================================
   Stairwell Smoke Exhaust : CLEAN baseline
   Safety: The smoke exhaust fan must not run if the isolation
   damper is confirmed closed, preventing duct implosion.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM smoke_exhaust
  VAR
    smoke_alarm AT %IX0.0 : BOOL;
    damper_closed AT %IX0.1 : BOOL;
    exhaust_fan AT %QX0.0 : BOOL;
  END_VAR

  exhaust_fan := smoke_alarm AND NOT damper_closed;
END_PROGRAM
