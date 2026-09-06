(* ============================================================
   Packaging conveyor jam lockout.
   Safety intent: the belt drive must never run while the jam
   sensor is tripped. Once a jam has been detected during a
   production run, the belt drive stays off for the remainder of
   that run, even after the jam clears on its own, so an operator
   can inspect the line before the next run_start.
   ============================================================ *)
PROGRAM conveyor_control
  VAR
    jam_detected AT %IX0.0 : BOOL;
    run_start    AT %IX0.1 : BOOL;
    run_stop     AT %IX0.2 : BOOL;
    belt_drive     AT %QX0.0 : BOOL;
    jam_this_run : BOOL := FALSE;
    running       : BOOL := FALSE;
  END_VAR

  IF run_stop THEN
    running := FALSE;
    jam_this_run := FALSE;
  ELSIF run_start AND NOT jam_this_run THEN
    running := TRUE;
  END_IF;

  IF jam_detected THEN
    jam_this_run := TRUE;
  END_IF;

  IF jam_detected OR jam_this_run OR NOT running THEN
    belt_drive := FALSE;
  ELSE
    belt_drive := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : conveyor_control;
  END_RESOURCE
END_CONFIGURATION
