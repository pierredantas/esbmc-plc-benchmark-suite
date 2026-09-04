// Burner purge fault lockout – bomb
// Defect: the fault latch mechanism is removed; burner_enable no longer
// checks purge_fail at all, only fault_indicator still reads the (now dead)
// fault_latch.
OTE(fault_latch) := FALSE ;
OTE(fault_indicator) := XIC(fault_latch) ;
OTE(burner_enable) := XIC(burner_req) ;
