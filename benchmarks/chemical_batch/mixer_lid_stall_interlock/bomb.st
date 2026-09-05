(* ============================================================
   Batch mixer lid/stall dual interlock : BOMB variant.
   Seeded defect: the heater dispatch was reordered to check
   heat_request before agitator_stalled, so a pending heat
   request wins the branch the scan the stall is detected, and
   ELSIF agitator_stalled becomes unreachable once heat_request
   is true.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM mixer_control
  VAR
    lid_open        AT %IX0.0 : BOOL;
    agitator_stalled AT %IX0.1 : BOOL;
    run_request     AT %IX0.2 : BOOL;
    heat_request    AT %IX0.3 : BOOL;
    agitator_on      AT %QX0.0 : BOOL;
    heater_on        AT %QX0.1 : BOOL;
  END_VAR

  IF lid_open THEN
    agitator_on := FALSE;
  ELSIF run_request THEN
    agitator_on := TRUE;
  ELSE
    agitator_on := FALSE;
  END_IF;

  IF heat_request THEN
    heater_on := TRUE;
  ELSIF agitator_stalled THEN
    heater_on := FALSE;
  ELSE
    heater_on := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : mixer_control;
  END_RESOURCE
END_CONFIGURATION
