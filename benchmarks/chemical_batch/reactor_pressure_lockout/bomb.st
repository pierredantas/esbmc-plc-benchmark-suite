(* ============================================================
   Chemical reactor overpressure lockout : BOMB variant.
   Seeded defect: the pump dispatch was reordered to check
   feed_request before the fault/pressure lockout, so a pending
   feed request wins the branch the scan the fault is set (and
   remains commandable afterwards, since ELSIF fault_flag OR
   pressure_high is now unreachable once feed_request is true).
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM reactor_control
  VAR
    pressure_high  AT %IX0.0 : BOOL;
    clear_fault    AT %IX0.1 : BOOL;
    feed_request   AT %IX0.2 : BOOL;
    feed_pump        AT %QX0.0 : BOOL;
    fault_flag : BOOL := FALSE;
  END_VAR

  IF pressure_high THEN
    fault_flag := TRUE;
  ELSIF clear_fault THEN
    fault_flag := FALSE;
  END_IF;

  IF pressure_high THEN
    feed_pump := FALSE;
  ELSIF feed_request THEN
    feed_pump := TRUE;
  ELSIF fault_flag THEN
    feed_pump := FALSE;
  ELSE
    feed_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : reactor_control;
  END_RESOURCE
END_CONFIGURATION
