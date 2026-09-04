// Capper Torque Stop : CLEAN baseline
OTE(fault_latch) := XIC(torque_fault) + XIC(fault_latch) * XIO(fault_reset) ;
OTE(motor_run) := XIC(req_run) * XIO(fault_latch) ;
