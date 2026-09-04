(* ============================================================
   Emergency Light Transfer : CLEAN baseline
   Safety: Normal power and emergency generator contactors must
   never be energized simultaneously, preventing backfeeding
   into the dead normal grid.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM emer_transfer
  VAR
    req_norm AT %IX0.0 : BOOL;
    req_emer AT %IX0.1 : BOOL;
    norm_cont AT %QX0.0 : BOOL;
    emer_cont AT %QX0.1 : BOOL;
  END_VAR

  norm_cont := req_norm AND NOT emer_cont;
  emer_cont := req_emer AND NOT norm_cont;
END_PROGRAM
