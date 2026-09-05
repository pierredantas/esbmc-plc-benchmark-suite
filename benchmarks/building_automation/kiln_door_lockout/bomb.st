(* ============================================================
   Industrial kiln door safety latch : BOMB variant.
   Seeded defect: the heater dispatch was "optimised" to check
   heat_request before the fault latch, so a heat request already
   pending when the fault latches wins the branch and the heater
   stays on into the very scan the fault is set (and remains
   commandable afterwards, since ELSIF door_fault_latched is now
   unreachable once heat_request is true).
   Expected verdict: VIOLATION of P2.
   ============================================================ *)
PROGRAM kiln_control
  VAR
    door_open     AT %IX0.0 : BOOL;
    heat_request  AT %IX0.1 : BOOL;
    reset_button  AT %IX0.2 : BOOL;
    heater_element AT %QX0.0 : BOOL;
    door_fault_latched : BOOL := FALSE;
  END_VAR

  IF door_open THEN
    door_fault_latched := TRUE;
  ELSIF reset_button THEN
    door_fault_latched := FALSE;
  END_IF;

  IF door_open THEN
    heater_element := FALSE;
  ELSIF heat_request THEN
    heater_element := TRUE;
  ELSIF door_fault_latched THEN
    heater_element := FALSE;
  ELSE
    heater_element := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : kiln_control;
  END_RESOURCE
END_CONFIGURATION
