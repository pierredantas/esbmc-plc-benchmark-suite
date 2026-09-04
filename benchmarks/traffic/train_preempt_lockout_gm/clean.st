(* ============================================================
   Train Preemption Lockout : CLEAN baseline
   Safety: The vehicle green light (veh_green) must never
   be energized while a train track circuit (train_detect)
   is active.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM preemption
  VAR
    train_detect AT %IX0.0 : BOOL;
    preempt_reset AT %IX0.1 : BOOL;
    timer_green AT %IX0.2 : BOOL;
    lockout_latch AT %QX0.0 : BOOL;
    veh_green AT %QX0.1 : BOOL;
  END_VAR

  (* Latch the lockout if train is detected. Unlatch ONLY if reset and NO train *)
  lockout_latch := train_detect OR (lockout_latch AND NOT preempt_reset);
  veh_green := timer_green AND NOT lockout_latch;
END_PROGRAM
