# Batch 3: benchmarks g_bus_coupler_changeover, g_busbar_interlock, g_comb_and, g_comb_mixed, g_comb_or, g_compressor_cycle, g_conveyor_interlock, g_ctd_load

## g_bus_coupler_changeover

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(incomer_a && incomer_b && coupler)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_bus_coupler_changeover_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_bus_coupler_changeover_clean" pouType="program">
    <interface><inputVars><variable name="incomer_a_healthy"><type><BOOL /></type></variable><variable name="incomer_b_healthy"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="incomer_a"><type><BOOL /></type></variable><variable name="incomer_b"><type><BOOL /></type></variable><variable name="coupler"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>incomer_a</variable></coil><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><coil localId="6" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>incomer_b</variable></coil><contact localId="7" negated="true" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="50" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>coupler</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_bus_coupler_changeover_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_busbar_interlock

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['feeder_a', 'feeder_b']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_busbar_interlock_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_busbar_interlock_clean" pouType="program">
    <interface><inputVars><variable name="feeder_a_cmd"><type><BOOL /></type></variable><variable name="feeder_b_cmd"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="feeder_a"><type><BOOL /></type></variable><variable name="feeder_b"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>feeder_b_cmd</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>feeder_a_cmd</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>feeder_a</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>feeder_b_cmd</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>feeder_b</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_busbar_interlock_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_comb_and

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Y || (A && B && C)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_comb_and"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_comb_and" pouType="program">
    <interface><inputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable><variable name="C"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Y"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>A</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>B</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>C</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>Y</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_comb_and" /></task></resource></configuration></configurations></instances>
</project>
```

## g_comb_mixed

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Y || A || C

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_comb_mixed"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_comb_mixed" pouType="program">
    <interface><inputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable><variable name="C"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Y"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>A</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>B</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>C</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="4" /><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>Y</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_comb_mixed" /></task></resource></configuration></configurations></instances>
</project>
```

## g_comb_or

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Y || A || B

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_comb_or"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_comb_or" pouType="program">
    <interface><inputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Y"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>A</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>B</variable></contact><coil localId="5" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>Y</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_comb_or" /></task></resource></configuration></configurations></instances>
</project>
```

## g_compressor_cycle

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Load && PressHigh)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_compressor_cycle"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_compressor_cycle" pouType="program">
    <interface><inputVars><variable name="PressLow"><type><BOOL /></type></variable><variable name="PressHigh"><type><BOOL /></type></variable><variable name="MinOffDone"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Load"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Load</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>PressLow</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="40" y="20" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>MinOffDone</variable></contact><contact localId="6" negated="true" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>PressHigh</variable></contact><coil localId="7" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>Load</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_compressor_cycle" /></task></resource></configuration></configurations></instances>
</project>
```

## g_conveyor_interlock

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(conveyor && estop)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_conveyor_interlock_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_conveyor_interlock_clean" pouType="program">
    <interface><inputVars><variable name="run_cmd"><type><BOOL /></type></variable><variable name="estop"><type><BOOL /></type></variable><variable name="guard_open"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="conveyor"><type><BOOL /></type></variable><variable name="warn"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>estop</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>run_cmd</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>guard_open</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>conveyor</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>estop</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>warn</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_conveyor_interlock_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_ctd_load

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Empty && Load)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Car call queue: count served calls down to zero and flag Empty.
     Load restores the preset when a new batch of calls arrives. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_ctd_load"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_ctd_load" pouType="program">
    <interface><inputVars><variable name="Pulse"><type><BOOL /></type></variable><variable name="Load"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Empty"><type><BOOL /></type></variable></outputVars><localVars><variable name="CTD0"><type><derived name="CTD" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Pulse</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>2</expression></inVariable>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Load</variable></contact>
      <block localId="5" width="80" height="80" typeName="CTD" instanceName="CTD0"><position x="60" y="10" /><inputVariables><variable formalParameter="CD"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PV"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable><variable formalParameter="LD"><connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="8" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="CV"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <coil localId="6" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Empty</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_ctd_load" /></task></resource></configuration></configurations></instances>
</project>
```
