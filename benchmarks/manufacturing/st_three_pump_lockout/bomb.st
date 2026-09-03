(* ============================================================
   Three-pump station lockout : BOMB variant
   Safety: at most one of pump_a, pump_b, pump_c may run at a
   time (shared discharge header cannot take combined flow).
   Seeded defect: a maintenance override lets req_a and req_b
   both drive their pumps without clearing each other, so P1 is
   violated (pairwise, not just 3-way, exclusion breaks) while
   pump_c stays correctly interlocked out.
   Expected verdict: VIOLATION of P1.
   ============================================================ *)
PROGRAM three_pump
  VAR
    req_a AT %IX0.0 : BOOL;
    req_b AT %IX0.1 : BOOL;
    req_c AT %IX0.2 : BOOL;
    maint AT %IX0.3 : BOOL;
    pump_a AT %QX0.0 : BOOL;
    pump_b AT %QX0.1 : BOOL;
    pump_c AT %QX0.2 : BOOL;
  END_VAR

  IF maint THEN
    pump_a := req_a;
    pump_b := req_b;
    pump_c := FALSE;
  ELSIF req_a THEN
    pump_a := TRUE;
    pump_b := FALSE;
    pump_c := FALSE;
  ELSIF req_b THEN
    pump_a := FALSE;
    pump_b := TRUE;
    pump_c := FALSE;
  ELSIF req_c THEN
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := TRUE;
  ELSE
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : three_pump;
  END_RESOURCE
END_CONFIGURATION
