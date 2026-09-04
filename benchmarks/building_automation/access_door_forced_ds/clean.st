(* ============================================================
   Access‑control door forced‑open alarm
   Safety: If door_forced is TRUE, alarm_latch sets and remains
   until manual_reset.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM door_alarm
  VAR
    door_forced  AT %IX0.0 : BOOL;
    manual_reset AT %IX0.1 : BOOL;
    alarm_latch  AT %QX0.0 : BOOL;
    lock_hold    AT %QX0.1 : BOOL;   (* door held locked *)
    latch        : BOOL;
  END_VAR

  IF door_forced THEN
    latch := TRUE;
  ELSIF manual_reset THEN
    latch := FALSE;
  END_IF;

  alarm_latch := latch;
  lock_hold := latch;   (* door held locked until reset *)
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : door_alarm;
  END_RESOURCE
END_CONFIGURATION
