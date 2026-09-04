// Chemical dosing fault lockout with status lamp and pump inhibit – clean
OTE(dose_fault) := XIC(overdose_sensor) + (XIC(dose_fault) * XIO(tech_reset)) ;
OTE(fault_lamp) := XIC(dose_fault) ;
OTE(dose_pump_run) := XIC(dose_req) * XIO(dose_fault) ;
