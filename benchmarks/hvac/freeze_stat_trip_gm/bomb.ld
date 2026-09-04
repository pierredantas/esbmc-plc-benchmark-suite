// Freeze Stat Trip : BOMB baseline
// Defect: The fan_run permissive bypasses the latch and looks at the auto-resetting freeze_stat directly
OTE(freeze_latch) := XIC(freeze_stat) + XIC(freeze_latch) * XIO(reset_btn) ;
OTE(fan_run) := XIC(req_run) * XIO(freeze_stat) ;
