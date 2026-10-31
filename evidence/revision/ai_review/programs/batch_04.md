# Batch 4: benchmarks g_ctu_saturate, g_dead_bus_close_check, g_door_reversal, g_elevator_door, g_estop_reset, g_failsafe_motor_latch, g_ftrig_edge, g_fwd_rev_interlock

## g_ctu_saturate

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Done && Reset)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Carton counter: count product pulses up to a preset and latch Done.
     Reset is dominant and clears the count. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_ctu_saturate"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_ctu_saturate" pouType="program">
    <interface><inputVars><variable name="Pulse"><type><BOOL /></type></variable><variable name="Reset"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Done"><type><BOOL /></type></variable></outputVars><localVars><variable name="CTU0"><type><derived name="CTU" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Pulse</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>2</expression></inVariable>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Reset</variable></contact>
      <block localId="5" width="80" height="80" typeName="CTU" instanceName="CTU0"><position x="60" y="10" /><inputVariables><variable formalParameter="CU"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PV"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable><variable formalParameter="R"><connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="8" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="CV"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <coil localId="6" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Done</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_ctu_saturate" /></task></resource></configuration></configurations></instances>
</project>
```

## g_dead_bus_close_check

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !breaker_close || !bus_live || sync_check_ok

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_dead_bus_close_check_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_dead_bus_close_check_clean" pouType="program">
    <interface><inputVars><variable name="close_request"><type><BOOL /></type></variable><variable name="bus_live"><type><BOOL /></type></variable><variable name="sync_check_ok"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="breaker_close"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>close_request</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>bus_live</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>close_request</variable></contact><contact localId="6" negated="false" storage="none" edge="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>sync_check_ok</variable></contact><coil localId="7" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="4" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>breaker_close</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_dead_bus_close_check_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_door_reversal

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(MoveDown && Beam)

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

## g_elevator_door

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['door_open', 'drive']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_elevator_door_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_elevator_door_clean" pouType="program">
      <interface><inputVars><variable name="open_req"><type><BOOL /></type></variable><variable name="move_req"><type><BOOL /></type></variable><variable name="at_floor"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="door_open"><type><BOOL /></type></variable><variable name="drive"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>move_req</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>open_req</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>at_floor</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>door_open</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>move_req</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>drive</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_elevator_door_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_estop_reset

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Run && EStop)

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

## g_failsafe_motor_latch

- Language: LD-graphical
- File: failsafe_motor_latch.xml
- Properties:
- P1 (invariant): THERMAL_OVERLOAD_NC || !MOTOR_RUN

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="Lessons in Electric Circuits transcription" productVersion="1" creationDateTime="2026-09-02T12:00:00"/>
  <contentHeader name="failsafe_motor_latch">
    <coordinateInfo>
      <fbd><scaling x="1" y="1"/></fbd>
      <ld><scaling x="1" y="1"/></ld>
      <sfc><scaling x="1" y="1"/></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="main" pouType="program">
        <interface>
          <localVars>
            <variable name="START"><type><BOOL/></type></variable>
            <variable name="THERMAL_OVERLOAD_NC"><type><BOOL/></type></variable>
            <variable name="STOP_NC"><type><BOOL/></type></variable>
            <variable name="MOTOR_RUN"><type><BOOL/></type></variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="100">
              <position x="0" y="0"/>
              <connectionPointOut formalParameter=""/>
            </leftPowerRail>
            <rightPowerRail localId="200">
              <position x="100" y="0"/>
              <connectionPointIn>
                <connection refLocalId="5"/>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="1">
              <position x="10" y="0"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>START</variable>
            </contact>
            <contact localId="2">
              <position x="10" y="10"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>MOTOR_RUN</variable>
            </contact>
            <contact localId="3">
              <position x="20" y="0"/>
              <connectionPointIn>
                <connection refLocalId="1"/>
                <connection refLocalId="2"/>
              </connectionPointIn>
              <connectionPointOut/>
              <variable>THERMAL_OVERLOAD_NC</variable>
            </contact>
            <contact localId="4">
              <position x="30" y="0"/>
              <connectionPointIn><connection refLocalId="3"/></connectionPointIn>
              <connectionPointOut/>
              <variable>STOP_NC</variable>
            </contact>
            <coil localId="5">
              <position x="40" y="0"/>
              <connectionPointIn><connection refLocalId="4"/></connectionPointIn>
              <connectionPointOut/>
              <variable>MOTOR_RUN</variable>
            </coil>
          </LD>
        </body>
      </pou>
    </pous>
  </types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="main" /></task></resource></configuration></configurations></instances>
</project>
```

