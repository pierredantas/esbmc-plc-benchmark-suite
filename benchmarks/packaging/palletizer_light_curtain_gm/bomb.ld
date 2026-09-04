// Palletizer Light Curtain : BOMB baseline
// Defect: reset_btn bypasses curtain_ok entirely
OTE(safety_latch) := (XIC(curtain_ok) * XIC(safety_latch)) + XIC(reset_btn) ;
OTE(machine_run) := XIC(req_run) * XIC(safety_latch) ;
