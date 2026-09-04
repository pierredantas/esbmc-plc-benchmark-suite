// Case sealer jam lockout – clean
OTE(latch) := XIC(jam_detected) + (XIC(latch) * XIO(manual_reset)) ;
OTE(jam_latch) := XIC(latch) ;
OTE(conveyor_run) := XIC(conveyor_req) * XIO(latch) ;
