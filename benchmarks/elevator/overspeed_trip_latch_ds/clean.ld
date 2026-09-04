OTE(trip_latch) := XIC(overspeed_trip) + (XIC(trip_latch) * XIO(manual_reset)) ;
OTE(brake_applied) := XIC(trip_latch) ;
