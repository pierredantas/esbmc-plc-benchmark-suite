(* ============================================================
   Water treatment dosing pump fault lockout.
   Safety intent: the dosing pump must never run while the tank
   level is below the low-level cutoff. If the pump ever runs dry
   (commanded on while below cutoff), any subsequent start command
   is ignored and the pump stays off, until an operator
   acknowledges the fault, regardless of how many times start is
   pressed afterward.
   ============================================================ *)
PROGRAM dosing_control
  VAR
    level_low     AT %IX0.0 : BOOL;
    start_cmd     AT %IX0.1 : BOOL;
    ack_fault     AT %IX0.2 : BOOL;
    dosing_pump     AT %QX0.0 : BOOL;
    dry_run_fault : BOOL := FALSE;
  END_VAR

  IF dosing_pump AND level_low THEN
    dry_run_fault := TRUE;
  ELSIF ack_fault THEN
    dry_run_fault := FALSE;
  END_IF;

  IF dry_run_fault OR level_low THEN
    dosing_pump := FALSE;
  ELSIF start_cmd THEN
    dosing_pump := TRUE;
  ELSE
    dosing_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dosing_control;
  END_RESOURCE
END_CONFIGURATION
