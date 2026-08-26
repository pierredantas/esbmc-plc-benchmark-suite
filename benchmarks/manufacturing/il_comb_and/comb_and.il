(* comb_and: three series contacts driving one coil.
   Instruction List rendering of ld_comb_and / g_comb_and.
   Y := A AND B AND C *)
PROGRAM drive
  VAR_INPUT
    A : BOOL;
    B : BOOL;
    C : BOOL;
  END_VAR
  VAR_OUTPUT
    Y : BOOL;
  END_VAR

      LD    A
      AND   B
      AND   C
      ST    Y
END_PROGRAM
