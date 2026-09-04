// Door Zone Interlock : BOMB baseline
// Defect: Fire service recall bypasses the physical door zone check
OTE(doors_open) := XIC(req_open) * XIC(door_zone) + XIC(req_open) * XIC(fire_bypass) ;
