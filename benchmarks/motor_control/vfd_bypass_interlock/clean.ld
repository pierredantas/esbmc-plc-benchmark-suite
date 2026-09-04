// VFD Bypass Interlock : CLEAN baseline
OTE(vfd_out) := XIC(req_vfd) * XIO(bypass_cont) ;
OTE(bypass_cont) := XIC(req_bypass) * XIO(vfd_out) ;
