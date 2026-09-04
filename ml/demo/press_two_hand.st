(* ============================================================
   Hydraulic press two-hand safety control : demo program, not in
   the suite.
   Safety intent: the press ram must never descend unless both
   palm buttons are pressed simultaneously (prevents one-handed
   operation while the other hand is in the die area).
   ============================================================ *)
PROGRAM press_control
  VAR
    palm_left  AT %IX0.0 : BOOL;
    palm_right AT %IX0.1 : BOOL;
    light_curtain_clear AT %IX0.2 : BOOL;
    ram_descend AT %QX0.0 : BOOL;
  END_VAR

  IF palm_left AND palm_right AND light_curtain_clear THEN
    ram_descend := TRUE;
  ELSE
    ram_descend := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : press_control;
  END_RESOURCE
END_CONFIGURATION
