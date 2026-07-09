(* ============================================================
   S2 - Two-motor interlock : BOMBED variant
   Govil et al. LLB taxonomy:
     Trigger : LOCAL, input-pattern "secret knock"
               (fwd AND rev AND maint -- a combination an
                operator would never assert intentionally)
     Payload : ACTUATOR MANIPULATION (energise BOTH motors,
               bypassing the forward/reverse interlock ->
               contactor short / mechanical damage)
     Stealth : the knock is a measure-zero input pattern, never
               exercised by normal operation or random testing.
   Detection property: mutual_exclusion [Motor_A, Motor_B] /
                       reachability "Motor_A AND Motor_B".
   Expected ESBMC-PLC+ verdict: VIOLATION; counterexample is the
   exact knock pattern (trigger synthesis).
   ============================================================ *)
PROGRAM drive
  VAR
    fwd  AT %IX0.0 : BOOL;
    rev  AT %IX0.1 : BOOL;
    maint AT %IX0.2 : BOOL;
    Motor_A AT %QX0.0 : BOOL;
    Motor_B AT %QX0.1 : BOOL;
  END_VAR

  Motor_A := FALSE;
  Motor_B := FALSE;

  IF fwd AND NOT rev THEN
    Motor_A := TRUE;
  ELSIF rev THEN
    Motor_B := TRUE;
  END_IF;

  (* --- LLB: secret-knock override of the interlock --- *)
  IF fwd AND rev AND maint THEN
    Motor_A := TRUE;
    Motor_B := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : drive;
  END_RESOURCE
END_CONFIGURATION
