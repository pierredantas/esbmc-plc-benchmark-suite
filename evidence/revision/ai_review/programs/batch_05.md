# Batch 5: benchmarks g_guard_lock, g_hvac_fan_delay, g_independent_hp_trip, g_motor_interlock, g_packaging_filler, g_phase_hold_permissive, g_ppu_evolution_1, g_pump_alternation

## g_guard_lock

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Unlocked && Motor)

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

## g_hvac_fan_delay

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['heat', 'cool']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_hvac_fan_delay_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_hvac_fan_delay_clean" pouType="program">
      <interface><inputVars><variable name="heat_call"><type><BOOL /></type></variable><variable name="cool_call"><type><BOOL /></type></variable><variable name="enable"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="heat"><type><BOOL /></type></variable><variable name="cool"><type><BOOL /></type></variable><variable name="fan"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>cool_call</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>heat_call</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>enable</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>heat</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>cool_call</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>enable</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="30" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>cool</variable></coil><contact localId="10" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>enable</variable></contact><coil localId="11" negated="false" storage="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>fan</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_hvac_fan_delay_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_independent_hp_trip

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !pressure_high || vent_valve

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_independent_hp_trip_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_independent_hp_trip_clean" pouType="program">
    <interface><inputVars><variable name="pressure_high"><type><BOOL /></type></variable><variable name="sequence_step_active"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="vent_valve"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>pressure_high</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>vent_valve</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_independent_hp_trip_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_motor_interlock

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['Motor_A', 'Motor_B']
- P2 (reachability): Motor_A && Motor_B

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_motor_interlock_clean">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="drive" pouType="program">
        <interface>
          <inputVars>
            <variable name="fwd"><type><BOOL /></type></variable>
            <variable name="rev"><type><BOOL /></type></variable>
            <variable name="maint"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="Motor_A"><type><BOOL /></type></variable>
            <variable name="Motor_B"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="0">
              <position x="0" y="0" />
              <connectionPointOut formalParameter="none" />
            </leftPowerRail>
            <!-- Rung A: Motor_A := fwd AND NOT rev -->
            <contact localId="3" negated="false" storage="none" edge="none">
              <position x="20" y="10" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut />
              <variable>fwd</variable>
            </contact>
            <contact localId="4" negated="true" storage="none" edge="none">
              <position x="40" y="10" />
              <connectionPointIn><connection refLocalId="3" /></connectionPointIn>
              <connectionPointOut />
              <variable>rev</variable>
            </contact>
            <coil localId="5" negated="false" storage="none">
              <position x="60" y="10" />
              <connectionPointIn><connection refLocalId="4" /></connectionPointIn>
              <connectionPointOut />
              <variable>Motor_A</variable>
            </coil>
            <!-- Rung B: Motor_B := rev -->
            <contact localId="6" negated="false" storage="none" edge="none">
              <position x="20" y="30" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut />
              <variable>rev</variable>
            </contact>
            <coil localId="7" negated="false" storage="none">
              <position x="60" y="30" />
              <connectionPointIn><connection refLocalId="6" /></connectionPointIn>
              <connectionPointOut />
              <variable>Motor_B</variable>
            </coil>
            <rightPowerRail localId="2147483646">
              <position x="80" y="0" />
              <connectionPointIn />
            </rightPowerRail>
          </LD>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="drive" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_packaging_filler

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(fill_valve && full)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_packaging_filler_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_packaging_filler_clean" pouType="program">
      <interface><inputVars><variable name="bottle_present"><type><BOOL /></type></variable><variable name="full"><type><BOOL /></type></variable><variable name="start"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="fill_valve"><type><BOOL /></type></variable><variable name="reject"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>full</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>bottle_present</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>start</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>fill_valve</variable></coil><contact localId="7" negated="true" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>bottle_present</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>start</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="30" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>reject</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_packaging_filler_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_phase_hold_permissive

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(held && heater)

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

## g_ppu_evolution_1

- Language: LD-graphical
- File: evolution_1.xml
- Properties:
- P1 (invariant): !Open || (A && B)

