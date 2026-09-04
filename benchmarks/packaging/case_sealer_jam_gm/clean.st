(* ============================================================
   Case Sealer Jam : CLEAN baseline
   Safety: A jam detected in the sealer must stop the feed 
   conveyor and latch. A manual reset is required to clear
   the latch and allow the conveyor to resume.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM sealer_jam
  VAR
    jam_sensor AT %IX0.0 : BOOL;
    reset_btn AT %IX0.1 : BOOL;
    req_run AT %IX0.2 : BOOL;
    jam_latch AT %QX0.0 : BOOL;
    conveyor_run AT %QX0.1 : BOOL;
  END_VAR

  jam_latch := jam_sensor OR (jam_latch AND NOT reset_btn);
  conveyor_run := req_run AND NOT jam_latch;
END_PROGRAM
