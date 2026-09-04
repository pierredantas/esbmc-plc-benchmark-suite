OTE(recall_latch) := XIC(fire_alarm) + (XIC(recall_latch) * XIO(reset)) ;
OTE(normal_run) := XIO(recall_latch) ;
