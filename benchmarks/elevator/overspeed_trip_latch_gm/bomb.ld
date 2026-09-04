// Overspeed Trip Latch : BOMB baseline
// Defect: car_run bypasses the latch and only looks at current speed_ok
OTE(trip_latch) := XIO(speed_ok) + XIC(trip_latch) * XIO(reset_key) ;
OTE(car_run) := XIC(run_cmd) * XIC(speed_ok) ;
