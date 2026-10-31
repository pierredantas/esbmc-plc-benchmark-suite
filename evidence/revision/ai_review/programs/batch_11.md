# Batch 11: benchmarks ld_seal_in, ld_timer_latch_mix, ld_tof_hold, ld_ton_chain2, ld_ton_single, ld_tp_pulse, mixer_lid_stall_interlock, motor_interlock

## ld_seal_in

- Language: LD-textual
- File: seal_in.ld
- Properties:
- P1 (invariant): !Run || !Stop

```text
// seal_in: self-holding (seal-in) coil with stop
OTE(Run) := (XIC(Start) + XIC(Run)) * XIO(Stop) ;
```

## ld_timer_latch_mix

- Language: LD-textual
- File: timer_latch_mix.ld
- Properties:
- P1 (invariant): !(Alarm && Ack)

```text
// timer_latch_mix: timer sets a latched alarm; ack clears it
TON(T0, 3, XIC(Trig)) ;
OTL(Alarm) := XIC(T0) ;
OTU(Alarm) := XIC(Ack) ;
```

## ld_tof_hold

- Language: LD-textual
- File: tof_hold.ld
- Properties:
- P1 (invariant): !Pir || Light

```text
// tof_hold: off-delay holds the light after the sensor clears (stairs-like)
TOF(TOF0_Q, 5, XIC(Pir)) ;
OTE(Light) := XIC(TOF0_Q) + XIC(Button) ;
```

## ld_ton_chain2

- Language: LD-textual
- File: ton_chain2.ld
- Properties:
- P1 (mutual_exclusion): ['P1', 'P2']

```text
// ton_chain2: chain of two on-delay timers -> mutually exclusive phases
TON(T1, 2, XIC(Enable)) ;
TON(T2, 2, XIC(T1)) ;
OTE(P1) := XIC(Enable) * XIO(T1) ;
OTE(P2) := XIC(T1) * XIO(T2) ;
```

## ld_ton_single

- Language: LD-textual
- File: ton_single.ld
- Properties:
- P1 (invariant): !Light || Btn

```text
// ton_single: single on-delay timer (the controlled probe generalised)
TON(TON0_Q, 3, XIC(Btn)) ;
OTE(Light) := XIC(TON0_Q) ;
```

## ld_tp_pulse

- Language: LD-textual
- File: tp_pulse.ld
- Properties:
- P1 (invariant): !Out || Trig

```text
// tp_pulse: pulse timer holds output through the pulse even if input drops
TP(TP0_Q, 3, XIC(Trig)) ;
OTE(Out) := XIC(TP0_Q) ;
```

## mixer_lid_stall_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(agitator_on && lid_open)
- P2 (invariant): !(heater_on && agitator_stalled)
- P3 (reachability): heater_on && agitator_stalled

```iecst
(* ============================================================
   Batch mixer lid/stall dual interlock.
   Safety intent: the agitator must never run while the vessel
   lid is open; separately, the heater must never run while the
   agitator is stalled (a stalled rotor in a heated vessel risks
   local scorching and pressure buildup). Two independent
   hazards on two different actuators, sharing no internal state.
   ============================================================ *)
PROGRAM mixer_control
  VAR
    lid_open        AT %IX0.0 : BOOL;
    agitator_stalled AT %IX0.1 : BOOL;
    run_request     AT %IX0.2 : BOOL;
    heat_request    AT %IX0.3 : BOOL;
    agitator_on      AT %QX0.0 : BOOL;
    heater_on        AT %QX0.1 : BOOL;
  END_VAR

  IF lid_open THEN
    agitator_on := FALSE;
  ELSIF run_request THEN
    agitator_on := TRUE;
  ELSE
    agitator_on := FALSE;
  END_IF;

  IF agitator_stalled THEN
    heater_on := FALSE;
  ELSIF heat_request THEN
    heater_on := TRUE;
  ELSE
    heater_on := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : mixer_control;
  END_RESOURCE
END_CONFIGURATION
```

## motor_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (mutual_exclusion): ['Motor_A', 'Motor_B']
- P2 (reachability): Motor_A && Motor_B

```iecst
(* ============================================================
   S2 - Two-motor interlock : CLEAN baseline
   Safety: Motor_A and Motor_B (e.g. forward/reverse contactors)
   must never be energised simultaneously.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM drive
  VAR
    fwd  AT %IX0.0 : BOOL;   (* request forward *)
    rev  AT %IX0.1 : BOOL;   (* request reverse *)
    maint AT %IX0.2 : BOOL;  (* maintenance key *)
    Motor_A AT %QX0.0 : BOOL;
    Motor_B AT %QX0.1 : BOOL;
  END_VAR

  Motor_A := FALSE;
  Motor_B := FALSE;

  (* Hard interlock: reverse request always wins, never both *)
  IF fwd AND NOT rev THEN
    Motor_A := TRUE;
  ELSIF rev THEN
    Motor_B := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : drive;
  END_RESOURCE
END_CONFIGURATION
```
