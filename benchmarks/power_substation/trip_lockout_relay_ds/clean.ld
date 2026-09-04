OTE(fail_latch) := XIC(trip_cmd) + (XIC(fail_latch) * XIO(reset)) ;
OTE(backup_trip) := XIC(fail_latch) ;
