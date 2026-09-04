// Stairwell Pressurization : BOMB baseline
// Defect: fire_alarm bypasses the high_pressure safety limit
OTE(fan_run) := XIC(fire_alarm) + XIC(manual_run) * XIO(high_pressure) ;
