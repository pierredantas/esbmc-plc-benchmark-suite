# Batch 1: g_burner_purge, g_door_reversal, g_estop_reset, g_guard_lock, g_phase_hold_permissive, g_two_hand

## g_burner_purge

- Language: LD-graphical
- Clause cited by the descriptor: Authored from the light-off order in EN 298: purge, prove flame, then admit main gas, with a lockout that needs a manual reset
- Safety intent: The main gas valve must open only after the purge has completed and the flame is proven.
- Property (checked and holds): P1: !MainValve || (PurgeDone && FlameProven)  (EN 298 light-off order: the main gas valve opens only after the purge has completed and the flame is proven.)
- Discriminator `lockout_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: !Lockout || FlameFail  (Lockout holds only while the flame fault is present. A latching lockout must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_burner_purge"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_burner_purge" pouType="program">
    <interface><inputVars><variable name="CallForHeat"><type><BOOL /></type></variable><variable name="PurgeDone"><type><BOOL /></type></variable><variable name="FlameProven"><type><BOOL /></type></variable><variable name="FlameFail"><type><BOOL /></type></variable><variable name="ResetBtn"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Fan"><type><BOOL /></type></variable><variable name="Lockout"><type><BOOL /></type></variable><variable name="Pilot"><type><BOOL /></type></variable><variable name="MainValve"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Fan</variable></coil><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>FlameFail</variable></contact><contact localId="7" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="5" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>ResetBtn</variable></contact><coil localId="8" negated="false" storage="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></coil><contact localId="9" negated="false" storage="none" edge="none"><position x="20" y="80" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><contact localId="10" negated="false" storage="none" edge="none"><position x="40" y="80" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>PurgeDone</variable></contact><contact localId="11" negated="true" storage="none" edge="none"><position x="60" y="80" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><coil localId="12" negated="false" storage="none"><position x="80" y="80" /><connectionPointIn><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>Pilot</variable></coil><contact localId="13" negated="false" storage="none" edge="none"><position x="20" y="110" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><contact localId="14" negated="false" storage="none" edge="none"><position x="40" y="110" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>PurgeDone</variable></contact><contact localId="15" negated="false" storage="none" edge="none"><position x="60" y="110" /><connectionPointIn><connection refLocalId="14" /></connectionPointIn><connectionPointOut /><variable>FlameProven</variable></contact><contact localId="16" negated="true" storage="none" edge="none"><position x="80" y="110" /><connectionPointIn><connection refLocalId="15" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><coil localId="17" negated="false" storage="none"><position x="100" y="110" /><connectionPointIn><connection refLocalId="16" /></connectionPointIn><connectionPointOut /><variable>MainValve</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_burner_purge" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_burner_purge: Fan := CallForHeat
g_burner_purge: Lockout := ((FlameFail OR Lockout) AND NOT ResetBtn)
g_burner_purge: Pilot := ((((CallForHeat) AND PurgeDone)) AND NOT Lockout)
g_burner_purge: MainValve := ((((((CallForHeat) AND PurgeDone)) AND FlameProven)) AND NOT Lockout)
```

Mutants that no property kills (9):

- S1: contact CallForHeat (feeds Fan) negated false->true
- S2: contact Lockout (feeds Lockout) negated false->true
- S3: contact FlameFail (feeds Lockout) negated false->true
- S4: contact ResetBtn (feeds Lockout) negated true->false
- S5: contact CallForHeat (feeds Pilot) negated false->true
- S6: contact PurgeDone (feeds Pilot) negated false->true
- S7: contact Lockout (feeds Pilot) negated true->false
- S8: contact CallForHeat (feeds MainValve) negated false->true
- S9: contact Lockout (feeds MainValve) negated true->false

## g_door_reversal

