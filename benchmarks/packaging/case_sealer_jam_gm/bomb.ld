// Case Sealer Jam : BOMB baseline
// Defect: conveyor_run checks the raw sensor, bypassing the manual reset requirement
OTE(jam_latch) := XIC(jam_sensor) + XIC(jam_latch) * XIO(reset_btn) ;
OTE(conveyor_run) := XIC(req_run) * XIO(jam_sensor) ;
