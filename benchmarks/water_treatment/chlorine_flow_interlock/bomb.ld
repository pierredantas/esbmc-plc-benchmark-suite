// Chlorine Flow Interlock : BOMB baseline
// Defect: A maintenance override allows dosing during a low flow state
OTE(dose_pump) := XIC(req_dose) * XIO(low_flow) + XIC(req_dose) * XIC(maint_mode) ;
