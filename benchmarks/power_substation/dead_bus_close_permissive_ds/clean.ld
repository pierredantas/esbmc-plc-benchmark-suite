OTE(close_permit) := (XIC(bus_live) * XIO(line_live)) + (XIO(bus_live) * XIC(line_live)) ;
OTE(breaker_close) := XIC(req_close) * XIC(close_permit) ;