```xml
﻿<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Beckhoff Automation GmbH" productName="TwinCAT PLC Control" productVersion="3.5.10.30" creationDateTime="2019-09-26T16:12:41.2429215" />
  <contentHeader name="LD_EVOLUTION_1" modificationDateTime="2019-09-26T16:12:41.2429215">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
    <addData>
      <data name="http://www.3s-software.com/plcopenxml/projectinformation" handleUnknown="implementation">
        <ProjectInformation />
      </data>
    </addData>
  </contentHeader>
  <types>
    <dataTypes />
    <pous />
  </types>
  <instances>
    <configurations />
  </instances>
  <addData>
    <data name="http://www.3s-software.com/plcopenxml/application" handleUnknown="implementation">
      <resource name="LD_EVOLUTION_1">
        <task name="PlcTask" interval="PT0S" priority="20">
          <pouInstance name="Main" typeName="">
            <documentation>
              <xhtml xmlns="http://www.w3.org/1999/xhtml" />
            </documentation>
          </pouInstance>
          <addData>
            <data name="http://www.3s-software.com/plcopenxml/tasksettings" handleUnknown="implementation">
              <TaskSettings KindOfTask="Cyclic" Interval="10000" IntervalUnit="us">
                <Watchdog Enabled="false" TimeUnit="ms" />
              </TaskSettings>
            </data>
            <data name="http://www.3s-software.com/plcopenxml/objectid" handleUnknown="discard">
              <ObjectId>7639a151-d882-4f30-8d0d-8fc980a25c63</ObjectId>
            </data>
          </addData>
        </task>
        <addData>
          <data name="http://www.3s-software.com/plcopenxml/pou" handleUnknown="implementation">
            <pou name="Main" pouType="program">
              <interface>
                <localVars>
                  <variable name="A">
                    <type>
                      <BOOL />
                    </type>
                  </variable>
                  <variable name="B">
                    <type>
                      <BOOL />
                    </type>
                  </variable>
                  <variable name="Open">
                    <type>
                      <BOOL />
                    </type>
                  </variable>
                </localVars>
              </interface>
              <body>
                <LD>
                  <leftPowerRail localId="0">
                    <position x="0" y="0" />
                    <connectionPointOut formalParameter="none" />
                  </leftPowerRail>
                  <comment localId="1" height="0" width="0">
                    <position x="0" y="0" />
                    <content>
                      <xhtml xmlns="http://www.w3.org/1999/xhtml" />
                    </content>
                  </comment>
                  <vendorElement localId="2">
                    <position x="0" y="0" />
                    <alternativeText>
                      <xhtml xmlns="http://www.w3.org/1999/xhtml" />
                    </alternativeText>
                    <addData>
                      <data name="http://www.3s-software.com/plcopenxml/fbdelementtype" handleUnknown="implementation">
                        <ElementType xmlns="">networktitle</ElementType>
                      </data>
                    </addData>
                  </vendorElement>
                  <contact localId="3" negated="false" storage="none" edge="none">
                    <position x="0" y="0" />
                    <connectionPointIn>
                      <connection refLocalId="0" />
                    </connectionPointIn>
                    <connectionPointOut />
                    <variable>A</variable>
                  </contact>
                  <contact localId="4" negated="false" storage="none" edge="none">
                    <position x="0" y="0" />
                    <connectionPointIn>
                      <connection refLocalId="3" />
                    </connectionPointIn>
                    <connectionPointOut />
                    <variable>B</variable>
                  </contact>
                  <coil localId="5" negated="false" storage="none">
                    <position x="0" y="0" />
                    <connectionPointIn>
                      <connection refLocalId="4" />
                    </connectionPointIn>
                    <connectionPointOut />
                    <variable>Open</variable>
                  </coil>
                  <rightPowerRail localId="2147483646">
                    <position x="0" y="0" />
                    <connectionPointIn />
                  </rightPowerRail>
                </LD>
              </body>
              <addData>
                <data name="http://www.3s-software.com/plcopenxml/interfaceasplaintext" handleUnknown="implementation">
                  <InterfaceAsPlainText>
                    <xhtml xmlns="http://www.w3.org/1999/xhtml">PROGRAM Main
VAR
	A: BOOL;
	B: BOOL;
	Open: BOOL;
END_VAR
</xhtml>
                  </InterfaceAsPlainText>
                </data>
                <data name="http://www.3s-software.com/plcopenxml/objectid" handleUnknown="discard">
                  <ObjectId>62ecdd86-aa2a-4ae8-bc9c-e41c0d5d516a</ObjectId>
                </data>
              </addData>
            </pou>
          </data>
          <data name="http://www.3s-software.com/plcopenxml/libraries" handleUnknown="implementation">
            <Libraries>
              <Library Name="#Tc2_Standard" Namespace="Tc2_Standard" HideWhenReferencedAsDependency="false" PublishSymbolsInContainer="false" SystemLibrary="false" LinkAllContent="false" DefaultResolution="Tc2_Standard, * (Beckhoff Automation GmbH)" />
              <Library Name="#Tc2_System" Namespace="Tc2_System" HideWhenReferencedAsDependency="false" PublishSymbolsInContainer="false" SystemLibrary="false" LinkAllContent="false" DefaultResolution="Tc2_System, * (Beckhoff Automation GmbH)">
                <Parameters>
                  <Parameter Name="TABLE_UPPER_BOUND" Value="15" />
                  <Parameter Name="STRING_LENGTH_EXP" Value="255" />
                  <Parameter Name="STRING_LENGTH_ADDRESS" Value="20" />
                  <Parameter Name="STRING_LENGTH_COMMENT" Value="255" />
                  <Parameter Name="STRING_LENGTH_OUTSTRING" Value="255" />
                  <Parameter Name="TABLE_SHOW_VALID_ITEMS" Value="FALSE" />
                </Parameters>
              </Library>
              <Library Name="#Tc3_Module" Namespace="Tc3_Module" HideWhenReferencedAsDependency="false" PublishSymbolsInContainer="false" SystemLibrary="false" LinkAllContent="false" DefaultResolution="Tc3_Module, * (Beckhoff Automation GmbH)" />
              <addData>
                <data name="http://www.3s-software.com/plcopenxml/objectid" handleUnknown="discard">
                  <ObjectId>2d897156-30ad-4570-9c8e-07fd6b7a2f3d</ObjectId>
                </data>
              </addData>
            </Libraries>
          </data>
          <data name="http://www.3s-software.com/plcopenxml/objectid" handleUnknown="discard">
            <ObjectId>86dcef93-a638-40ed-9257-5d8a6dff2c67</ObjectId>
          </data>
        </addData>
      </resource>
    </data>
    <data name="http://www.3s-software.com/plcopenxml/projectstructure" handleUnknown="discard">
      <ProjectStructure>
        <Object Name="Untitled1" ObjectId="86dcef93-a638-40ed-9257-5d8a6dff2c67">
          <Object Name="Bibliotheksverwalter" ObjectId="2d897156-30ad-4570-9c8e-07fd6b7a2f3d" />
          <Folder Name="POUs">
            <Object Name="Main" ObjectId="62ecdd86-aa2a-4ae8-bc9c-e41c0d5d516a" />
          </Folder>
          <Object Name="PlcTask" ObjectId="7639a151-d882-4f30-8d0d-8fc980a25c63" />
        </Object>
      </ProjectStructure>
    </data>
  </addData>
</project>
```

