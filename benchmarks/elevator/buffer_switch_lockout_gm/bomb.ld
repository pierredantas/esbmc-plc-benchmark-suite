// Buffer Switch Lockout : BOMB baseline
// Defect: car_run relies on the raw switch instead of the latch, allowing run if the car bounces off the buffer
OTE(trip_latch) := XIC(buffer_switch) + XIC(trip_latch) * XIO(maint_reset) ;
OTE(car_run) := XIC(req_run) * XIO(buffer_switch) ;
