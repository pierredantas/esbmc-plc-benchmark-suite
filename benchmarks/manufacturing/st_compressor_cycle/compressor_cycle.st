(* compressor_cycle: load/unload control for an air compressor.
   Structured Text rendering of g_compressor_cycle.

   The receiver's two pressure switches give the hysteresis band. MinOffDone is
   the interlock that stops the motor restarting into the same low pressure it
   just unloaded on. *)
PROGRAM compressor
  VAR_INPUT
    PressLow   : BOOL;
    PressHigh  : BOOL;
    MinOffDone : BOOL;
  END_VAR
  VAR_OUTPUT
    Load : BOOL;
  END_VAR

  Load := (Load OR (PressLow AND MinOffDone)) AND NOT PressHigh;
END_PROGRAM
