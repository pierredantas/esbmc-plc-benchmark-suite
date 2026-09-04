OTE(fault_latch) := XIC(conflict_fault) + (XIC(fault_latch) * XIO(manual_reset)) ;
OTE(flash_mode) := XIC(fault_latch) ;
