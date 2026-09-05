(* ============================================================
   Packaging conveyor jam lockout : BOMB variant.
   Seeded defect: the belt drive dispatch was reordered to check
   run_start priority before jam_this_run, on the reasoning that
   "a fresh run_start means the operator already inspected the
   line" — so once running is TRUE the jam_this_run latch is
   still set but no longer consulted by the belt output.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM conveyor_control
  VAR
    jam_detected AT %IX0.0 : BOOL;
    run_start    AT %IX0.1 : BOOL;
    run_stop     AT %IX0.2 : BOOL;
    belt_drive     AT %QX0.0 : BOOL;
    jam_this_run : BOOL := FALSE;
    running       : BOOL := FALSE;
  END_VAR

  IF run_stop THEN
    running := FALSE;
    jam_this_run := FALSE;
  ELSIF run_start AND NOT jam_this_run THEN
    running := TRUE;
  END_IF;

  IF jam_detected THEN
    jam_this_run := TRUE;
  END_IF;

  IF jam_detected THEN
    belt_drive := FALSE;
  ELSIF running THEN
    belt_drive := TRUE;
  ELSE
    belt_drive := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : conveyor_control;
  END_RESOURCE
END_CONFIGURATION
