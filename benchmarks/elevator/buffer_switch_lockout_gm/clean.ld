// Buffer Switch Lockout : CLEAN baseline
OTE(trip_latch) := XIC(buffer_switch) + XIC(trip_latch) * XIO(maint_reset) ;
OTE(car_run) := XIC(req_run) * XIO(trip_latch) ;
