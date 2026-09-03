(* ============================================================
   Three-pump station lockout : demo program, not in the suite.
   Safety intent: at most one of the three pumps may run at a time
   (shared discharge header cannot take combined flow).
   ============================================================ *)
PROGRAM three_pump
  VAR
    req_a AT %IX0.0 : BOOL;
    req_b AT %IX0.1 : BOOL;
    req_c AT %IX0.2 : BOOL;
    pump_a AT %QX0.0 : BOOL;
    pump_b AT %QX0.1 : BOOL;
    pump_c AT %QX0.2 : BOOL;
  END_VAR

  IF req_a THEN
    pump_a := TRUE;
    pump_b := FALSE;
    pump_c := FALSE;
  ELSIF req_b THEN
    pump_a := FALSE;
    pump_b := TRUE;
    pump_c := FALSE;
  ELSIF req_c THEN
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := TRUE;
  ELSE
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : three_pump;
  END_RESOURCE
END_CONFIGURATION
