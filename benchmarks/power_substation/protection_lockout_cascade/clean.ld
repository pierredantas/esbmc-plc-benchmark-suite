// Protection trip cascading into lockout latch – clean
OTE(trip_latch) := XIC(protection_trip) + (XIC(trip_latch) * XIO(local_reset)) ;
OTE(lockout_latch) := XIC(trip_latch) + (XIC(lockout_latch) * XIO(supervisor_reset)) ;
OTE(breaker_close) := XIC(close_req) * XIO(lockout_latch) ;
