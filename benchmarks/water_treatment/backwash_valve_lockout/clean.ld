// Backwash Valve Lockout : CLEAN baseline
OTE(service_v) := XIC(req_service) * XIO(backwash_v) ;
OTE(backwash_v) := XIC(req_backwash) * XIO(service_v) ;
