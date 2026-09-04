(* ============================================================
   Palletizer Light Curtain : CLEAN baseline
   Safety: A tripped light curtain (curtain_ok = 0) drops the
   safety_latch. It must require a dedicated reset_btn to
   restore the latch, preventing automatic machine restart.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM palletizer
  VAR
    curtain_ok AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    safety_latch AT %QX0.0 : BOOL;
    machine_run AT %QX0.1 : BOOL;
  END_VAR

  safety_latch := curtain_ok AND (safety_latch OR reset_btn);
  machine_run := req_run AND safety_latch;
END_PROGRAM
