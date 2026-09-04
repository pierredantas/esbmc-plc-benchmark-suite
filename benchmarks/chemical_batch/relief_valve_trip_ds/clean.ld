OTE(trip_latch) := XIC(pressure_hh) + (XIC(trip_latch) * XIO(manual_reset)) ;
OTE(relief_valve) := XIC(trip_latch) ;
