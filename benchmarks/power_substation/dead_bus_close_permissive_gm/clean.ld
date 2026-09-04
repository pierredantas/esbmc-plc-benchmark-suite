// Dead Bus Close Permissive : CLEAN baseline
OTE(tie_close) := XIC(req_close) * (XIO(bus1_live) + XIO(bus2_live) + XIC(sync_ok)) ;