## g_ftrig_edge

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !OneShot || !Sig

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_ftrig_edge"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_ftrig_edge" pouType="program">
    <interface><inputVars><variable name="Sig"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Fall"><type><BOOL /></type></variable><variable name="OneShot"><type><BOOL /></type></variable><variable name="Sig_prev"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Sig</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Sig_prev</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>Fall</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Fall</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>OneShot</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Sig</variable></contact><coil localId="9" negated="false" storage="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Sig_prev</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_ftrig_edge" /></task></resource></configuration></configurations></instances>
</project>
```

## g_fwd_rev_interlock

- Language: LD-graphical
- File: fwd_rev_interlock.xml
- Properties:
- P1 (invariant): !(M1_FWD && M2_REV)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="Lessons in Electric Circuits transcription" productVersion="1" creationDateTime="2026-09-02T12:00:00"/>
  <contentHeader name="fwd_rev_interlock">
    <coordinateInfo>
      <fbd><scaling x="1" y="1"/></fbd>
      <ld><scaling x="1" y="1"/></ld>
      <sfc><scaling x="1" y="1"/></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="main" pouType="program">
        <interface>
          <localVars>
            <variable name="START_FWD"><type><BOOL/></type></variable>
            <variable name="START_REV"><type><BOOL/></type></variable>
            <variable name="STOP"><type><BOOL/></type></variable>
            <variable name="M1_FWD"><type><BOOL/></type></variable>
            <variable name="M2_REV"><type><BOOL/></type></variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="100">
              <position x="0" y="0"/>
              <connectionPointOut formalParameter=""/>
            </leftPowerRail>
            <rightPowerRail localId="200">
              <position x="100" y="0"/>
              <connectionPointIn>
                <connection refLocalId="5"/>
                <connection refLocalId="10"/>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="1">
              <position x="10" y="0"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>START_FWD</variable>
            </contact>
            <contact localId="2">
              <position x="10" y="10"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M1_FWD</variable>
            </contact>
            <contact localId="3" negated="true">
              <position x="20" y="0"/>
              <connectionPointIn>
                <connection refLocalId="1"/>
                <connection refLocalId="2"/>
              </connectionPointIn>
              <connectionPointOut/>
              <variable>STOP</variable>
            </contact>
            <contact localId="4" negated="true">
              <position x="30" y="0"/>
              <connectionPointIn><connection refLocalId="3"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M2_REV</variable>
            </contact>
            <coil localId="5">
              <position x="40" y="0"/>
              <connectionPointIn><connection refLocalId="4"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M1_FWD</variable>
            </coil>
            <contact localId="6">
              <position x="10" y="20"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>START_REV</variable>
            </contact>
            <contact localId="7">
              <position x="10" y="30"/>
              <connectionPointIn><connection refLocalId="100"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M2_REV</variable>
            </contact>
            <contact localId="8" negated="true">
              <position x="20" y="20"/>
              <connectionPointIn>
                <connection refLocalId="6"/>
                <connection refLocalId="7"/>
              </connectionPointIn>
              <connectionPointOut/>
              <variable>STOP</variable>
            </contact>
            <contact localId="9" negated="true">
              <position x="30" y="20"/>
              <connectionPointIn><connection refLocalId="8"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M1_FWD</variable>
            </contact>
            <coil localId="10">
              <position x="40" y="20"/>
              <connectionPointIn><connection refLocalId="9"/></connectionPointIn>
              <connectionPointOut/>
              <variable>M2_REV</variable>
            </coil>
          </LD>
        </body>
      </pou>
    </pous>
  </types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="main" /></task></resource></configuration></configurations></instances>
</project>
```
