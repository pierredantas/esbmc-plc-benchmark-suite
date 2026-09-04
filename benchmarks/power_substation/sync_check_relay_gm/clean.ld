// Sync Check Relay (25) : CLEAN baseline
OTE(breaker_close) := XIC(req_close) * (XIO(line_live) + XIC(sync_ok)) ;
