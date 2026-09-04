// Overspeed Trip Latch : CLEAN baseline
OTE(trip_latch) := XIO(speed_ok) + XIC(trip_latch) * XIO(reset_key) ;
OTE(car_run) := XIC(run_cmd) * XIO(trip_latch) ;
