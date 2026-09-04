(* ============================================================
   Stairwell Pressurization : CLEAN baseline
   Safety: The fire alarm runs the pressurization fan, but
   a high static pressure switch must trip the fan to prevent
   ductwork rupture, regardless of the fire alarm state.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM stairwell
  VAR
    fire_alarm AT %IX0.0 : BOOL;
    manual_run AT %IX0.1 : BOOL;
    high_pressure AT %IX0.2 : BOOL;
    fan_run AT %QX0.0 : BOOL;
  END_VAR

  fan_run := (fire_alarm OR manual_run) AND NOT high_pressure;
END_PROGRAM
