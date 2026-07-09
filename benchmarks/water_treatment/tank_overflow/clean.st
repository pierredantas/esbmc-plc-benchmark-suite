(* ============================================================
   S1 - Tank level control : CLEAN (benign) baseline
   Domain: water/chemical tank fill with high-level interlock.
   Safety: the pump must never run while the tank is full.
   Govil et al. taxonomy: N/A (this is the benign host program).
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;   (* sensor: tank full          *)
    start      AT %IX0.1 : BOOL;   (* operator: request fill     *)
    pump       AT %QX0.0 : BOOL;   (* actuator: fill pump        *)
  END_VAR

  (* Fill while requested and not yet full *)
  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  (* Safety interlock: full tank always stops the pump *)
  IF level_high THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
