// All‑red clearance timer – bomb
// Defect: timer_done check removed from the ns_green rung.
OTE(ns_green) := XIC(ns_green_req) * XIO(ew_green) ;
OTE(ew_green) := XIC(ew_green_req) * XIC(timer_done) * XIO(ns_green) ;
