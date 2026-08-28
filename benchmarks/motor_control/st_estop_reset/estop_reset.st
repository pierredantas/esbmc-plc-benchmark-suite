(* estop_reset: emergency stop with a monitored manual reset.
   Structured Text rendering of g_estop_reset.

   ISO 13849-1 asks for the safety function to be restored by a separate manual
   action. The reset is taken on the falling edge of the button, so a reset that
   is bridged or held down cannot restore anything. EStop breaks the drive rung
   directly as well as through Safe, the way a hardwired stop breaks the coil
   circuit rather than waiting on the program. *)
PROGRAM drive
  VAR_INPUT
    EStop : BOOL;
    Reset : BOOL;
    Start : BOOL;
  END_VAR
  VAR_OUTPUT
    ResetEdge  : BOOL;
    Safe       : BOOL;
    Run        : BOOL;
    Reset_prev : BOOL;
  END_VAR

  ResetEdge := Reset_prev AND NOT Reset;
  Safe := (Safe OR ResetEdge) AND NOT EStop;
  Run := Safe AND Start AND NOT EStop;
  Reset_prev := Reset;
END_PROGRAM
