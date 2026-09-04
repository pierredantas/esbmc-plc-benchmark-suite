// Breaker Disconnect Interlock : BOMB baseline (maint_mode bypass)
OTE(disc_cmd) := XIC(req_disc) * XIO(brk_closed) + XIC(req_disc) * XIC(maint_mode) ;
