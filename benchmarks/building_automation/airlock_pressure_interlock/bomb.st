(* ============================================================
   Cleanroom airlock door interlock : BOMB variant.
   Seeded defect: the two door branches were split from an
   IF/ELSIF chain into independent IF statements, apparently to
   let each door respond to its own request without waiting on the
   other's condition, and the "NOT outer_request" / "NOT
   inner_request" cross-checks were dropped as "redundant" now that
   cycle_busy already gates both. Both requests arriving in the
   same scan (a plausible double-badge event during shift change)
   unlocks both doors together, breaking the pressure interlock.
   Expected verdict: VIOLATION of P1 (witness: P2).
   ============================================================ *)
PROGRAM airlock_control
  VAR
    inner_request AT %IX0.0 : BOOL;
    outer_request AT %IX0.1 : BOOL;
    cycle_busy    AT %IX0.2 : BOOL;
    inner_unlocked AT %QX0.0 : BOOL;
    outer_unlocked AT %QX0.1 : BOOL;
  END_VAR

  IF NOT cycle_busy AND inner_request THEN
    inner_unlocked := TRUE;
  ELSE
    inner_unlocked := FALSE;
  END_IF;

  IF NOT cycle_busy AND outer_request THEN
    outer_unlocked := TRUE;
  ELSE
    outer_unlocked := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : airlock_control;
  END_RESOURCE
END_CONFIGURATION
