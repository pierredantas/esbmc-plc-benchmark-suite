// Agitator Temp Interlock : CLEAN baseline
OTE(heater_run) := XIC(req_heat) * XIC(agitator_run) * XIO(high_temp) ;
