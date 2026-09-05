(* ============================================================
   Cleanroom airlock door interlock : demo program, not in the
   suite.
   Safety intent: the inner and outer airlock doors must never
   both be unlocked at the same time (maintains pressure
   differential and contamination control).
   ============================================================ *)
PROGRAM airlock_control
  VAR
    inner_request AT %IX0.0 : BOOL;
    outer_request AT %IX0.1 : BOOL;
    cycle_busy    AT %IX0.2 : BOOL;
    inner_unlocked AT %QX0.0 : BOOL;
    outer_unlocked AT %QX0.1 : BOOL;
  END_VAR

  IF NOT cycle_busy AND inner_request AND NOT outer_request THEN
    inner_unlocked := TRUE;
    outer_unlocked := FALSE;
  ELSIF NOT cycle_busy AND outer_request AND NOT inner_request THEN
    inner_unlocked := FALSE;
    outer_unlocked := TRUE;
  ELSE
    inner_unlocked := FALSE;
    outer_unlocked := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : airlock_control;
  END_RESOURCE
END_CONFIGURATION
