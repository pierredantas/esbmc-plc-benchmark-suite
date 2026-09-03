(* ============================================================
   Gas burner ignition sequence : demo program, not in the suite.
   Safety intent: the gas valve must never open unless the purge
   fan has been confirmed running, and the spark igniter must
   never be energised while the gas valve is closed (no fuel to
   ignite, wasted spark risk is secondary to the interlock logic
   itself being sound).
   ============================================================ *)
PROGRAM burner_seq
  VAR
    purge_fan_ok  AT %IX0.0 : BOOL;
    start_request AT %IX0.1 : BOOL;
    flame_proven  AT %IX0.2 : BOOL;
    gas_valve     AT %QX0.0 : BOOL;
    igniter       AT %QX0.1 : BOOL;
  END_VAR

  IF start_request AND purge_fan_ok THEN
    gas_valve := TRUE;
  ELSE
    gas_valve := FALSE;
  END_IF;

  IF gas_valve AND NOT flame_proven THEN
    igniter := TRUE;
  ELSE
    igniter := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : burner_seq;
  END_RESOURCE
END_CONFIGURATION