- Language: LD-graphical
- Clause cited by the descriptor: Authored from the reversal requirement for power-operated doors in EN 13241: an obstruction sends the door back to open rather than pausing it
- Safety intent: The door must never drive down while the photo-eye beam is broken.
- Property (checked and holds): P1: !(MoveDown && Beam)  (The door never drives down while the photo-eye beam is broken.)
- Discriminator `reversal_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: !Reversing || Beam  (Reversal lasts only while the beam is broken. A latched reversal must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_door_reversal"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_door_reversal" pouType="program">
    <interface><inputVars><variable name="CloseCmd"><type><BOOL /></type></variable><variable name="OpenCmd"><type><BOOL /></type></variable><variable name="Beam"><type><BOOL /></type></variable><variable name="TopLimit"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Reversing"><type><BOOL /></type></variable><variable name="MoveDown"><type><BOOL /></type></variable><variable name="MoveUp"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Reversing</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Beam</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>TopLimit</variable></contact><coil localId="6" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>Reversing</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CloseCmd</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>Beam</variable></contact><contact localId="9" negated="true" storage="none" edge="none"><position x="60" y="50" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Reversing</variable></contact><coil localId="10" negated="false" storage="none"><position x="80" y="50" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>MoveDown</variable></coil><contact localId="11" negated="false" storage="none" edge="none"><position x="20" y="80" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>OpenCmd</variable></contact><contact localId="12" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Reversing</variable></contact><coil localId="13" negated="false" storage="none"><position x="40" y="80" /><connectionPointIn><connection refLocalId="11" /><connection refLocalId="12" /></connectionPointIn><connectionPointOut /><variable>MoveUp</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_door_reversal" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_door_reversal: Reversing := ((Beam OR Reversing) AND NOT TopLimit)
g_door_reversal: MoveDown := ((((CloseCmd) AND NOT Beam)) AND NOT Reversing)
g_door_reversal: MoveUp := OpenCmd OR Reversing
```

Mutants that no property kills (7):

- S1: contact Reversing (feeds Reversing) negated false->true
- S2: contact Beam (feeds Reversing) negated false->true
- S3: contact TopLimit (feeds Reversing) negated true->false
- S4: contact CloseCmd (feeds MoveDown) negated false->true
- S5: contact Reversing (feeds MoveDown) negated true->false
- S6: contact OpenCmd (feeds MoveUp) negated false->true
- S7: contact Reversing (feeds MoveUp) negated false->true

## g_estop_reset

- Language: LD-graphical
- Clause cited by the descriptor: Authored from the reset requirement in ISO 13850 and ISO 13849-1: the safety function is restored by a separate manual action, never by releasing the actuator
- Safety intent: The drive must never be energised while the emergency stop is actuated.
- Property (checked and holds): P1: !(Run && EStop)  (ISO 13850 stop function: the drive is never energised while the emergency stop is actuated.)
- Discriminator `restart_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: Safe || EStop  (The safety function is available whenever the emergency stop is clear. A monitored reset must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_estop_reset"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_estop_reset" pouType="program">
    <interface><inputVars><variable name="EStop"><type><BOOL /></type></variable><variable name="Reset"><type><BOOL /></type></variable><variable name="Start"><type><BOOL /></type></variable></inputVars><outputVars><variable name="ResetEdge"><type><BOOL /></type></variable><variable name="Safe"><type><BOOL /></type></variable><variable name="Run"><type><BOOL /></type></variable><variable name="Reset_prev"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Reset_prev</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Reset</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>ResetEdge</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Safe</variable></contact><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>ResetEdge</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="60" y="30" /><connectionPointIn><connection refLocalId="6" /><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>EStop</variable></contact><coil localId="9" negated="false" storage="none"><position x="80" y="30" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Safe</variable></coil><contact localId="10" negated="false" storage="none" edge="none"><position x="20" y="60" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Safe</variable></contact><contact localId="11" negated="false" storage="none" edge="none"><position x="40" y="60" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Start</variable></contact><contact localId="15" negated="true" storage="none" edge="none"><position x="60" y="60" /><connectionPointIn><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>EStop</variable></contact><coil localId="12" negated="false" storage="none"><position x="80" y="60" /><connectionPointIn><connection refLocalId="15" /></connectionPointIn><connectionPointOut /><variable>Run</variable></coil><contact localId="13" negated="false" storage="none" edge="none"><position x="20" y="80" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Reset</variable></contact><coil localId="14" negated="false" storage="none"><position x="40" y="80" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>Reset_prev</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_estop_reset" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_estop_reset: ResetEdge := ((Reset_prev) AND NOT Reset)
g_estop_reset: Safe := ((ResetEdge OR Safe) AND NOT EStop)
g_estop_reset: Run := ((((Safe) AND Start)) AND NOT EStop)
g_estop_reset: Reset_prev := Reset
```

