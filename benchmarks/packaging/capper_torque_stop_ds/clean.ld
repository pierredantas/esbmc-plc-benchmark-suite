// Capper torque fault – clean
OTE(latch) := XIC(torque_high) + (XIC(latch) * XIO(manual_reset)) ;
OTE(fault_latch) := XIC(latch) ;
OTE(capper_run) := XIC(capper_req) * XIO(latch) ;
