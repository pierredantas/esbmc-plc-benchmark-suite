(* ============================================================
   Machine guard door interlock : demo program, not in the suite.
   Safety intent: the spindle must never run while the guard door
   is open.
   ============================================================ *)
PROGRAM guard_interlock
  VAR
    door_open    AT %IX0.0 : BOOL;
    start_button AT %IX0.1 : BOOL;
    spindle_run  AT %QX0.0 : BOOL;
  END_VAR

  IF door_open THEN
    spindle_run := FALSE;
  ELSIF start_button THEN
    spindle_run := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : guard_interlock;
  END_RESOURCE
END_CONFIGURATION
