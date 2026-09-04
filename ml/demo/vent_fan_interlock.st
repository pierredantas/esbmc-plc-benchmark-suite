(* ============================================================
   Paint booth vent fan / spray gun interlock : demo program, not
   in the suite.
   Safety intent: the spray gun trigger must be blocked whenever
   the exhaust fan is NOT running (solvent vapour must always be
   extracted while spraying).
   ============================================================ *)
PROGRAM booth_interlock
  VAR
    fan_running   AT %IX0.0 : BOOL;
    trigger_pull  AT %IX0.1 : BOOL;
    gun_enabled   AT %QX0.0 : BOOL;
  END_VAR

  IF NOT fan_running THEN
    gun_enabled := FALSE;
  ELSE
    gun_enabled := trigger_pull;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : booth_interlock;
  END_RESOURCE
END_CONFIGURATION
