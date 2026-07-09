(* ============================================================
   S1 - Tank level control : BOMBED variant
   Govil et al. LLB taxonomy:
     Trigger : LOCAL, counter/time-based (scan_cnt >= THRESHOLD)
     Payload : ACTUATOR MANIPULATION (bypass the full-tank
               interlock so the pump keeps running -> overflow)
     Stealth : dormant for THRESHOLD scans; passes inspection/
               simulation runs that are shorter than THRESHOLD.
   Detection property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION; the counterexample
   trace recovers the detonation trigger (scan_cnt reaching
   THRESHOLD), i.e. trigger SYNTHESIS.
   THRESHOLD kept small (50) for a fast demo; see S5 for the
   parametric scalability sweep vs nuXmv BDD.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;        (* dormant time fuse          *)
    armed      : BOOL := FALSE;     (* set once fuse expires      *)
  END_VAR

  (* --- LLB fuse: increments silently every scan --- *)
  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 50 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  (* --- LLB payload: interlock is gated by NOT armed --- *)
  (* Before detonation it behaves exactly like clean.st.    *)
  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
