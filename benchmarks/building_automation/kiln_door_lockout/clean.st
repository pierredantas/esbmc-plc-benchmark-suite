(* ============================================================
   Industrial kiln door safety latch : demo program, not in the
   suite.
   Safety intent: the heating element must never be energised
   while the kiln door is open; once the door has been opened
   during a heat cycle, the element stays locked out even after
   the door closes again, until an operator explicitly resets it.
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

  IF door_fault_latched OR door_open THEN
    heater_element := FALSE;
  ELSIF heat_request THEN
    heater_element := TRUE;
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
