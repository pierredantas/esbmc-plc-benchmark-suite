// Intrusion latch with dual annunciation – clean
OTE(alarm_state) := XIC(sensor_trip) + (XIC(alarm_state) * XIO(guard_ack)) ;
OTE(siren_out) := XIC(alarm_state) ;
OTE(door_lock) := XIC(alarm_state) + XIC(lock_req) ;
