(* ============================================================
   Trip Lockout Relay (86) : CLEAN baseline
   Safety: A protection relay trip must set the lockout_86 latch,
   preventing the circuit breaker from closing. The latch 
   requires a manual reset after the fault is cleared.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM lockout_relay
  VAR
    protection_trip AT %IX0.0 : BOOL;
    manual_reset AT %IX0.1 : BOOL;
    req_close AT %IX0.2 : BOOL;
    lockout_86 AT %QX0.0 : BOOL;
    breaker_close AT %QX0.1 : BOOL;
  END_VAR

  lockout_86 := protection_trip OR (lockout_86 AND NOT manual_reset);
  breaker_close := req_close AND NOT lockout_86;
END_PROGRAM
