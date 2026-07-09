(* ============================================================
   S3 - Pressure relief with HMI reporting : CLEAN baseline
   A relief valve opens on over-pressure; the value reported to
   the HMI/SCADA must always equal the real valve command
   (no spoofing). Safety/integrity invariant:
        reported_open  ==  valve_open
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM relief
  VAR
    over_press AT %IX0.0 : BOOL;   (* pressure switch *)
    valve_open    AT %QX0.0 : BOOL; (* real actuator command  *)
    reported_open AT %QX0.1 : BOOL; (* value sent to the HMI  *)
  END_VAR

  IF over_press THEN
    valve_open := TRUE;
  ELSE
    valve_open := FALSE;
  END_IF;

  (* Honest reporting: HMI mirrors the real command *)
  reported_open := valve_open;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : relief;
  END_RESOURCE
END_CONFIGURATION
