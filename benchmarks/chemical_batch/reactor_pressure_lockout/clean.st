(* ============================================================
   Chemical reactor overpressure lockout.
   Safety intent: the feed pump must never run while reactor
   pressure is above the safe limit. If pressure ever exceeds the
   safe limit, the reactor is considered faulted and the feed
   pump remains shut down, even after pressure falls back into
   range, until an operator manually clears the fault.
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

  IF fault_flag OR pressure_high THEN
    feed_pump := FALSE;
  ELSIF feed_request THEN
    feed_pump := TRUE;
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
