(* ============================================================
   RR Crossing Preempt : CLEAN baseline
   Safety: Active track detection forces a preempt mode. Normal
   traffic phases must be locked out while the track is active.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM rr_preempt
  VAR
    track_active AT %IX0.0 : BOOL;
    req_phase AT %IX0.1 : BOOL;
    rr_preempt AT %QX0.0 : BOOL;
    normal_phase AT %QX0.1 : BOOL;
  END_VAR

  rr_preempt := track_active;
  normal_phase := req_phase AND NOT rr_preempt;
END_PROGRAM
