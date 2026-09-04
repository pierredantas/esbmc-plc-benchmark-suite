(* ============================================================
   Breaker Disconnect Interlock : CLEAN baseline
   Safety: The mechanical disconnector (disc_cmd) must never
   be actuated while the main breaker (brk_closed) is closed,
   to prevent catastrophic arcing.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM disconnector
  VAR
    req_disc AT %IX0.0 : BOOL;
    brk_closed AT %IX0.1 : BOOL;
    disc_cmd AT %QX0.0 : BOOL;
  END_VAR

  disc_cmd := req_disc AND NOT brk_closed;
END_PROGRAM
