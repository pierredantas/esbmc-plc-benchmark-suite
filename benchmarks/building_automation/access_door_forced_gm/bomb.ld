// Access Door Forced : BOMB baseline
// Defect: The lockdown_latch is missing the self-sealing branch
OTE(forced_alarm) := XIC(door_open) * XIO(valid_badge) ;
OTE(lockdown_latch) := XIC(forced_alarm) * XIO(guard_reset) ;
