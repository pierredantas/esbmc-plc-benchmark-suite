(* ============================================================
   Substation breaker closing-coil dual interlock.
   Safety intent: the closing coil must never energise while the
   earthing switch is closed (closing onto an earthed line is
   catastrophic); separately, the closing coil must never
   energise while a protection trip is latched (closing into a
   known fault re-energises it). Two independent guard
   conditions on the same output, neither derived from the
   other.
   ============================================================ *)
PROGRAM breaker_control
  VAR
    earth_switch_closed AT %IX0.0 : BOOL;
    trip_latched        AT %IX0.1 : BOOL;
    close_request       AT %IX0.2 : BOOL;
    closing_coil          AT %QX0.0 : BOOL;
  END_VAR

  IF earth_switch_closed OR trip_latched THEN
    closing_coil := FALSE;
  ELSIF close_request THEN
    closing_coil := TRUE;
  ELSE
    closing_coil := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : breaker_control;
  END_RESOURCE
END_CONFIGURATION
