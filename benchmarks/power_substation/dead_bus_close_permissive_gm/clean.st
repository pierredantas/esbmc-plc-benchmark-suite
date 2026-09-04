(* ============================================================
   Dead Bus Close Permissive : CLEAN baseline
   Safety: The tie_close breaker must only close if at least
   one bus is dead, OR if both are live AND synchronization
   is verified (sync_ok).
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM tie_breaker
  VAR
    req_close AT %IX0.0 : BOOL;
    bus1_live AT %IX0.1 : BOOL;
    bus2_live AT %IX0.2 : BOOL;
    sync_ok AT %IX0.3 : BOOL;
    tie_close AT %QX0.0 : BOOL;
  END_VAR

  tie_close := req_close AND (NOT bus1_live OR NOT bus2_live OR sync_ok);
END_PROGRAM
