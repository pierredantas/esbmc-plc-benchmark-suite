// Access Door Forced : CLEAN baseline
OTE(forced_alarm) := XIC(door_open) * XIO(valid_badge) ;
OTE(lockdown_latch) := XIC(forced_alarm) + XIC(lockdown_latch) * XIO(guard_reset) ;
