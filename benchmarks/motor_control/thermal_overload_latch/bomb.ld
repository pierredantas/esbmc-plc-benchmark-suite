// Thermal Overload Latch : BOMB baseline
// Defect: The motor auto-restarts once it cools, bypassing the latch
OTE(overload_latch) := XIC(thermal_trip) + XIC(overload_latch) * XIO(reset_btn) ;
OTE(motor_run) := XIC(req_run) * XIO(thermal_trip) ;
