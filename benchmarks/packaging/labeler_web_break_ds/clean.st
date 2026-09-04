(* ============================================================
   Labeler web‑break detection
   Safety: If web_break is TRUE, labeler_run is forced FALSE
   and fault_latch sets until manual_reset.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM labeler
  VAR
    web_break    AT %IX0.0 : BOOL;
    manual_reset AT %IX0.1 : BOOL;
    labeler_req  AT %IX0.2 : BOOL;
    labeler_run  AT %QX0.0 : BOOL;
    fault_latch  AT %QX0.1 : BOOL;
    latch        : BOOL;
  END_VAR

  IF web_break THEN
    latch := TRUE;
  ELSIF manual_reset THEN
    latch := FALSE;
  END_IF;

  fault_latch := latch;
  labeler_run := labeler_req AND NOT latch;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : labeler;
  END_RESOURCE
END_CONFIGURATION
