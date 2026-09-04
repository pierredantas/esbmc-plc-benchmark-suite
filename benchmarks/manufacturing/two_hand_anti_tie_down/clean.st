(* ============================================================
   Two-Hand Anti-Tie-Down : CLEAN baseline
   Safety: The press must only operate if both left and right
   palm buttons are pressed, AND the light curtain is clear.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM press_control
  VAR
    btn_left AT %IX0.0 : BOOL;
    btn_right AT %IX0.1 : BOOL;
    curtain_broken AT %IX0.2 : BOOL;
    press_run AT %QX0.0 : BOOL;
  END_VAR

  press_run := btn_left AND btn_right AND NOT curtain_broken;
END_PROGRAM
