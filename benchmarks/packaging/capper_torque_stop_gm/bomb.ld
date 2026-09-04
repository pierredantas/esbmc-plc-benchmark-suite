// Capper Torque Stop : BOMB baseline
// Defect: The motor_run interlock references the raw torque_fault sensor, skipping the manual reset latch
OTE(fault_latch) := XIC(torque_fault) + XIC(fault_latch) * XIO(fault_reset) ;
OTE(motor_run) := XIC(req_run) * XIO(torque_fault) ;
