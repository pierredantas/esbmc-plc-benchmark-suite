(* ============================================================
   Dual immersion heater : demo program, not in the suite.
   Safety intent: heater_A and heater_B must never be energised
   together (shared circuit breaker is rated for one at a time).
   ============================================================ *)
PROGRAM dual_heater
  VAR
    demand_a  AT %IX0.0 : BOOL;
    demand_b  AT %IX0.1 : BOOL;
    heater_A  AT %QX0.0 : BOOL;
    heater_B  AT %QX0.1 : BOOL;
  END_VAR

  IF demand_a THEN
    heater_A := TRUE;
    heater_B := FALSE;
  ELSIF demand_b THEN
    heater_A := FALSE;
    heater_B := TRUE;
  ELSE
    heater_A := FALSE;
    heater_B := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dual_heater;
  END_RESOURCE
END_CONFIGURATION
