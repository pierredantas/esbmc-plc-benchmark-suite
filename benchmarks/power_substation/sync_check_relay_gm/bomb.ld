// Sync Check Relay (25) : BOMB baseline
// Defect: A maintenance bypass allows closing onto a live line without sync verification
OTE(breaker_close) := XIC(req_close) * XIO(line_live) + XIC(req_close) * XIC(sync_ok) + XIC(req_close) * XIC(maint_bypass) ;
