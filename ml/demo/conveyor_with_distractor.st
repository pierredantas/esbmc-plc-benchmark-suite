(* ============================================================
   Conveyor with unrelated diagnostic counter : demo program, not
   in the suite.
   Safety intent: the belt motor must never run while the
   emergency-stop rope switch is tripped. cycle_count is a
   diagnostic counter unrelated to any safety property.
   ============================================================ *)
PROGRAM belt_control
  VAR
    estop_tripped AT %IX0.0 : BOOL;
    run_request   AT %IX0.1 : BOOL;
    belt_motor    AT %QX0.0 : BOOL;
    cycle_count   : INT := 0;
  END_VAR

  IF estop_tripped THEN
    belt_motor := FALSE;
  ELSIF run_request THEN
    belt_motor := TRUE;
  END_IF;

  IF belt_motor THEN
    cycle_count := cycle_count + 1;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : belt_control;
  END_RESOURCE
END_CONFIGURATION
