# Batch 9: benchmarks g_vessel_empty_permissive, hoist_overload_cutoff, il_comb_and, il_counter_reset, il_seal_in, intrusion_dual_alarm, kiln_door_lockout, ld_comb_and

## g_vessel_empty_permissive

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['feed_valve', 'discharge_valve']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_vessel_empty_permissive_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_vessel_empty_permissive_clean" pouType="program">
    <interface><inputVars><variable name="feed_cmd"><type><BOOL /></type></variable><variable name="discharge_cmd"><type><BOOL /></type></variable><variable name="vessel_empty"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="feed_valve"><type><BOOL /></type></variable><variable name="discharge_valve"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>discharge_cmd</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>vessel_empty</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>feed_cmd</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>feed_valve</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>discharge_cmd</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>vessel_empty</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="30" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>discharge_valve</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_vessel_empty_permissive_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## hoist_overload_cutoff

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(overload_tripped && hoist_raise)
- P2 (reachability): overload_tripped && hoist_raise

```iecst
(* ============================================================
   Crane hoist overload cutoff : demo program, not in the suite.
   Safety intent: the hoist motor must never raise the load while
   the overload sensor is tripped, regardless of the operator's
   raise command.
   ============================================================ *)
PROGRAM hoist_control
  VAR
    overload_tripped AT %IX0.0 : BOOL;
    raise_command    AT %IX0.1 : BOOL;
    lower_command    AT %IX0.2 : BOOL;
    hoist_raise       AT %QX0.0 : BOOL;
    hoist_lower       AT %QX0.1 : BOOL;
  END_VAR

  IF overload_tripped THEN
    hoist_raise := FALSE;
  ELSIF raise_command AND NOT lower_command THEN
    hoist_raise := TRUE;
  ELSE
    hoist_raise := FALSE;
  END_IF;

  hoist_lower := lower_command AND NOT raise_command;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : hoist_control;
  END_RESOURCE
END_CONFIGURATION
```

## il_comb_and

- Language: IL
- File: comb_and.il
- Properties:
- P1 (invariant): !Y || (A && B && C)

```text
(* comb_and: three series contacts driving one coil.
   Instruction List rendering of ld_comb_and / g_comb_and.
   Y := A AND B AND C *)
PROGRAM drive
  VAR_INPUT
    A : BOOL;
    B : BOOL;
    C : BOOL;
  END_VAR
  VAR_OUTPUT
    Y : BOOL;
  END_VAR

      LD    A
      AND   B
      AND   C
      ST    Y
END_PROGRAM
```

## il_counter_reset

- Language: IL
- File: counter_reset.il
- Properties:
- P1 (invariant): !Reset || (OUT == ResetCounterValue)

```text
(* counter_reset: a free-running counter with a reset-to-value.
   Reset loads ResetCounterValue, otherwise Cnt increments; OUT follows Cnt.
   Imported from the Beremiz IEC 61131-3 language test (CounterIL function block),
   re-expressed as a PROGRAM so it stands alone. See benchmark.yml for provenance. *)
PROGRAM drive
  VAR_INPUT
    Reset : BOOL;
    ResetCounterValue : INT;
  END_VAR
  VAR_OUTPUT
    OUT : INT;
  END_VAR
  VAR
    Cnt : INT;
  END_VAR

      LD    Reset
      JMPC  ResetCnt

      LD    Cnt
      ADD   1
      JMP   QuitFb

ResetCnt:
      LD    ResetCounterValue

QuitFb:
      ST    Cnt
      ST    OUT
END_PROGRAM
```

## il_seal_in

- Language: IL
- File: seal_in.il
- Properties:
- P1 (invariant): !Run || !Stop

```text
(* seal_in: self-holding (seal-in) coil with stop.
   Instruction List rendering of ld_seal_in / g_seal_in.
   Deprecated in IEC 61131-3 edition 3.0 (2013) and removed in
   edition 4.0 (2025); kept here because deployed plants still run it.
   Run := (Start OR Run) AND NOT Stop *)
PROGRAM drive
  VAR_INPUT
    Start : BOOL;
    Stop  : BOOL;
  END_VAR
  VAR_OUTPUT
    Run : BOOL;
  END_VAR

      LD    Start
      OR    Run
      ANDN  Stop
      ST    Run
END_PROGRAM
```

## intrusion_dual_alarm

- Language: LD-textual
- File: clean.ld
- Properties:
- P1 (invariant): sensor_trip -> siren_out
- P2 (reachability): sensor_trip && !siren_out

```text
// Intrusion latch with dual annunciation – clean
OTE(alarm_state) := XIC(sensor_trip) + (XIC(alarm_state) * XIO(guard_ack)) ;
OTE(siren_out) := XIC(alarm_state) ;
OTE(door_lock) := XIC(alarm_state) + XIC(lock_req) ;
```

## kiln_door_lockout

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(heater_element && door_open)
- P2 (invariant): !(heater_element && door_fault_latched)
- P3 (reachability): heater_element && door_fault_latched

```iecst
(* ============================================================
   Industrial kiln door safety latch : demo program, not in the
   suite.
   Safety intent: the heating element must never be energised
   while the kiln door is open; once the door has been opened
   during a heat cycle, the element stays locked out even after
   the door closes again, until an operator explicitly resets it.
   ============================================================ *)
PROGRAM kiln_control
  VAR
    door_open     AT %IX0.0 : BOOL;
    heat_request  AT %IX0.1 : BOOL;
    reset_button  AT %IX0.2 : BOOL;
    heater_element AT %QX0.0 : BOOL;
    door_fault_latched : BOOL := FALSE;
  END_VAR

  IF door_open THEN
    door_fault_latched := TRUE;
  ELSIF reset_button THEN
    door_fault_latched := FALSE;
  END_IF;

  IF door_fault_latched OR door_open THEN
    heater_element := FALSE;
  ELSIF heat_request THEN
    heater_element := TRUE;
  ELSE
    heater_element := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : kiln_control;
  END_RESOURCE
END_CONFIGURATION
```

## ld_comb_and

- Language: LD-textual
- File: comb_and.ld
- Properties:
- P1 (invariant): !Y || (A && B && C)

```text
// comb_and: series contacts (AND) -> coil
OTE(Y) := XIC(A) * XIC(B) * XIC(C) ;
```
