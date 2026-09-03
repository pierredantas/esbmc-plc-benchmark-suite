(* ============================================================
   Pump / pressure-relief valve : demo program, not in the
   benchmark suite.
   Safety intent: the feed pump must never run while the relief
   valve is closed (dead-heading risk), and the relief valve must
   never be closed while the high-pressure alarm is active.
   ============================================================ *)
PROGRAM pump_relief
  VAR
    hi_pressure_alarm AT %IX0.0 : BOOL;  (* pressure above safe limit *)
    pump_request      AT %IX0.1 : BOOL;
    manual_close       AT %IX0.2 : BOOL;
    pump_run          AT %QX0.0 : BOOL;
    relief_valve_open AT %QX0.1 : BOOL;
  END_VAR

  IF hi_pressure_alarm THEN
    relief_valve_open := TRUE;
  ELSIF manual_close AND NOT hi_pressure_alarm THEN
    relief_valve_open := FALSE;
  END_IF;

  IF relief_valve_open AND pump_request THEN
    pump_run := TRUE;
  ELSE
    pump_run := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : pump_relief;
  END_RESOURCE
END_CONFIGURATION
