(* ============================================================
   Buffer Switch Lockout : CLEAN baseline
   Safety: If the car impacts the pit buffer, the buffer_switch
   trips. This must latch and strictly prevent the car from 
   running until manually reset by maintenance.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM buffer_lockout
  VAR
    buffer_switch AT %IX0.0 : BOOL;
    maint_reset AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    trip_latch AT %QX0.0 : BOOL;
    car_run AT %QX0.1 : BOOL;
  END_VAR

  trip_latch := buffer_switch OR (trip_latch AND NOT maint_reset);
  car_run := req_run AND NOT trip_latch;
END_PROGRAM
