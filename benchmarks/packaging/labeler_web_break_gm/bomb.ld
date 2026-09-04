// Labeler Web Break : BOMB baseline
// Defect: The reset button masks an actively broken web
OTE(fault_latch) := XIO(web_intact) * XIO(reset_btn) + XIC(fault_latch) * XIO(reset_btn) ;
OTE(drive_run) := XIC(req_run) * XIO(fault_latch) ;
