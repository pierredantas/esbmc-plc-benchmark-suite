(* ============================================================
   Case sealer jam lockout
   Safety: If jam_detected is TRUE, conveyor_run is forced FALSE
   and jam_latch stays ON until manual_reset.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM case_sealer
  VAR
    jam_detected AT %IX0.0 : BOOL;
    manual_reset AT %IX0.1 : BOOL;
    conveyor_req AT %IX0.2 : BOOL;
    conveyor_run AT %QX0.0 : BOOL;
    jam_latch    AT %QX0.1 : BOOL;
    latch        : BOOL;
  END_VAR

  IF jam_detected THEN
    latch := TRUE;
  ELSIF manual_reset THEN
    latch := FALSE;
  END_IF;

  jam_latch := latch;
  conveyor_run := conveyor_req AND NOT latch;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : case_sealer;
  END_RESOURCE
END_CONFIGURATION
