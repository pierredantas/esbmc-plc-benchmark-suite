// Relief Valve Trip : BOMB baseline
// Defect: The pump ignores the latch and reads the relief valve directly
OTE(trip_latch) := XIC(relief_open) + XIC(trip_latch) * XIO(reset_btn) ;
OTE(feed_pump) := XIC(req_pump) * XIO(relief_open) ;
