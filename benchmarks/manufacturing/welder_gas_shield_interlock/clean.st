(* ============================================================
   MIG welder shielding-gas interlock : demo program, not in the
   suite.
   Safety intent: the arc (weld current) must never strike unless
   BOTH the shielding-gas flow is confirmed AND the torch trigger
   is pulled; the arc must also be blocked whenever the gas flow
   sensor drops out mid-weld.
   ============================================================ *)
PROGRAM welder_control
  VAR
    gas_flow_ok   AT %IX0.0 : BOOL;
    trigger_pull  AT %IX0.1 : BOOL;
    arc_on        AT %QX0.0 : BOOL;
  END_VAR

  IF NOT gas_flow_ok THEN
    arc_on := FALSE;
  ELSIF trigger_pull AND gas_flow_ok THEN
    arc_on := TRUE;
  ELSE
    arc_on := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : welder_control;
  END_RESOURCE
END_CONFIGURATION
