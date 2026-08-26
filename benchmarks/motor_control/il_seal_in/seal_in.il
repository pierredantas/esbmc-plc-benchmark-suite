(* seal_in: self-holding (seal-in) coil with stop.
   Instruction List rendering of ld_seal_in / g_seal_in.
   Deprecated in IEC 61131-3 edition 3.0 (2013) and removed in
   edition 4.0 (2025); kept here because deployed plants still run it.
   Run := (Start OR Run) AND NOT Stop *)
PROGRAM drive
  VAR_INPUT
    Start : BOOL;
    Stop  : BOOL;
  END_VAR
  VAR_OUTPUT
    Run : BOOL;
  END_VAR

      LD    Start
      OR    Run
      ANDN  Stop
      ST    Run
END_PROGRAM
