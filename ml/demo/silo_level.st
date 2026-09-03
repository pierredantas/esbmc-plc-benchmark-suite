(* ============================================================
   Grain silo fill control : demo program, not in the suite.
   Safety intent: the inlet auger must never run while the
   high-level sensor is tripped (overfill/structural risk), and
   the outlet gate must never open while the inlet auger runs
   (product would short-circuit straight through).
   ============================================================ *)
PROGRAM silo_fill
  VAR
    high_level    AT %IX0.0 : BOOL;
    fill_request  AT %IX0.1 : BOOL;
    empty_request AT %IX0.2 : BOOL;
    inlet_auger   AT %QX0.0 : BOOL;
    outlet_gate   AT %QX0.1 : BOOL;
  END_VAR

  IF high_level THEN
    inlet_auger := FALSE;
  ELSIF fill_request AND NOT empty_request THEN
    inlet_auger := TRUE;
  END_IF;

  IF inlet_auger THEN
    outlet_gate := FALSE;
  ELSIF empty_request THEN
    outlet_gate := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : silo_fill;
  END_RESOURCE
END_CONFIGURATION
