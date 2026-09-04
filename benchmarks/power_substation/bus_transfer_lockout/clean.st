(* ============================================================
   Bus Transfer Lockout : CLEAN baseline
   Safety: The bus tie breaker must not close if both Source A 
   and Source B mains are already closed (preventing unsynced ties).
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM bus_tie
  VAR
    req_tie AT %IX0.0 : BOOL;
    source_a_closed AT %IX0.1 : BOOL;
    source_b_closed AT %IX0.2 : BOOL;
    tie_close AT %QX0.0 : BOOL;
  END_VAR

  tie_close := req_tie AND NOT (source_a_closed AND source_b_closed);
END_PROGRAM
