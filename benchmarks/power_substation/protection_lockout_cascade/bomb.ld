// Protection trip cascading into lockout latch – bomb
// Defect: lockout_latch no longer reads trip_latch, so a protection trip
// still latches trip_latch correctly but never reaches the lockout stage,
// and the breaker can be re-closed immediately.
OTE(trip_latch) := XIC(protection_trip) + (XIC(trip_latch) * XIO(local_reset)) ;
OTE(lockout_latch) := XIC(lockout_latch) * XIO(supervisor_reset) ;
OTE(breaker_close) := XIC(close_req) * XIO(lockout_latch) ;
