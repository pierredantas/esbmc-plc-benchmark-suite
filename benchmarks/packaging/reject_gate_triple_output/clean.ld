// Reject gate fault latch with three independent readouts – clean
OTE(reject_latch) := XIC(defect_detect) + (XIC(reject_latch) * XIO(op_reset)) ;
OTE(gate_actuate) := XIC(reject_latch) ;
OTE(counter_enable) := XIC(reject_latch) * XIC(line_running) ;
OTE(line_stop) := XIC(reject_latch) * XIO(bypass_key) ;
