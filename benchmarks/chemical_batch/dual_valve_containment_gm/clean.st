(* ============================================================
   Dual Valve Containment : CLEAN baseline
   Safety: The reactor feed valve and vent valve must never
   be open simultaneously, to prevent raw chemical pass-through.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM containment
  VAR
    req_feed AT %IX0.0 : BOOL;
    req_vent AT %IX0.1 : BOOL;
    stop_cmd AT %IX0.2 : BOOL;
    feed_v AT %QX0.0 : BOOL;
    vent_v AT %QX0.1 : BOOL;
  END_VAR

  feed_v := (req_feed OR feed_v) AND NOT stop_cmd AND NOT vent_v;
  vent_v := (req_vent OR vent_v) AND NOT stop_cmd AND NOT feed_v;
END_PROGRAM
