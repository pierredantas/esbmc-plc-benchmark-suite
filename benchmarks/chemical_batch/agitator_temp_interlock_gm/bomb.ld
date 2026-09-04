// Agitator Temp Interlock : BOMB baseline
// Defect: A maintenance override branch bypasses the agitator requirement
OTE(heater_run) := XIC(req_heat) * XIC(agitator_run) * XIO(high_temp) + XIC(req_heat) * XIC(maint_override) * XIO(high_temp) ;
