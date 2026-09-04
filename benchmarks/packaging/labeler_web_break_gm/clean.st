(* ============================================================
   Labeler Web Break : CLEAN baseline
   Safety: If the label web breaks (web_intact drops), the 
   machine must trip and require a manual reset. It cannot
   run while the fault is latched.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM web_break
  VAR
    web_intact AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    fault_latch AT %QX0.0 : BOOL;
    drive_run AT %QX0.1 : BOOL;
  END_VAR

  fault_latch := NOT web_intact OR (fault_latch AND NOT reset_btn);
  drive_run := req_run AND NOT fault_latch;
END_PROGRAM
