(* ============================================================
   Sync Check Relay (25) : CLEAN baseline
   Safety: The line breaker must only close if the line is dead,
   OR if the sync check relay verifies phase alignment (sync_ok).
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM sync_check
  VAR
    req_close AT %IX0.0 : BOOL;
    line_live AT %IX0.1 : BOOL;
    sync_ok AT %IX0.2 : BOOL;
    breaker_close AT %QX0.0 : BOOL;
  END_VAR

  breaker_close := req_close AND (NOT line_live OR sync_ok);
END_PROGRAM
