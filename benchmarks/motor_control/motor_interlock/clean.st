(* ============================================================
   S2 - Two-motor interlock : CLEAN baseline
   Safety: Motor_A and Motor_B (e.g. forward/reverse contactors)
   must never be energised simultaneously.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM drive
  VAR
    fwd  AT %IX0.0 : BOOL;   (* request forward *)
    rev  AT %IX0.1 : BOOL;   (* request reverse *)
    maint AT %IX0.2 : BOOL;  (* maintenance key *)
    Motor_A AT %QX0.0 : BOOL;
    Motor_B AT %QX0.1 : BOOL;
  END_VAR

  Motor_A := FALSE;
  Motor_B := FALSE;

  (* Hard interlock: reverse request always wins, never both *)
  IF fwd AND NOT rev THEN
    Motor_A := TRUE;
  ELSIF rev THEN
    Motor_B := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : drive;
  END_RESOURCE
END_CONFIGURATION
