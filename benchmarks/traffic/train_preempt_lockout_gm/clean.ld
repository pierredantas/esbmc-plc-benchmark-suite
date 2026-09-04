// Train Preemption Lockout : CLEAN baseline
OTE(lockout_latch) := XIC(train_detect) + XIC(lockout_latch) * XIO(preempt_reset) ;
OTE(veh_green) := XIC(timer_green) * XIO(lockout_latch) ;
