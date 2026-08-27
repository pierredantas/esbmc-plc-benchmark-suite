(* seal_in: self-holding (seal-in) coil with stop.
   Structured Text rendering of ld_seal_in / g_seal_in.
   Run := (Start OR Run) AND NOT Stop *)
PROGRAM drive
  VAR_INPUT
    Start : BOOL;
    Stop  : BOOL;
  END_VAR
  VAR_OUTPUT
    Run : BOOL;
  END_VAR

  Run := (Start OR Run) AND NOT Stop;
END_PROGRAM
