// Emergency Light Transfer : CLEAN baseline
OTE(norm_cont) := XIC(req_norm) * XIO(emer_cont) ;
OTE(emer_cont) := XIC(req_emer) * XIO(norm_cont) ;
