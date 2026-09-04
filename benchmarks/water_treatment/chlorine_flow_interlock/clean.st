(* ============================================================
   Chlorine Flow Interlock : CLEAN baseline
   Safety: The chlorine dosing pump must never run if the 
   main water line flow is below the minimum threshold (low_flow),
   preventing toxic gas accumulation.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM dosing_interlock
  VAR
    req_dose AT %IX0.0 : BOOL;
    low_flow AT %IX0.1 : BOOL;
    dose_pump AT %QX0.0 : BOOL;
  END_VAR

  dose_pump := req_dose AND NOT low_flow;
END_PROGRAM
