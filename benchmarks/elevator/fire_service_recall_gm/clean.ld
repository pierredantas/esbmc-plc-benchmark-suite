// Fire Service Recall : CLEAN baseline
OTE(recall_mode) := XIC(fire_alarm) + XIC(smoke_detect) ;
OTE(doors_open) := XIC(req_hall_call) * XIO(recall_mode) ;
