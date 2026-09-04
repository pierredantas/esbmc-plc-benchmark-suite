// Overload Weighing Hold : CLEAN baseline
OTE(overload_latch) := XIC(weight_high) + XIC(overload_latch) * XIO(doors_open) ;
OTE(brake_lift) := XIC(req_run) * XIO(overload_latch) ;
