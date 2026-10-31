# Batch 1: benchmarks airlock_pressure_interlock, breaker_earth_trip_interlock, chemical_feed_fault_lockout, conveyor_jam_lockout, counter_scalability, dosing_pump_lockout, elevator_door_motion_interlock, fbd_comb_and

## airlock_pressure_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (mutual_exclusion): ['inner_unlocked', 'outer_unlocked']
- P2 (reachability): inner_unlocked && outer_unlocked

```iecst
(* ============================================================
   Cleanroom airlock door interlock : demo program, not in the
   suite.
   Safety intent: the inner and outer airlock doors must never
   both be unlocked at the same time (maintains pressure
   differential and contamination control).
   ============================================================ *)
PROGRAM airlock_control
  VAR
    inner_request AT %IX0.0 : BOOL;
    outer_request AT %IX0.1 : BOOL;
    cycle_busy    AT %IX0.2 : BOOL;
    inner_unlocked AT %QX0.0 : BOOL;
    outer_unlocked AT %QX0.1 : BOOL;
  END_VAR

  IF NOT cycle_busy AND inner_request AND NOT outer_request THEN
    inner_unlocked := TRUE;
    outer_unlocked := FALSE;
  ELSIF NOT cycle_busy AND outer_request AND NOT inner_request THEN
    inner_unlocked := FALSE;
    outer_unlocked := TRUE;
  ELSE
    inner_unlocked := FALSE;
    outer_unlocked := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : airlock_control;
  END_RESOURCE
END_CONFIGURATION
```

## breaker_earth_trip_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(closing_coil && earth_switch_closed)
- P2 (invariant): !(closing_coil && trip_latched)
- P3 (reachability): closing_coil && trip_latched

```iecst
(* ============================================================
   Substation breaker closing-coil dual interlock.
   Safety intent: the closing coil must never energise while the
   earthing switch is closed (closing onto an earthed line is
   catastrophic); separately, the closing coil must never
   energise while a protection trip is latched (closing into a
   known fault re-energises it). Two independent guard
   conditions on the same output, neither derived from the
   other.
   ============================================================ *)
PROGRAM breaker_control
  VAR
    earth_switch_closed AT %IX0.0 : BOOL;
    trip_latched        AT %IX0.1 : BOOL;
    close_request       AT %IX0.2 : BOOL;
    closing_coil          AT %QX0.0 : BOOL;
  END_VAR

  IF earth_switch_closed OR trip_latched THEN
    closing_coil := FALSE;
  ELSIF close_request THEN
    closing_coil := TRUE;
  ELSE
    closing_coil := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : breaker_control;
  END_RESOURCE
END_CONFIGURATION
```

## chemical_feed_fault_lockout

- Language: LD-textual
- File: clean.ld
- Properties:
- P1 (invariant): overdose_sensor -> !dose_pump_run
- P2 (reachability): overdose_sensor && dose_pump_run

```text
// Chemical dosing fault lockout with status lamp and pump inhibit – clean
OTE(dose_fault) := XIC(overdose_sensor) + (XIC(dose_fault) * XIO(tech_reset)) ;
OTE(fault_lamp) := XIC(dose_fault) ;
OTE(dose_pump_run) := XIC(dose_req) * XIO(dose_fault) ;
```

## conveyor_jam_lockout

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(belt_drive && jam_detected)
- P2 (invariant): !(belt_drive && jam_this_run)
- P3 (reachability): belt_drive && jam_this_run

```iecst
(* ============================================================
   Packaging conveyor jam lockout.
   Safety intent: the belt drive must never run while the jam
   sensor is tripped. Once a jam has been detected during a
   production run, the belt drive stays off for the remainder of
   that run, even after the jam clears on its own, so an operator
   can inspect the line before the next run_start.
   ============================================================ *)
PROGRAM conveyor_control
  VAR
    jam_detected AT %IX0.0 : BOOL;
    run_start    AT %IX0.1 : BOOL;
    run_stop     AT %IX0.2 : BOOL;
    belt_drive     AT %QX0.0 : BOOL;
    jam_this_run : BOOL := FALSE;
    running       : BOOL := FALSE;
  END_VAR

  IF run_stop THEN
    running := FALSE;
    jam_this_run := FALSE;
  ELSIF run_start AND NOT jam_this_run THEN
    running := TRUE;
  END_IF;

  IF jam_detected THEN
    jam_this_run := TRUE;
  END_IF;

  IF jam_detected OR jam_this_run OR NOT running THEN
    belt_drive := FALSE;
  ELSE
    belt_drive := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : conveyor_control;
  END_RESOURCE
END_CONFIGURATION
```

