(* ============================================================
   Pedestrian Conflict Interlock : CLEAN baseline
   Safety: A pedestrian walk signal must never illuminate if
   the parallel vehicle green OR conflicting turn arrow is active.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM ped_interlock
  VAR
    req_ped AT %IX0.0 : BOOL;
    veh_green AT %IX0.1 : BOOL;
    turn_arrow AT %IX0.2 : BOOL;
    ped_walk AT %QX0.0 : BOOL;
  END_VAR

  ped_walk := req_ped AND NOT veh_green AND NOT turn_arrow;
END_PROGRAM
