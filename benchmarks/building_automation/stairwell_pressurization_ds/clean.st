(* ============================================================
   Stairwell pressurization fan control
   Safety: fan_on = fire_alarm AND pressure_low. Fan is not to
   run without fire alarm (prevents unnecessary noise/energy).
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM stairwell_fan
  VAR
    fire_alarm   AT %IX0.0 : BOOL;
    pressure_low AT %IX0.1 : BOOL;   (* pressure below setpoint *)
    fan_on       AT %QX0.0 : BOOL;
  END_VAR

  fan_on := fire_alarm AND pressure_low;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : stairwell_fan;
  END_RESOURCE
END_CONFIGURATION
