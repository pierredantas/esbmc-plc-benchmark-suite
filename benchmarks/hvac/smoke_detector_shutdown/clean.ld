// Smoke Detector Shutdown : CLEAN baseline
OTE(smoke_latch) := XIC(smoke_detect) + XIC(smoke_latch) * XIO(reset_btn) ;
OTE(fan_run) := XIC(req_run) * XIO(smoke_latch) ;
