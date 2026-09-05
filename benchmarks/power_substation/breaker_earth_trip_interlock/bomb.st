(* ============================================================
   Substation breaker closing-coil dual interlock : BOMB variant.
   Seeded defect: the combined guard was reordered to give
   close_request priority over the protection-trip check (kept
   ahead only of earth_switch_closed), so a held close_request
   energises the coil even while a protection trip is latched;
   the earthing-switch guard is untouched and still holds.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM breaker_control
  VAR
    earth_switch_closed AT %IX0.0 : BOOL;
    trip_latched        AT %IX0.1 : BOOL;
    close_request       AT %IX0.2 : BOOL;
    closing_coil          AT %QX0.0 : BOOL;
  END_VAR

  IF earth_switch_closed THEN
    closing_coil := FALSE;
  ELSIF close_request THEN
    closing_coil := TRUE;
  ELSIF trip_latched THEN
    closing_coil := FALSE;
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
