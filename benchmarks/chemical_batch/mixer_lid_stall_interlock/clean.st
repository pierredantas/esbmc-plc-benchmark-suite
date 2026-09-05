(* ============================================================
   Batch mixer lid/stall dual interlock.
   Safety intent: the agitator must never run while the vessel
   lid is open; separately, the heater must never run while the
   agitator is stalled (a stalled rotor in a heated vessel risks
   local scorching and pressure buildup). Two independent
   hazards on two different actuators, sharing no internal state.
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

  IF agitator_stalled THEN
    heater_on := FALSE;
  ELSIF heat_request THEN
    heater_on := TRUE;
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
