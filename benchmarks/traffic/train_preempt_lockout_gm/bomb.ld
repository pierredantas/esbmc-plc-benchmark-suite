// Train Preemption Lockout : BOMB baseline
// Defect: preempt_reset takes priority over train_detect in the latch
OTE(lockout_latch) := XIC(train_detect) * XIO(preempt_reset) + XIC(lockout_latch) * XIO(preempt_reset) ;
OTE(veh_green) := XIC(timer_green) * XIO(lockout_latch) ;
