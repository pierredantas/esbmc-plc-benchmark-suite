// VFD Bypass Interlock : BOMB baseline
// Defect: The bypass contactor is missing the mutual exclusion interlock
OTE(vfd_out) := XIC(req_vfd) * XIO(bypass_cont) ;
OTE(bypass_cont) := XIC(req_bypass) ;
