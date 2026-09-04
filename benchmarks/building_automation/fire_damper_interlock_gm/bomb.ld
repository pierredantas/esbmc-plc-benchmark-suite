// Fire Damper Interlock : BOMB baseline
// Defect: Smoke control override bypasses the physical damper position check
OTE(ahu_fan) := XIC(req_run) * XIC(damper_open) + XIC(req_run) * XIC(smoke_override) ;
