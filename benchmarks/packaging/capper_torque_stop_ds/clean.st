(* ============================================================
   Capper torque‑fault stop
   Safety: If torque_high is TRUE, capper_run is forced FALSE
   and fault_latch sets until manual_reset.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM capper
  VAR
    torque_high  AT %IX0.0 : BOOL;
    manual_reset AT %IX0.1 : BOOL;
    capper_req   AT %IX0.2 : BOOL;
    capper_run   AT %QX0.0 : BOOL;
    fault_latch  AT %QX0.1 : BOOL;
    latch        : BOOL;
  END_VAR

  IF torque_high THEN
    latch := TRUE;
  ELSIF manual_reset THEN
    latch := FALSE;
  END_IF;

  fault_latch := latch;
  capper_run := capper_req AND NOT latch;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : capper;
  END_RESOURCE
END_CONFIGURATION
