(* ============================================================
   Crane hoist overload cutoff : demo program, not in the suite.
   Safety intent: the hoist motor must never raise the load while
   the overload sensor is tripped, regardless of the operator's
   raise command.
   ============================================================ *)
PROGRAM hoist_control
  VAR
    overload_tripped AT %IX0.0 : BOOL;
    raise_command    AT %IX0.1 : BOOL;
    lower_command    AT %IX0.2 : BOOL;
    hoist_raise       AT %QX0.0 : BOOL;
    hoist_lower       AT %QX0.1 : BOOL;
  END_VAR

  IF overload_tripped THEN
    hoist_raise := FALSE;
  ELSIF raise_command AND NOT lower_command THEN
    hoist_raise := TRUE;
  ELSE
    hoist_raise := FALSE;
  END_IF;

  hoist_lower := lower_command AND NOT raise_command;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : hoist_control;
  END_RESOURCE
END_CONFIGURATION
