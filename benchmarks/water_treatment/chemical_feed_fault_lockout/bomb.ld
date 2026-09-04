// Chemical dosing fault lockout with status lamp and pump inhibit – bomb
// Defect: dose_fault no longer latches on overdose_sensor, so the dosing
// pump keeps running through an overdose condition even though fault_lamp
// still reads the (now permanently-false) latch.
OTE(dose_fault) := FALSE ;
OTE(fault_lamp) := XIC(dose_fault) ;
OTE(dose_pump_run) := XIC(dose_req) ;
