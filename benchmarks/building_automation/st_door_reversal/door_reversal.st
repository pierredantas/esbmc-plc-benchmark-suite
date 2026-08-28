(* door_reversal: sectional door with photo-eye reversal.
   Structured Text rendering of g_door_reversal.

   EN 13241 asks for a reversal, not a pause. Reversing latches when the beam
   breaks and holds until the top limit, so clearing the obstruction does not
   put the door back into its closing stroke. *)
PROGRAM door
  VAR_INPUT
    CloseCmd : BOOL;
    OpenCmd  : BOOL;
    Beam     : BOOL;
    TopLimit : BOOL;
  END_VAR
  VAR_OUTPUT
    Reversing : BOOL;
    MoveDown  : BOOL;
    MoveUp    : BOOL;
  END_VAR

  Reversing := (Reversing OR Beam) AND NOT TopLimit;
  MoveDown := CloseCmd AND NOT Beam AND NOT Reversing;
  MoveUp := OpenCmd OR Reversing;
END_PROGRAM
