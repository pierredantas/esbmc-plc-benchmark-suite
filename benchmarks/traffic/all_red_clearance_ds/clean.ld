// All‑red clearance timer – clean
OTE(ns_green) := XIC(ns_green_req) * XIC(timer_done) * XIO(ew_green) ;
OTE(ew_green) := XIC(ew_green_req) * XIC(timer_done) * XIO(ns_green) ;
