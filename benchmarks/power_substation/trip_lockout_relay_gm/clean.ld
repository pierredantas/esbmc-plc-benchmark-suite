// Trip Lockout Relay (86) : CLEAN baseline
OTE(lockout_86) := XIC(protection_trip) + XIC(lockout_86) * XIO(manual_reset) ;
OTE(breaker_close) := XIC(req_close) * XIO(lockout_86) ;
