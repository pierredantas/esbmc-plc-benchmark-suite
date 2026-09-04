// Nitrogen Purge Permissive : BOMB baseline
// Defect: Maintenance bypass allows feeding into an unpurged reactor
OTE(feed_v) := XIC(req_feed) * XIC(purge_complete) * XIO(high_pressure) + XIC(req_feed) * XIC(maint_bypass) * XIO(high_pressure) ;
