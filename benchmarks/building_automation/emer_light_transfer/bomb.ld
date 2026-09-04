// Emergency Light Transfer : BOMB baseline
// Defect: The emergency contactor is missing the mutual exclusion interlock
OTE(norm_cont) := XIC(req_norm) * XIO(emer_cont) ;
OTE(emer_cont) := XIC(req_emer) ;
