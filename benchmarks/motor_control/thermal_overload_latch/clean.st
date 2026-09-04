(* ============================================================
   Thermal Overload Latch : CLEAN baseline
   Safety: A motor thermal overload trip must instantly drop the
   motor_run permissive and latch. A manual reset is required
   to clear the fault once the motor cools down.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM thermal_latch
  VAR
    thermal_trip AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    overload_latch AT %QX0.0 : BOOL;
    motor_run AT %QX0.1 : BOOL;
  END_VAR

  overload_latch := thermal_trip OR (overload_latch AND NOT reset_btn);
  motor_run := req_run AND NOT overload_latch;
END_PROGRAM
