(* ============================================================
   Backwash Valve Lockout : CLEAN baseline
   Safety: The filter service valve and backwash valve must
   never be open simultaneously to prevent raw water contamination.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM backwash_seq
  VAR
    req_service AT %IX0.0 : BOOL;
    req_backwash AT %IX0.1 : BOOL;
    service_v AT %QX0.0 : BOOL;
    backwash_v AT %QX0.1 : BOOL;
  END_VAR

  service_v := req_service AND NOT backwash_v;
  backwash_v := req_backwash AND NOT service_v;
END_PROGRAM
