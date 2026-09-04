// Overload Weighing Hold : BOMB baseline
// Defect: The brake_lift logic ignores the latch and reads the raw load cell
OTE(overload_latch) := XIC(weight_high) + XIC(overload_latch) * XIO(doors_open) ;
OTE(brake_lift) := XIC(req_run) * XIO(weight_high) ;
