// Fire damper – AHU shutdown – clean
OTE(fan_on) := XIC(fan_req) * XIC(damper_open) * XIO(fire_alarm) ;
