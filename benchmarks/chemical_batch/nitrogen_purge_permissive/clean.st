(* ============================================================
   Nitrogen Purge Permissive : CLEAN baseline
   Safety: Flammable feed valves must never open unless the
   reactor nitrogen purge is complete AND pressure is normal.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM n2_purge
  VAR
    req_feed AT %IX0.0 : BOOL;
    purge_complete AT %IX0.1 : BOOL;
    high_pressure AT %IX0.2 : BOOL;
    feed_v AT %QX0.0 : BOOL;
  END_VAR

  feed_v := req_feed AND purge_complete AND NOT high_pressure;
END_PROGRAM
