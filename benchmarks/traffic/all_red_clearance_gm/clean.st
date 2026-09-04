(* ============================================================
   All Red Clearance : CLEAN baseline
   Safety: The North-South green signal must strictly require 
   the East-West signal to report physically red (ew_red) to
   prevent conflicting right-of-way collisions.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM all_red
  VAR
    req_ns_green AT %IX0.0 : BOOL;
    ew_red AT %IX0.1 : BOOL;
    ns_green AT %QX0.0 : BOOL;
  END_VAR

  ns_green := req_ns_green AND ew_red;
END_PROGRAM
