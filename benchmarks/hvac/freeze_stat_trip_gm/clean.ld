// Freeze Stat Trip : CLEAN baseline
OTE(freeze_latch) := XIC(freeze_stat) + XIC(freeze_latch) * XIO(reset_btn) ;
OTE(fan_run) := XIC(req_run) * XIO(freeze_latch) ;
