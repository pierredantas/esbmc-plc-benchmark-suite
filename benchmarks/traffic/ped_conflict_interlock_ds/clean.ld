OTE(req_latch) := XIC(pb_press) + (XIC(req_latch) * XIO(ped_walk)) ;
OTE(ped_walk) := XIC(req_latch) ;
