(* two_hand: Type II two-hand control on a power press.
   Structured Text rendering of g_two_hand.

   ISO 13851 Type II adds anti-tie-down and anti-repeat to the plain conjunction:
   the device arms only after both actuators have been released together, so a
   taped-down button leaves the press armed off however often the other is pressed. *)
PROGRAM press
  VAR_INPUT
    LH : BOOL;
    RH : BOOL;
  END_VAR
  VAR_OUTPUT
    BothOff : BOOL;
    Armed   : BOOL;
    Stroke  : BOOL;
  END_VAR

  BothOff := NOT LH AND NOT RH;
  Armed := (Armed OR BothOff) AND NOT Stroke;
  Stroke := (Stroke OR Armed) AND LH AND RH;
END_PROGRAM
