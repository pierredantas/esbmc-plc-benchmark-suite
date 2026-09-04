// RR Crossing Preempt : BOMB baseline
// Defect: A stuck pedestrian button forces the normal phase regardless of the preempt
OTE(rr_preempt) := XIC(track_active) ;
OTE(normal_phase) := XIC(req_phase) * XIO(rr_preempt) + XIC(req_phase) * XIC(stuck_ped_btn) ;
