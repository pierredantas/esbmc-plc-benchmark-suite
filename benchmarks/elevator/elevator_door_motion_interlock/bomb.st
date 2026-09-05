(* ============================================================
   Elevator door/motion dual interlock : BOMB variant.
   Seeded defect: the combined guard was split into a
   door-only check, and the overload check was moved to a
   separate, independent IF that only ever forces the car to
   stop, never preventing a move_request from starting it in the
   same scan the overload sensor is tripped.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM elevator_control
  VAR
    door_open        AT %IX0.0 : BOOL;
    overload_tripped AT %IX0.1 : BOOL;
    move_request     AT %IX0.2 : BOOL;
    car_moving        AT %QX0.0 : BOOL;
  END_VAR

  IF door_open THEN
    car_moving := FALSE;
  ELSIF move_request THEN
    car_moving := TRUE;
  ELSE
    car_moving := FALSE;
  END_IF;

  IF overload_tripped AND NOT move_request THEN
    car_moving := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : elevator_control;
  END_RESOURCE
END_CONFIGURATION
