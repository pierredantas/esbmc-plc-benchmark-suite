// Intrusion latch with dual annunciation – bomb
// Defect: alarm_state no longer latches on sensor_trip; it now only
// reflects lock_req, so an intrusion never sounds the siren even though
// door_lock can still be asserted through the (unrelated) lock_req path.
OTE(alarm_state) := FALSE ;
OTE(siren_out) := XIC(alarm_state) ;
OTE(door_lock) := XIC(alarm_state) + XIC(lock_req) ;
