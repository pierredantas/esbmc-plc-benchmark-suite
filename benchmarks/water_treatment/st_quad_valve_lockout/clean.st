(* ============================================================
   Four-way header selector valve : CLEAN baseline
   Safety: exactly one (or none) of the four outlet valves may be
   open at a time; the shared header cannot supply two lines at
   once without cross-contaminating batches.
   Expected verdict: SAFE.
   ============================================================ *)
PROGRAM quad_valve
  VAR
    sel_1 AT %IX0.0 : BOOL;
    sel_2 AT %IX0.1 : BOOL;
    sel_3 AT %IX0.2 : BOOL;
    sel_4 AT %IX0.3 : BOOL;
    valve_1 AT %QX0.0 : BOOL;
    valve_2 AT %QX0.1 : BOOL;
    valve_3 AT %QX0.2 : BOOL;
    valve_4 AT %QX0.3 : BOOL;
  END_VAR

  valve_1 := FALSE;
  valve_2 := FALSE;
  valve_3 := FALSE;
  valve_4 := FALSE;

  IF sel_1 THEN
    valve_1 := TRUE;
  ELSIF sel_2 THEN
    valve_2 := TRUE;
  ELSIF sel_3 THEN
    valve_3 := TRUE;
  ELSIF sel_4 THEN
    valve_4 := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : quad_valve;
  END_RESOURCE
END_CONFIGURATION
