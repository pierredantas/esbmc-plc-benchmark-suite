(* ============================================================
   Fire damper – AHU shutdown interlock
   Safety: fan_on is allowed only if damper_open AND no fire_alarm.
   Expected ESBMC-PLC+ verdict: SAFE.
   ============================================================ *)
PROGRAM ahu_control
  VAR
    fan_req      AT %IX0.0 : BOOL;   (* operator request *)
    damper_open  AT %IX0.1 : BOOL;   (* damper open feedback *)
    fire_alarm   AT %IX0.2 : BOOL;
    fan_on       AT %QX0.0 : BOOL;
  END_VAR

  fan_on := fan_req AND damper_open AND NOT fire_alarm;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : ahu_control;
  END_RESOURCE
END_CONFIGURATION