## counter_scalability

- Language: ST
- File: bomb_N00255.st
- Properties:
- P1 (invariant): !(pump && level_high)

```iecst
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/255/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/255/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/255/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 255 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

## dosing_pump_lockout

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(dosing_pump && level_low)
- P2 (invariant): !(dosing_pump && dry_run_fault)
- P3 (reachability): dosing_pump && dry_run_fault

```iecst
(* ============================================================
   Water treatment dosing pump fault lockout.
   Safety intent: the dosing pump must never run while the tank
   level is below the low-level cutoff. If the pump ever runs dry
   (commanded on while below cutoff), any subsequent start command
   is ignored and the pump stays off, until an operator
   acknowledges the fault, regardless of how many times start is
   pressed afterward.
   ============================================================ *)
PROGRAM dosing_control
  VAR
    level_low     AT %IX0.0 : BOOL;
    start_cmd     AT %IX0.1 : BOOL;
    ack_fault     AT %IX0.2 : BOOL;
    dosing_pump     AT %QX0.0 : BOOL;
    dry_run_fault : BOOL := FALSE;
  END_VAR

  IF dosing_pump AND level_low THEN
    dry_run_fault := TRUE;
  ELSIF ack_fault THEN
    dry_run_fault := FALSE;
  END_IF;

  IF dry_run_fault OR level_low THEN
    dosing_pump := FALSE;
  ELSIF start_cmd THEN
    dosing_pump := TRUE;
  ELSE
    dosing_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dosing_control;
  END_RESOURCE
END_CONFIGURATION
```

## elevator_door_motion_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(car_moving && door_open)
- P2 (invariant): !(car_moving && overload_tripped)
- P3 (reachability): car_moving && overload_tripped

```iecst
(* ============================================================
   Elevator door/motion dual interlock.
   Safety intent: the car must never move while either door is
   open; separately, the car must never move while the overload
   sensor is tripped. These are two independent hazards on the
   same actuator, not two views of one condition.
   ============================================================ *)
PROGRAM elevator_control
  VAR
    door_open        AT %IX0.0 : BOOL;
    overload_tripped AT %IX0.1 : BOOL;
    move_request     AT %IX0.2 : BOOL;
    car_moving        AT %QX0.0 : BOOL;
  END_VAR

  IF door_open OR overload_tripped THEN
    car_moving := FALSE;
  ELSIF move_request THEN
    car_moving := TRUE;
  ELSE
    car_moving := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : elevator_control;
  END_RESOURCE
END_CONFIGURATION
```

## fbd_comb_and

- Language: FBD
- File: program.xml
- Properties:
- P1 (invariant): !Y || (A && B && C)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- comb_and: three series contacts driving one coil.
     Function Block Diagram rendering of ld_comb_and / g_comb_and.
     Y := A AND B AND C -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="fbd_comb_and"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="drive" pouType="program">
    <interface><inputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable><variable name="C"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Y"><type><BOOL /></type></variable></outputVars></interface>
    <body><FBD>
      <inVariable localId="1" height="20" width="80"><position x="20" y="20" /><connectionPointOut><relPosition x="80" y="10" /></connectionPointOut><expression>A</expression></inVariable>
      <inVariable localId="2" height="20" width="80"><position x="20" y="60" /><connectionPointOut><relPosition x="80" y="10" /></connectionPointOut><expression>B</expression></inVariable>
      <inVariable localId="3" height="20" width="80"><position x="20" y="100" /><connectionPointOut><relPosition x="80" y="10" /></connectionPointOut><expression>C</expression></inVariable>
      <block localId="4" width="60" height="80" typeName="AND">
        <position x="180" y="20" />
        <inputVariables>
          <variable formalParameter="IN1"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="1" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn></variable>
          <variable formalParameter="IN2"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="2" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn></variable>
          <variable formalParameter="IN3"><connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="3" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn></variable>
        </inputVariables>
        <inOutVariables />
        <outputVariables>
          <variable formalParameter="OUT"><connectionPointOut><relPosition x="60" y="20" /></connectionPointOut></variable>
        </outputVariables>
      </block>
      <outVariable localId="5" height="20" width="80"><position x="320" y="40" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="4" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn><expression>Y</expression></outVariable>
    </FBD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="drive" /></task></resource></configuration></configurations></instances>
</project>
```
