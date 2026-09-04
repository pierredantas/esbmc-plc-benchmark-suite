(* ============================================================
   Palletizer light‑curtain interlock
   Safety: palletizer_run is allowed only if curtain_clear is TRUE.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM palletizer
  VAR
    curtain_broken AT %IX0.0 : BOOL;
    palletizer_req AT %IX0.1 : BOOL;
    palletizer_run AT %QX0.0 : BOOL;
  END_VAR

  palletizer_run := palletizer_req AND NOT curtain_broken;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : palletizer;
  END_RESOURCE
END_CONFIGURATION
