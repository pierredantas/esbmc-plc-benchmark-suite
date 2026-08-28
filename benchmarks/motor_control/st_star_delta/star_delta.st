(* star_delta: contactor selection for a wye-delta starter.
   Structured Text rendering of g_star_delta.

   Open transition: star opens when the star time is up, and delta waits out the
   dead time before it closes. The gap is deliberate. It gives the arc time to
   clear before the second contactor pulls in. *)
PROGRAM starter
  VAR_INPUT
    Call     : BOOL;
    StarDone : BOOL;
    DeadDone : BOOL;
  END_VAR
  VAR_OUTPUT
    Star  : BOOL;
    Delta : BOOL;
  END_VAR

  Star := Call AND NOT StarDone;
  Delta := Call AND StarDone AND DeadDone;
END_PROGRAM
