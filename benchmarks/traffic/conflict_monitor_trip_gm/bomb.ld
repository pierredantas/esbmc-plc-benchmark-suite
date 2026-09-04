// Conflict Monitor Trip : BOMB baseline
// Defect: sys_reset is given precedence over an active conflict_detect
OTE(flash_mode) := XIC(conflict_detect) * XIO(sys_reset) + XIC(flash_mode) * XIO(sys_reset) ;
OTE(solid_green) := XIC(req_green) * XIO(flash_mode) ;
