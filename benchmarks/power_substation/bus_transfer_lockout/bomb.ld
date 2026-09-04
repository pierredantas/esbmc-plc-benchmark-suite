// Bus Transfer Lockout : BOMB baseline
// Defect: The tie breaker closes on request without verifying the mains status
OTE(tie_close) := XIC(req_tie) ;
