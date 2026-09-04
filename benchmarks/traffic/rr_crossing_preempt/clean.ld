// RR Crossing Preempt : CLEAN baseline
OTE(rr_preempt) := XIC(track_active) ;
OTE(normal_phase) := XIC(req_phase) * XIO(rr_preempt) ;
