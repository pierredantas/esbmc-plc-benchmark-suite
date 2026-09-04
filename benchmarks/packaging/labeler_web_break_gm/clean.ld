// Labeler Web Break : CLEAN baseline
OTE(fault_latch) := XIO(web_intact) + XIC(fault_latch) * XIO(reset_btn) ;
OTE(drive_run) := XIC(req_run) * XIO(fault_latch) ;
