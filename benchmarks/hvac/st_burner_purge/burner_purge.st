(* burner_purge: purge, light-off and lockout for a gas burner.
   Structured Text rendering of g_burner_purge.

   EN 298 fixes the order: fan first, main gas only after the purge has completed
   and the flame is proven. The lockout latches on a flame fault and needs the
   reset button, because a burner that retries on its own fills the chamber. *)
PROGRAM burner
  VAR_INPUT
    CallForHeat : BOOL;
    PurgeDone   : BOOL;
    FlameProven : BOOL;
    FlameFail   : BOOL;
    ResetBtn    : BOOL;
  END_VAR
  VAR_OUTPUT
    Fan       : BOOL;
    Lockout   : BOOL;
    Pilot     : BOOL;
    MainValve : BOOL;
  END_VAR

  Fan := CallForHeat;
  Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
  Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
  MainValve := CallForHeat AND PurgeDone AND FlameProven AND NOT Lockout;
END_PROGRAM
