(* ============================================================
   Overload Weighing Hold : CLEAN baseline
   Safety: An overloaded car (weight_high) must latch the trip
   state and prevent the brake from lifting. The latch clears
   only when doors are open and the weight drops.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM load_weighing
  VAR
    weight_high AT %IX0.0 : BOOL;
    doors_open AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    overload_latch AT %QX0.0 : BOOL;
    brake_lift AT %QX0.1 : BOOL;
  END_VAR

  overload_latch := weight_high OR (overload_latch AND NOT doors_open);
  brake_lift := req_run AND NOT overload_latch;
END_PROGRAM