Mutants that no property kills (9):

- S1: contact Reset_prev (feeds ResetEdge) negated false->true
- S2: contact Reset (feeds ResetEdge) negated true->false
- S3: contact Safe (feeds Safe) negated false->true
- S4: contact ResetEdge (feeds Safe) negated false->true
- S5: contact EStop (feeds Safe) negated true->false
- S6: contact Safe (feeds Run) negated false->true
- S7: contact Start (feeds Run) negated false->true
- S8: contact EStop (feeds Run) negated true->false
- S9: contact Reset (feeds Reset_prev) negated false->true

## g_guard_lock

- Language: LD-graphical
- Clause cited by the descriptor: Authored from the guard-locking requirement in ISO 14119: the guard stays locked until the hazardous movement has stopped, not until the drive command drops
- Safety intent: The safety guard must never be released while the drive is energised.
- Property (checked and holds): P1: !(Unlocked && Motor)  (ISO 14119 guard locking: the guard is never released while the drive is energised.)
- Discriminator `rundown_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: !OpenReq || Motor || Unlocked  (A request with the drive already stopped always releases the guard. Guard locking must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_guard_lock"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_guard_lock" pouType="program">
    <interface><inputVars><variable name="OpenReq"><type><BOOL /></type></variable><variable name="DoorClosed"><type><BOOL /></type></variable><variable name="RunCmd"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Motor"><type><BOOL /></type></variable><variable name="Unlocked"><type><BOOL /></type></variable></outputVars><localVars><variable name="Rundown"><type><derived name="TON" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Motor</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#30ms</expression></inVariable>
      <block localId="5" width="80" height="60" typeName="TON" instanceName="Rundown">
        <position x="60" y="10" />
        <inputVariables>
          <variable formalParameter="IN"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable>
          <variable formalParameter="PT"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable>
        </inputVariables>
        <inOutVariables />
        <outputVariables>
          <variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable>
          <variable formalParameter="ET"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable>
        </outputVariables>
      </block>
      <contact localId="6" negated="false" storage="none" edge="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact>
      <coil localId="7" negated="false" storage="none"><position x="200" y="10" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>Unlocked</variable></coil>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="100" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>RunCmd</variable></contact><contact localId="9" negated="false" storage="none" edge="none"><position x="40" y="100" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>DoorClosed</variable></contact><contact localId="10" negated="true" storage="none" edge="none"><position x="60" y="100" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact><coil localId="11" negated="false" storage="none"><position x="80" y="100" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Motor</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_guard_lock" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_guard_lock: Unlocked := ((TON(IN=NOT Motor, PT=T#30ms)) AND OpenReq)
g_guard_lock: Motor := ((((RunCmd) AND DoorClosed)) AND NOT OpenReq)
```

Mutants that no property kills (3):

- S1: contact Motor (feeds Unlocked) negated true->false
- S2: contact RunCmd (feeds Motor) negated false->true
- S3: contact DoorClosed (feeds Motor) negated false->true

## g_phase_hold_permissive

