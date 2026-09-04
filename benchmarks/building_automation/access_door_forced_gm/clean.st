(* ============================================================
   Access Door Forced : CLEAN baseline
   Safety: A door opened without a valid badge sets a forced 
   alarm and drops into a security lockdown latch.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM door_security
  VAR
    door_open AT %IX0.0 : BOOL;
    valid_badge AT %IX0.1 : BOOL;
    guard_reset AT %IX0.2 : BOOL;
    forced_alarm AT %QX0.0 : BOOL;
    lockdown_latch AT %QX0.1 : BOOL;
  END_VAR

  forced_alarm := door_open AND NOT valid_badge;
  lockdown_latch := forced_alarm OR (lockdown_latch AND NOT guard_reset);
END_PROGRAM
