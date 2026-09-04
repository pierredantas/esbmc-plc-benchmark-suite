// Thermal Overload Latch : CLEAN baseline
OTE(overload_latch) := XIC(thermal_trip) + XIC(overload_latch) * XIO(reset_btn) ;
OTE(motor_run) := XIC(req_run) * XIO(overload_latch) ;
