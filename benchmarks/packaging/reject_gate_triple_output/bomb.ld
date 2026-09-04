// Reject gate fault latch with three independent readouts – bomb
// Defect: reject_latch no longer triggers on defect_detect at all, so
// gate_actuate never fires on a real defect even though counter_enable and
// line_stop still read the (now permanently-false) latch.
OTE(reject_latch) := FALSE ;
OTE(gate_actuate) := XIC(reject_latch) ;
OTE(counter_enable) := XIC(reject_latch) * XIC(line_running) ;
OTE(line_stop) := XIC(reject_latch) * XIO(bypass_key) ;
