(* ============================================================
   Reactor overpressure trip, 2-out-of-3 voting : demo program,
   not in the suite.
   Safety intent: the trip valve must open whenever at least two
   of the three independent pressure switches agree the vessel is
   over-pressured (2oo3 voting rejects a single sensor fault).
   ============================================================ *)
PROGRAM trip_2oo3
  VAR
    ps1 AT %IX0.0 : BOOL;
    ps2 AT %IX0.1 : BOOL;
    ps3 AT %IX0.2 : BOOL;
    trip_valve AT %QX0.0 : BOOL;
  END_VAR

  IF (ps1 AND ps2) OR (ps1 AND ps3) OR (ps2 AND ps3) THEN
    trip_valve := TRUE;
  ELSE
    trip_valve := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : trip_2oo3;
  END_RESOURCE
END_CONFIGURATION