## g_pump_alternation

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (mutual_exclusion): ['PumpA', 'PumpB']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_pump_alternation"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_pump_alternation" pouType="program">
    <interface><inputVars><variable name="LevelHigh"><type><BOOL /></type></variable><variable name="LevelLow"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Call"><type><BOOL /></type></variable><variable name="Duty"><type><BOOL /></type></variable><variable name="PumpA"><type><BOOL /></type></variable><variable name="PumpB"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Call</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>LevelHigh</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>LevelLow</variable></contact><coil localId="6" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>Call</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Duty</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>LevelLow</variable></contact><contact localId="9" negated="true" storage="none" edge="none"><position x="20" y="60" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Duty</variable></contact><contact localId="10" negated="false" storage="none" edge="none"><position x="40" y="60" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>LevelLow</variable></contact><coil localId="11" negated="false" storage="none"><position x="60" y="50" /><connectionPointIn><connection refLocalId="8" /><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Duty</variable></coil><contact localId="12" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Call</variable></contact><contact localId="13" negated="true" storage="none" edge="none"><position x="40" y="90" /><connectionPointIn><connection refLocalId="12" /></connectionPointIn><connectionPointOut /><variable>Duty</variable></contact><coil localId="14" negated="false" storage="none"><position x="60" y="90" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>PumpA</variable></coil><contact localId="15" negated="false" storage="none" edge="none"><position x="20" y="120" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Call</variable></contact><contact localId="16" negated="false" storage="none" edge="none"><position x="40" y="120" /><connectionPointIn><connection refLocalId="15" /></connectionPointIn><connectionPointOut /><variable>Duty</variable></contact><coil localId="17" negated="false" storage="none"><position x="60" y="120" /><connectionPointIn><connection refLocalId="16" /></connectionPointIn><connectionPointOut /><variable>PumpB</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_pump_alternation" /></task></resource></configuration></configurations></instances>
</project>
```
