(* ============================================================
   Guard Door Interlock : CLEAN baseline
   Safety: The packaging machine drive must never run unless
   the physical guard door is closed and latched safely.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM guard_safety
  VAR
    req_run AT %IX0.0 : BOOL;
    guard_closed AT %IX0.1 : BOOL;
    estop_pressed AT %IX0.2 : BOOL;
    safety_relay AT %QX0.0 : BOOL;
    machine_run AT %QX0.1 : BOOL;
  END_VAR

  safety_relay := guard_closed AND NOT estop_pressed;
  machine_run := req_run AND safety_relay;
END_PROGRAM
