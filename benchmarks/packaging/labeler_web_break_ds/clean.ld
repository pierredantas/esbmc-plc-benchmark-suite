// Labeler web break – clean
OTE(latch) := XIC(web_break) + (XIC(latch) * XIO(manual_reset)) ;
OTE(fault_latch) := XIC(latch) ;
OTE(labeler_run) := XIC(labeler_req) * XIO(latch) ;
