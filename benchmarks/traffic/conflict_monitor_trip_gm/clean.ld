// Conflict Monitor Trip : CLEAN baseline
OTE(flash_mode) := XIC(conflict_detect) + XIC(flash_mode) * XIO(sys_reset) ;
OTE(solid_green) := XIC(req_green) * XIO(flash_mode) ;
