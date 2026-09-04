(* ============================================================
   Fire Damper Interlock : CLEAN baseline
   Safety: The main Air Handling Unit (AHU) fan must never run
   unless the isolation fire damper is fully open, to prevent
   the fan from imploding the ductwork against a closed damper.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM fire_damper
  VAR
    req_run AT %IX0.0 : BOOL;
    damper_open AT %IX0.1 : BOOL;
    ahu_fan AT %QX0.0 : BOOL;
  END_VAR

  ahu_fan := req_run AND damper_open;
END_PROGRAM
