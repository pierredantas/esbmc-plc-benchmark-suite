(* ============================================================
   Overspeed Trip Latch : CLEAN baseline
   Safety: If the overspeed governor drops out (speed_ok = 0),
   the trip_latch must set and drop the car_run permissive.
   It must require a manual reset_key to clear.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM overspeed
  VAR
    speed_ok AT %IX0.0 : BOOL;
    reset_key AT %IX0.1 : BOOL;
    run_cmd AT %IX0.2 : BOOL;
    trip_latch AT %QX0.0 : BOOL;
    car_run AT %QX0.1 : BOOL;
  END_VAR

  (* Latch sets if speed is not OK, unlatches only via reset_key *)
  trip_latch := NOT speed_ok OR (trip_latch AND NOT reset_key);
  car_run := run_cmd AND NOT trip_latch;
END_PROGRAM
