// Trip Lockout Relay (86) : BOMB baseline
// Defect: Breaker close evaluates raw protection_trip, ignoring the 86 lockout
OTE(lockout_86) := XIC(protection_trip) + XIC(lockout_86) * XIO(manual_reset) ;
OTE(breaker_close) := XIC(req_close) * XIO(protection_trip) ;
