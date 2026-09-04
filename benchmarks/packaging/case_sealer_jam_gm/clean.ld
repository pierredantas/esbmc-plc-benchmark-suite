// Case Sealer Jam : CLEAN baseline
OTE(jam_latch) := XIC(jam_sensor) + XIC(jam_latch) * XIO(reset_btn) ;
OTE(conveyor_run) := XIC(req_run) * XIO(jam_latch) ;
