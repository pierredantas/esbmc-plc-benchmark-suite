(* ============================================================
   Elevator door/motion dual interlock.
   Safety intent: the car must never move while either door is
   open; separately, the car must never move while the overload
   sensor is tripped. These are two independent hazards on the
   same actuator, not two views of one condition.
   ============================================================ *)
PROGRAM elevator_control
  VAR
    door_open        AT %IX0.0 : BOOL;
    overload_tripped AT %IX0.1 : BOOL;
    move_request     AT %IX0.2 : BOOL;
    car_moving        AT %QX0.0 : BOOL;
  END_VAR

  IF door_open OR overload_tripped THEN
    car_moving := FALSE;
  ELSIF move_request THEN
    car_moving := TRUE;
  ELSE
    car_moving := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : elevator_control;
  END_RESOURCE
END_CONFIGURATION