- Language: LD-graphical
- Clause cited by the descriptor: Authored for this suite, modeling an ISA-88 phase HELD state entered on agitator-permissive loss
- Safety intent: A phase held on permissive loss must keep the heater off; only explicitly clearing the hold may re-enable heating.
- Property (checked and holds): P1: !(held && heater)  (A phase held on permissive loss must keep the heater off; only clearing HELD through resume_command may re-enable heating.)

Program `clean.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_phase_hold_permissive_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_phase_hold_permissive_clean" pouType="program">
    <interface><inputVars><variable name="run_command"><type><BOOL /></type></variable><variable name="agitator_ok"><type><BOOL /></type></variable><variable name="resume_command"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="held"><type><BOOL /></type></variable><variable name="heater"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="6" negated="true" storage="none" edge="none"><position x="40" y="20" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>resume_command</variable></contact><coil localId="7" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>held</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="9" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="13" negated="false" storage="none" edge="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><coil localId="10" negated="false" storage="none"><position x="80" y="40" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>heater</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_phase_hold_permissive_clean" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_phase_hold_permissive_clean: held := ((held) AND NOT resume_command) OR ((run_command) AND NOT agitator_ok)
g_phase_hold_permissive_clean: heater := ((((run_command) AND NOT held)) AND agitator_ok)
```

Mutants that no property kills (6):

- S1: contact run_command (feeds held) negated false->true
- S2: contact agitator_ok (feeds held) negated true->false
- S3: contact held (feeds held) negated false->true
- S4: contact resume_command (feeds held) negated true->false
- S5: contact run_command (feeds heater) negated false->true
- S6: contact agitator_ok (feeds heater) negated false->true

## g_two_hand

- Language: LD-graphical
- Clause cited by the descriptor: Authored from the Type II requirements in ISO 13851: synchronous actuation, anti-tie-down and anti-repeat, so a taped actuator cannot start a cycle
- Safety intent: The ram must descend only while both hand actuators are held; releasing either one must stop the stroke.
- Property (checked and holds): P1: !Stroke || (LH && RH)  (ISO 13851 requires the ram to descend only while both actuators are held. Releasing either one stops the stroke.)
- Discriminator `tiedown_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: !(LH && RH) || Stroke  (Both actuators held always produces a stroke. A Type II device with anti-tie-down must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_two_hand"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_two_hand" pouType="program">
    <interface><inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars><outputVars><variable name="BothOff"><type><BOOL /></type></variable><variable name="Armed"><type><BOOL /></type></variable><variable name="Stroke"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>LH</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>RH</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>BothOff</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Armed</variable></contact><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>BothOff</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="6" /><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>Stroke</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Armed</variable></coil><contact localId="10" negated="false" storage="none" edge="none"><position x="20" y="80" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Stroke</variable></contact><contact localId="11" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Armed</variable></contact><contact localId="12" negated="false" storage="none" edge="none"><position x="40" y="80" /><connectionPointIn><connection refLocalId="10" /><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>LH</variable></contact><contact localId="13" negated="false" storage="none" edge="none"><position x="60" y="80" /><connectionPointIn><connection refLocalId="12" /></connectionPointIn><connectionPointOut /><variable>RH</variable></contact><coil localId="14" negated="false" storage="none"><position x="80" y="80" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>Stroke</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_two_hand" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```
g_two_hand: BothOff := ((NOT LH) AND NOT RH)
g_two_hand: Armed := ((Armed OR BothOff) AND NOT Stroke)
g_two_hand: Stroke := ((((Armed OR Stroke) AND LH)) AND RH)
```

Mutants that no property kills (6):

- S1: contact LH (feeds BothOff) negated true->false
- S2: contact RH (feeds BothOff) negated true->false
- S3: contact Armed (feeds Armed) negated false->true
- S4: contact Stroke (feeds Armed) negated true->false
- S5: contact Stroke (feeds Stroke) negated false->true
- S6: contact Armed (feeds Stroke) negated false->true
