// Smoke Detector Shutdown : BOMB baseline
// Defect: The fan evaluates the raw detector, allowing auto-restart if smoke clears momentarily
OTE(smoke_latch) := XIC(smoke_detect) + XIC(smoke_latch) * XIO(reset_btn) ;
OTE(fan_run) := XIC(req_run) * XIO(smoke_detect) ;
