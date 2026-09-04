(* ============================================================
   Relief Valve Trip : CLEAN baseline
   Safety: If a reactor pressure relief valve lifts, the feed
   pump must immediately trip and lock out until manually reset.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM relief_trip
  VAR
    relief_open AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_pump AT %IX0.2 : BOOL;
    trip_latch AT %QX0.0 : BOOL;
    feed_pump AT %QX0.1 : BOOL;
  END_VAR

  trip_latch := relief_open OR (trip_latch AND NOT reset_btn);
  feed_pump := req_pump AND NOT trip_latch;
END_PROGRAM
