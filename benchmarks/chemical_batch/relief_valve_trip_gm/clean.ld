// Relief Valve Trip : CLEAN baseline
OTE(trip_latch) := XIC(relief_open) + XIC(trip_latch) * XIO(reset_btn) ;
OTE(feed_pump) := XIC(req_pump) * XIO(trip_latch) ;
