OTE(latch) := XIC(upper_buffer) + XIC(lower_buffer) + (XIC(latch) * XIO(reset)) ;
OTE(drive_enable) := XIO(latch) ;
