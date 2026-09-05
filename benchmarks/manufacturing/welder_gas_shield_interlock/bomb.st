(* ============================================================
   MIG welder shielding-gas interlock : BOMB variant.
   Seeded defect: the gas-dropout check and the trigger check were
   split into independent IF statements (rather than IF/ELSIF),
   apparently to let a maintenance mode re-arm the arc within the
   same scan. Because both IFs can now write arc_on independently,
   the trigger branch, which never re-checks gas_flow_ok, wins
   whenever it executes after the dropout branch.
   Expected verdict: VIOLATION of P1 (witness: P2).
   ============================================================ *)
PROGRAM welder_control
  VAR
    gas_flow_ok   AT %IX0.0 : BOOL;
    trigger_pull  AT %IX0.1 : BOOL;
    arc_on        AT %QX0.0 : BOOL;
  END_VAR

  IF NOT gas_flow_ok THEN
    arc_on := FALSE;
  END_IF;

  IF trigger_pull THEN
    arc_on := TRUE;
  ELSE
    arc_on := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : welder_control;
  END_RESOURCE
END_CONFIGURATION
