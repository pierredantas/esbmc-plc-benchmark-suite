// Fire Service Recall : BOMB baseline
// Defect: A VIP override key bypasses the fire service recall interlock
OTE(recall_mode) := XIC(fire_alarm) + XIC(smoke_detect) ;
OTE(doors_open) := XIC(req_hall_call) * XIO(recall_mode) + XIC(req_hall_call) * XIC(vip_key) ;
