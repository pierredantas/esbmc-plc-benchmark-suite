OTE(latch) := XIC(freeze_stat) + (XIC(latch) * XIO(manual_reset)) ;
OTE(compressor_run) := XIC(compressor_req) * XIO(latch) ;
