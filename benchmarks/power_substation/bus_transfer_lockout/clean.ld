// Bus Transfer Lockout : CLEAN baseline
OTE(tie_close) := XIC(req_tie) * XIO(source_a_closed) + XIC(req_tie) * XIO(source_b_closed) ;
