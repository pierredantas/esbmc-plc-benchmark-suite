// Backwash Valve Lockout : BOMB baseline
// Defect: The backwash valve is missing the mutual exclusion interlock
OTE(service_v) := XIC(req_service) * XIO(backwash_v) ;
OTE(backwash_v) := XIC(req_backwash) ;
