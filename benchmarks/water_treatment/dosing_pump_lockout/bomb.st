(* ============================================================
   Water treatment dosing pump fault lockout : BOMB variant.
   Seeded defect: the pump dispatch was reordered to check
   start_cmd before dry_run_fault, so a held start command wins
   the branch the scan the dry-run fault is set, and the fault
   lockout only takes effect in scans where start_cmd happens to
   be false.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM dosing_control
  VAR
    level_low     AT %IX0.0 : BOOL;
    start_cmd     AT %IX0.1 : BOOL;
    ack_fault     AT %IX0.2 : BOOL;
    dosing_pump     AT %QX0.0 : BOOL;
    dry_run_fault : BOOL := FALSE;
  END_VAR

  IF dosing_pump AND level_low THEN
    dry_run_fault := TRUE;
  ELSIF ack_fault THEN
    dry_run_fault := FALSE;
  END_IF;

  IF level_low THEN
    dosing_pump := FALSE;
  ELSIF start_cmd THEN
    dosing_pump := TRUE;
  ELSIF dry_run_fault THEN
    dosing_pump := FALSE;
  ELSE
    dosing_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dosing_control;
  END_RESOURCE
END_CONFIGURATION
