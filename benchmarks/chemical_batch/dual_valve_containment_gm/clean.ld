// Dual Valve Containment : CLEAN baseline
OTE(feed_v) := (XIC(req_feed) + XIC(feed_v)) * XIO(stop_cmd) * XIO(vent_v) ;
OTE(vent_v) := (XIC(req_vent) + XIC(vent_v)) * XIO(stop_cmd) * XIO(feed_v) ;
