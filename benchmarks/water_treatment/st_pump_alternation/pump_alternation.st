(* pump_alternation: duty-standby pump station.
   Structured Text rendering of g_pump_alternation.

   One pump runs at a time so the standby stays available. Duty changes hands
   each time the well empties, which is what keeps the second pump from sitting
   unstarted for a season. *)
PROGRAM station
  VAR_INPUT
    LevelHigh : BOOL;
    LevelLow  : BOOL;
  END_VAR
  VAR_OUTPUT
    Call  : BOOL;
    Duty  : BOOL;
    PumpA : BOOL;
    PumpB : BOOL;
  END_VAR

  Call := (Call OR LevelHigh) AND NOT LevelLow;
  Duty := (Duty AND NOT LevelLow) OR (NOT Duty AND LevelLow);
  PumpA := Call AND NOT Duty;
  PumpB := Call AND Duty;
END_PROGRAM
