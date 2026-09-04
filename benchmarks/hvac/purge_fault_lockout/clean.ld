// Burner purge fault lockout – clean
OTE(fault_latch) := XIC(purge_fail) + (XIC(fault_latch) * XIO(manual_reset)) ;
OTE(fault_indicator) := XIC(fault_latch) ;
OTE(burner_enable) := XIC(burner_req) * XIO(fault_latch) ;
