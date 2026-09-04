(* ============================================================
   Capper Torque Stop : CLEAN baseline
   Safety: A torque_fault must instantly stop the capper motor
   and require a manual fault_reset to clear the fault_latch.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM capper
  VAR
    torque_fault AT %IX0.0 : BOOL;
    fault_reset AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    fault_latch AT %QX0.0 : BOOL;
    motor_run AT %QX0.1 : BOOL;
  END_VAR

  fault_latch := torque_fault OR (fault_latch AND NOT fault_reset);
  motor_run := req_run AND NOT fault_latch;
END_PROGRAM
