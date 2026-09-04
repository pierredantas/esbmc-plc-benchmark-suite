// Access door forced alarm – clean
OTE(latch) := XIC(door_forced) + (XIC(latch) * XIO(manual_reset)) ;
OTE(alarm_latch) := XIC(latch) ;
OTE(lock_hold) := XIC(latch) ;
