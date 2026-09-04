(* ============================================================
   Door Zone Interlock : CLEAN baseline
   Safety: Elevator doors must absolutely never open unless
   the car is physically detected within a landing door zone,
   preventing passengers from falling into the shaft.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM door_zone
  VAR
    req_open AT %IX0.0 : BOOL;
    door_zone AT %IX0.1 : BOOL;
    doors_open AT %QX0.0 : BOOL;
  END_VAR

  doors_open := req_open AND door_zone;
END_PROGRAM
