(* ============================================================
   Conflict Monitor Trip : CLEAN baseline
   Safety: A hardware conflict_detect must latch the intersection
   into flash_mode. Normal solid_green signals must be locked
   out until a manual sys_reset is applied.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM conflict_monitor
  VAR
    conflict_detect AT %IX0.0 : BOOL;
    sys_reset AT %IX0.1 : BOOL;
    req_green AT %IX0.2 : BOOL;
    flash_mode AT %QX0.0 : BOOL;
    solid_green AT %QX0.1 : BOOL;
  END_VAR

  flash_mode := conflict_detect OR (flash_mode AND NOT sys_reset);
  solid_green := req_green AND NOT flash_mode;
END_PROGRAM
