# Batch 6: benchmarks g_rtrig_edge, g_seal_in, g_star_delta, g_start_cycle, g_stop_eq, g_substation_breaker, g_tank_assignment, g_tank_start_eq

## g_rtrig_edge

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !OneShot || Sig

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_rtrig_edge"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_rtrig_edge" pouType="program">
    <interface><inputVars><variable name="Sig"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Rise"><type><BOOL /></type></variable><variable name="OneShot"><type><BOOL /></type></variable><variable name="Sig_prev"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Sig</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Sig_prev</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>Rise</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Rise</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>OneShot</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Sig</variable></contact><coil localId="9" negated="false" storage="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Sig_prev</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_rtrig_edge" /></task></resource></configuration></configurations></instances>
</project>
```

## g_seal_in

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Run || !Stop

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_seal_in"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_seal_in" pouType="program">
    <interface><inputVars><variable name="Start"><type><BOOL /></type></variable><variable name="Stop"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Run"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Start</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Run</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>Stop</variable></contact><coil localId="6" negated="false" storage="none"><position x="100" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>Run</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_seal_in" /></task></resource></configuration></configurations></instances>
</project>
```

## g_star_delta

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (mutual_exclusion): ['Star', 'Delta']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_star_delta"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_star_delta" pouType="program">
    <interface><inputVars><variable name="Call"><type><BOOL /></type></variable><variable name="StarDone"><type><BOOL /></type></variable><variable name="DeadDone"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Star"><type><BOOL /></type></variable><variable name="Delta"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Call</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>StarDone</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>Star</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Call</variable></contact><contact localId="7" negated="false" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>StarDone</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>DeadDone</variable></contact><coil localId="9" negated="false" storage="none"><position x="80" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Delta</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_star_delta" /></task></resource></configuration></configurations></instances>
</project>
```

## g_start_cycle

- Language: LD-graphical
- File: lstart_cycle.xml
- Properties:
- P1 (invariant): !(STOP && CYCLE_ON)
- P2 (invariant): !(START && STOP && CYCLE_ON)

```xml
<?xml version='1.0' encoding='utf-8'?>
<!-- fileHeader and contentHeader synthesised 2026-09-01. The program arrived
     from the PLC-LD-dataset with neither, and without the PLCopen
     namespace, so no conforming importer would recognise it as PLCopen XML.
     Only these headers and the namespace were added; the POUs, the ladder
     bodies and the configuration are untouched. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="PLC-LD-dataset" productVersion="1.0" creationDateTime="2024-01-01T00:00:00" />
  <contentHeader name="lstart_cycle">
    <coordinateInfo>
      <fbd><scaling x="1" y="1" /></fbd>
      <ld><scaling x="1" y="1" /></ld>
      <sfc><scaling x="1" y="1" /></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="program0" pouType="program">
        <interface>
          <inputVars>
            <variable name="TLB2">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="START">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="STOP">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="VALUE">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="CYCLE_ON">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="start_cycle0">
              <type>
                <derived name="start_cycle"/>
              </type>
            </variable>
            <variable name="valves_handler0">
              <type>
                <derived name="valves_handler"/>
              </type>
            </variable>
            <variable name="stop_cycle0">
              <type>
                <derived name="stop_cycle"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="1" height="300" width="10">
              <position x="30" y="30"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="150"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="280"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="240" width="10">
              <position x="720" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="6">
                  <position x="720" y="60"/>
                  <position x="605" y="60"/>
                  <position x="605" y="50"/>
                  <position x="491" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="120"/>
                <connection refLocalId="27" formalParameter="ENO">
                  <position x="720" y="160"/>
                  <position x="605" y="160"/>
                  <position x="605" y="130"/>
                  <position x="490" y="130"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="220"/>
                <connection refLocalId="29" formalParameter="ENO">
                  <position x="720" y="260"/>
                  <position x="547" y="260"/>
                  <position x="547" y="310"/>
                  <position x="470" y="310"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="3" height="20" width="21" negated="false">
              <position x="140" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="50"/>
                  <position x="40" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="280" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="3">
                  <position x="280" y="50"/>
                  <position x="161" y="50"/>
                </connection>
                <connection refLocalId="21">
                  <position x="280" y="50"/>
                  <position x="221" y="50"/>
                  <position x="221" y="80"/>
                  <position x="161" y="80"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <coil localId="6" height="20" width="21" negated="false">
              <position x="470" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="4">
                  <position x="470" y="50"/>
                  <position x="301" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </coil>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="210" y="190"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="540" y="140"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="27" formalParameter="OUT_MV1">
                  <position x="540" y="160"/>
                  <position x="510" y="160"/>
                  <position x="510" y="150"/>
                  <position x="490" y="150"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="560" y="210"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="27" formalParameter="OUT_MV2">
                  <position x="560" y="220"/>
                  <position x="520" y="220"/>
                  <position x="520" y="170"/>
                  <position x="490" y="170"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="140" y="70"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="80"/>
                  <position x="90" y="80"/>
                  <position x="90" y="50"/>
                  <position x="40" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="210" y="230"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="210" y="270"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <inVariable localId="25" height="30" width="80" negated="false">
              <position x="70" y="220"/>
              <connectionPointOut>
                <relPosition x="80" y="20"/>
              </connectionPointOut>
              <expression>CYCLE_ON</expression>
            </inVariable>
            <block localId="26" typeName="start_cycle" instanceName="start_cycle0" height="60" width="130">
              <position x="100" y="110"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="1">
                      <position x="100" y="140"/>
                      <position x="60" y="140"/>
                      <position x="60" y="180"/>
                      <position x="40" y="180"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="25">
                      <position x="100" y="160"/>
                      <position x="70" y="160"/>
                      <position x="70" y="185"/>
                      <position x="160" y="185"/>
                      <position x="160" y="240"/>
                      <position x="150" y="240"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="130" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="130" y="50"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="27" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="360" y="100"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="26" formalParameter="OUT">
                      <position x="360" y="130"/>
                      <position x="260" y="130"/>
                      <position x="260" y="160"/>
                      <position x="230" y="160"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="360" y="150"/>
                      <position x="270" y="150"/>
                      <position x="270" y="200"/>
                      <position x="260" y="200"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="360" y="170"/>
                      <position x="290" y="170"/>
                      <position x="290" y="250"/>
                      <position x="260" y="250"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="360" y="190"/>
                      <position x="310" y="190"/>
                      <position x="310" y="290"/>
                      <position x="260" y="290"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="130" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="130" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="130" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <contact localId="28" height="20" width="21" negated="true">
              <position x="90" y="310"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="90" y="320"/>
                  <position x="70" y="320"/>
                  <position x="70" y="310"/>
                  <position x="40" y="310"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <block localId="29" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="380" y="280"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="28">
                      <position x="380" y="310"/>
                      <position x="245" y="310"/>
                      <position x="245" y="320"/>
                      <position x="110" y="320"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="90" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="90" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="90" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="30" height="30" width="40" negated="false">
              <position x="570" y="300"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29" formalParameter="OUT_MV1">
                  <position x="570" y="320"/>
                  <position x="520" y="320"/>
                  <position x="520" y="330"/>
                  <position x="470" y="330"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="31" height="30" width="40" negated="false">
              <position x="570" y="350"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29" formalParameter="OUT_MV2">
                  <position x="570" y="370"/>
                  <position x="520" y="370"/>
                  <position x="520" y="350"/>
                  <position x="470" y="350"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
          </LD>
        </body>
      </pou>
             <pou name="stop_cycle" pouType="functionBlock">
        <interface>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[OUT_MV1 := FALSE;
OUT_MV2 := FALSE;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
      <pou name="valves_handler" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB2">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="real_value">
              <type>
                <INT/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[
real_value :=  IN1 - 5;

if real_value <= IN_TLB2 then
  OUT_MV2 := FALSE;
  OUT_MV1 := TRUE;
end_if;

if real_value >= IN_TLB1 THEN
  OUT_MV2 := TRUE;
  OUT_MV1 := FALSE;
end_if;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
      <pou name="start_cycle" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <BOOL/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[OUT := IN1;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="task0" priority="0" interval="T#20ms">
            <pouInstance name="instance0" typeName="program0"/>
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_stop_eq

- Language: LD-graphical
- File: lstop_eq.xml
- Properties:
- P1 (invariant): !(STOP && CYCLE_ON)

```xml
<?xml version='1.0' encoding='utf-8'?>
<!-- fileHeader and contentHeader synthesised 2026-09-01. The program arrived
     from the PLC-LD-dataset with neither, and without the PLCopen
     namespace, so no conforming importer would recognise it as PLCopen XML.
     Only these headers and the namespace were added; the POUs, the ladder
     bodies and the configuration are untouched. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="PLC-LD-dataset" productVersion="1.0" creationDateTime="2024-01-01T00:00:00" />
  <contentHeader name="lstop_eq">
    <coordinateInfo>
      <fbd><scaling x="1" y="1" /></fbd>
      <ld><scaling x="1" y="1" /></ld>
      <sfc><scaling x="1" y="1" /></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="program0" pouType="program">
        <interface>
          <inputVars>
            <variable name="TLB2">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="STOP">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="START">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="VALUE">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="CYCLE_ON">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="valves_handler0">
              <type>
                <derived name="valves_handler"/>
              </type>
            </variable>
            <variable name="stop_cycle0">
              <type>
                <derived name="stop_cycle"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="1" height="330" width="10">
              <position x="70" y="70"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="160"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="310"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="290" width="10">
              <position x="780" y="90"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29">
                  <position x="780" y="110"/>
                  <position x="621" y="110"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="150"/>
                <connection refLocalId="35" formalParameter="ENO">
                  <position x="780" y="240"/>
                  <position x="680" y="240"/>
                  <position x="680" y="200"/>
                  <position x="480" y="200"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="270"/>
                <connection refLocalId="37" formalParameter="ENO">
                  <position x="780" y="360"/>
                  <position x="640" y="360"/>
                  <position x="640" y="350"/>
                  <position x="520" y="350"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="510" y="100"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="21">
                  <position x="510" y="110"/>
                  <position x="430" y="110"/>
                  <position x="430" y="150"/>
                  <position x="181" y="150"/>
                </connection>
                <connection refLocalId="34" formalParameter="OUT">
                  <position x="510" y="110"/>
                  <position x="480" y="110"/>
                  <position x="480" y="80"/>
                  <position x="400" y="80"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="170" y="230"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="600" y="220"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="35" formalParameter="OUT_MV1">
                  <position x="600" y="230"/>
                  <position x="560" y="230"/>
                  <position x="560" y="220"/>
                  <position x="480" y="220"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="570" y="260"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="35" formalParameter="OUT_MV2">
                  <position x="570" y="280"/>
                  <position x="545" y="280"/>
                  <position x="545" y="240"/>
                  <position x="480" y="240"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="160" y="140"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="150"/>
                  <position x="120" y="150"/>
                  <position x="120" y="90"/>
                  <position x="80" y="90"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="160" y="190"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="200"/>
                  <position x="120" y="200"/>
                  <position x="120" y="230"/>
                  <position x="80" y="230"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="210" y="280"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="240" y="320"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <contact localId="25" height="20" width="21" negated="false">
              <position x="160" y="80"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="90"/>
                  <position x="80" y="90"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <coil localId="29" height="20" width="21" negated="false">
              <position x="600" y="100"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="4">
                  <position x="600" y="110"/>
                  <position x="531" y="110"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </coil>
            <inVariable localId="31" height="30" width="40" negated="false">
              <position x="260" y="70"/>
              <connectionPointOut>
                <relPosition x="40" y="10"/>
              </connectionPointOut>
              <expression>IN1</expression>
            </inVariable>
            <inVariable localId="32" height="30" width="30" negated="false">
              <position x="270" y="110"/>
              <connectionPointOut>
                <relPosition x="30" y="10"/>
              </connectionPointOut>
              <expression>1</expression>
            </inVariable>
            <block localId="34" typeName="EQ" height="80" width="70">
              <position x="330" y="30"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="25">
                      <position x="330" y="60"/>
                      <position x="255" y="60"/>
                      <position x="255" y="90"/>
                      <position x="181" y="90"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="31">
                      <position x="330" y="80"/>
                      <position x="300" y="80"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="32">
                      <position x="330" y="100"/>
                      <position x="315" y="100"/>
                      <position x="315" y="120"/>
                      <position x="300" y="120"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="70" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="70" y="50"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="35" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="350" y="170"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="350" y="200"/>
                      <position x="181" y="200"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="350" y="220"/>
                      <position x="285" y="220"/>
                      <position x="285" y="240"/>
                      <position x="220" y="240"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="350" y="240"/>
                      <position x="305" y="240"/>
                      <position x="305" y="300"/>
                      <position x="260" y="300"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="350" y="260"/>
                      <position x="320" y="260"/>
                      <position x="320" y="340"/>
                      <position x="290" y="340"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="130" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="130" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="130" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <contact localId="36" height="20" width="21" negated="true">
              <position x="140" y="370"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="380"/>
                  <position x="80" y="380"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <block localId="37" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="430" y="320"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="36">
                      <position x="430" y="350"/>
                      <position x="335" y="350"/>
                      <position x="335" y="380"/>
                      <position x="160" y="380"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="90" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="90" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="90" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="38" height="30" width="40" negated="false">
              <position x="590" y="360"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="37" formalParameter="OUT_MV1">
                  <position x="590" y="370"/>
                  <position x="520" y="370"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="39" height="30" width="40" negated="false">
              <position x="590" y="400"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="37" formalParameter="OUT_MV2">
                  <position x="590" y="410"/>
                  <position x="550" y="410"/>
                  <position x="550" y="390"/>
                  <position x="520" y="390"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
          </LD>
        </body>
      </pou>
      <pou name="stop_cycle" pouType="functionBlock">
        <interface>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[OUT_MV1 := FALSE;
OUT_MV2 := FALSE;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
      <pou name="valves_handler" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB2">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="real_value">
              <type>
                <INT/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[
real_value :=  IN1 - 5;

if real_value <= IN_TLB2 then
  OUT_MV2 := FALSE;
  OUT_MV1 := TRUE;
end_if;

if real_value >= IN_TLB1 THEN
  OUT_MV2 := TRUE;
  OUT_MV1 := FALSE;
end_if;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="task0" priority="0" interval="T#20ms">
            <pouInstance name="instance0" typeName="program0"/>
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_substation_breaker

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(breaker_closed && fault)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_substation_breaker_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_substation_breaker_clean" pouType="program">
      <interface><inputVars><variable name="close_cmd"><type><BOOL /></type></variable><variable name="fault"><type><BOOL /></type></variable><variable name="lockout"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="breaker_closed"><type><BOOL /></type></variable><variable name="alarm"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>fault</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>close_cmd</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>lockout</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>breaker_closed</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>fault</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>alarm</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_substation_breaker_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_tank_assignment

- Language: LD-graphical
- File: legitimate_lassignment.xml
- Properties:
- P1 (termination): None

```xml
<?xml version='1.0' encoding='utf-8'?>
<!-- fileHeader and contentHeader synthesised 2026-08-27. The program arrived
     from the PLC_Defuser dataset with neither, and without the PLCopen
     namespace, so no conforming importer would recognise it as PLCopen XML.
     Only these headers and the namespace were added; the POUs, the ladder
     bodies and the configuration are untouched. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="PLC_Defuser dataset" productVersion="1.0" creationDateTime="2019-01-01T00:00:00" />
  <contentHeader name="legitimate_lassignment">
    <coordinateInfo>
      <fbd><scaling x="1" y="1" /></fbd>
      <ld><scaling x="1" y="1" /></ld>
      <sfc><scaling x="1" y="1" /></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="program0" pouType="program">
        <interface>
          <inputVars>
            <variable name="TLB2">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="START">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="STOP">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="VALUE">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="CYCLE_ON">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="valves_handler0">
              <type>
                <derived name="valves_handler"/>
              </type>
            </variable>
            <variable name="stop_cycle0">
              <type>
                <derived name="stop_cycle"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="1" height="330" width="10">
              <position x="60" y="30"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="170"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="310"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="220" width="10">
              <position x="660" y="30"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="6">
                  <position x="660" y="50"/>
                  <position x="491" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="110"/>
                <connection refLocalId="25" formalParameter="ENO">
                  <position x="660" y="140"/>
                  <position x="390" y="140"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="200"/>
                <connection refLocalId="27" formalParameter="ENO">
                  <position x="660" y="230"/>
                  <position x="447" y="230"/>
                  <position x="447" y="310"/>
                  <position x="370" y="310"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="3" height="20" width="21" negated="false">
              <position x="140" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="50"/>
                  <position x="70" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="280" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="3">
                  <position x="280" y="50"/>
                  <position x="161" y="50"/>
                </connection>
                <connection refLocalId="21">
                  <position x="280" y="50"/>
                  <position x="221" y="50"/>
                  <position x="221" y="90"/>
                  <position x="161" y="90"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <coil localId="6" height="20" width="21" negated="false">
              <position x="470" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="4">
                  <position x="470" y="50"/>
                  <position x="301" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </coil>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="120" y="150"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="570" y="150"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="25" formalParameter="OUT_MV1">
                  <position x="570" y="160"/>
                  <position x="390" y="160"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="490" y="180"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="25" formalParameter="OUT_MV2">
                  <position x="490" y="200"/>
                  <position x="445" y="200"/>
                  <position x="445" y="180"/>
                  <position x="390" y="180"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="140" y="80"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="90"/>
                  <position x="105" y="90"/>
                  <position x="105" y="50"/>
                  <position x="70" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="150" y="120"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="150" y="130"/>
                  <position x="110" y="130"/>
                  <position x="110" y="190"/>
                  <position x="70" y="190"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="130" y="190"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="150" y="240"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <block localId="25" typeName="valves_handler" instanceName="valves_handler0" height="120" width="130">
              <position x="260" y="110"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="260" y="140"/>
                      <position x="215" y="140"/>
                      <position x="215" y="130"/>
                      <position x="171" y="130"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="60"/>
                    <connection refLocalId="18">
                      <position x="260" y="170"/>
                      <position x="220" y="170"/>
                      <position x="220" y="160"/>
                      <position x="170" y="160"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="80"/>
                    <connection refLocalId="23">
                      <position x="260" y="190"/>
                      <position x="225" y="190"/>
                      <position x="225" y="200"/>
                      <position x="180" y="200"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="110"/>
                    <connection refLocalId="24">
                      <position x="260" y="220"/>
                      <position x="230" y="220"/>
                      <position x="230" y="260"/>
                      <position x="200" y="260"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="130" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="130" y="60"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="130" y="80"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <contact localId="5" height="20" width="21" negated="true" executionOrderId="0">
              <position x="280" y="140"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <contact localId="26" height="20" width="21" negated="true">
              <position x="130" y="330"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="130" y="340"/>
                  <position x="70" y="340"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <block localId="27" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="280" y="280"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="26">
                      <position x="280" y="310"/>
                      <position x="190" y="310"/>
                      <position x="190" y="340"/>
                      <position x="151" y="340"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="90" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="90" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="90" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="28" height="30" width="40" negated="false">
              <position x="470" y="310"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="27" formalParameter="OUT_MV1">
                  <position x="470" y="320"/>
                  <position x="380" y="320"/>
                  <position x="380" y="330"/>
                  <position x="370" y="330"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="29" height="30" width="40" negated="false">
              <position x="440" y="340"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="27" formalParameter="OUT_MV2">
                  <position x="440" y="350"/>
                  <position x="370" y="350"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
          </LD>
        </body>
      </pou>
      <pou name="valves_handler" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB2">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="i">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="real_value">
              <type>
                <INT/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[
real_value :=  IN1 - 5;


if real_value <= IN_TLB2 then
  OUT_MV2 := FALSE;
  OUT_MV1 := TRUE;
end_if;

if real_value >= IN_TLB1 THEN
  OUT_MV2 := TRUE;
  OUT_MV1 := FALSE;
end_if;

]]></xhtml:p>
          </ST>
        </body>
      </pou>
      <pou name="stop_cycle" pouType="functionBlock">
        <interface>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[OUT_MV1 := FALSE;
OUT_MV2 := FALSE;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="task0" priority="0" interval="T#20ms">
            <pouInstance name="instance0" typeName="program0"/>
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_tank_start_eq

- Language: LD-graphical
- File: legitimate_lstart_eq.xml
- Properties:
- P1 (termination): None

```xml
<?xml version='1.0' encoding='utf-8'?>
<!-- fileHeader and contentHeader synthesised 2026-08-27. The program arrived
     from the PLC_Defuser dataset with neither, and without the PLCopen
     namespace, so no conforming importer would recognise it as PLCopen XML.
     Only these headers and the namespace were added; the POUs, the ladder
     bodies and the configuration are untouched. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Unknown" productName="PLC_Defuser dataset" productVersion="1.0" creationDateTime="2019-01-01T00:00:00" />
  <contentHeader name="legitimate_lstart_eq">
    <coordinateInfo>
      <fbd><scaling x="1" y="1" /></fbd>
      <ld><scaling x="1" y="1" /></ld>
      <sfc><scaling x="1" y="1" /></sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="program0" pouType="program">
        <interface>
          <inputVars>
            <variable name="TLB2">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="STOP">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="START">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="VALUE">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="CYCLE_ON">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="valves_handler0">
              <type>
                <derived name="valves_handler"/>
              </type>
            </variable>
            <variable name="stop_cycle0">
              <type>
                <derived name="stop_cycle"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="1" height="350" width="10">
              <position x="70" y="40"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="180"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="330"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="250" width="10">
              <position x="780" y="90"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29">
                  <position x="780" y="110"/>
                  <position x="621" y="110"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="130"/>
                <connection refLocalId="35" formalParameter="ENO">
                  <position x="780" y="220"/>
                  <position x="640" y="220"/>
                  <position x="640" y="200"/>
                  <position x="500" y="200"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="230"/>
                <connection refLocalId="36" formalParameter="ENO">
                  <position x="780" y="320"/>
                  <position x="560" y="320"/>
                  <position x="560" y="340"/>
                  <position x="480" y="340"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="510" y="100"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="21">
                  <position x="510" y="110"/>
                  <position x="470" y="110"/>
                  <position x="470" y="140"/>
                  <position x="401" y="140"/>
                </connection>
                <connection refLocalId="25">
                  <position x="510" y="110"/>
                  <position x="470" y="110"/>
                  <position x="470" y="80"/>
                  <position x="401" y="80"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="200" y="200"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="670" y="230"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="35" formalParameter="OUT_MV1">
                  <position x="670" y="240"/>
                  <position x="590" y="240"/>
                  <position x="590" y="220"/>
                  <position x="500" y="220"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="600" y="250"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="35" formalParameter="OUT_MV2">
                  <position x="600" y="270"/>
                  <position x="555" y="270"/>
                  <position x="555" y="240"/>
                  <position x="500" y="240"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="380" y="130"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="380" y="140"/>
                  <position x="130" y="140"/>
                  <position x="130" y="60"/>
                  <position x="80" y="60"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="160" y="190"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="200"/>
                  <position x="80" y="200"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="180" y="240"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="160" y="270"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <contact localId="25" height="20" width="21" negated="false">
              <position x="380" y="70"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="34" formalParameter="OUT">
                  <position x="380" y="80"/>
                  <position x="320" y="80"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <coil localId="29" height="20" width="21" negated="false">
              <position x="600" y="100"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="4">
                  <position x="600" y="110"/>
                  <position x="531" y="110"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </coil>
            <inVariable localId="31" height="30" width="40" negated="false">
              <position x="170" y="70"/>
              <connectionPointOut>
                <relPosition x="40" y="10"/>
              </connectionPointOut>
              <expression>IN1</expression>
            </inVariable>
            <inVariable localId="32" height="30" width="30" negated="false">
              <position x="190" y="100"/>
              <connectionPointOut>
                <relPosition x="30" y="10"/>
              </connectionPointOut>
              <expression>5</expression>
            </inVariable>
            <block localId="34" typeName="EQ" height="80" width="70">
              <position x="250" y="30"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="1">
                      <position x="250" y="60"/>
                      <position x="80" y="60"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="31">
                      <position x="250" y="80"/>
                      <position x="210" y="80"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="32">
                      <position x="250" y="100"/>
                      <position x="240" y="100"/>
                      <position x="240" y="120"/>
                      <position x="220" y="120"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="70" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="70" y="50"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="35" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="370" y="170"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="370" y="200"/>
                      <position x="181" y="200"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="370" y="220"/>
                      <position x="250" y="220"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="370" y="240"/>
                      <position x="320" y="240"/>
                      <position x="320" y="260"/>
                      <position x="230" y="260"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="370" y="260"/>
                      <position x="350" y="260"/>
                      <position x="350" y="280"/>
                      <position x="210" y="280"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="130" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="130" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="130" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="36" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="390" y="310"/>
             <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="40">
                      <position x="390" y="340"/>
                      <position x="300" y="340"/>
                      <position x="300" y="370"/>
                      <position x="210" y="370"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="90" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV1">
                  <connectionPointOut>
                    <relPosition x="90" y="50"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT_MV2">
                  <connectionPointOut>
                    <relPosition x="90" y="70"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="37" height="30" width="40" negated="false">
              <position x="580" y="340"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="36" formalParameter="OUT_MV1">
                  <position x="580" y="360"/>
                  <position x="480" y="360"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="38" height="30" width="40" negated="false">
              <position x="580" y="380"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="36" formalParameter="OUT_MV2">
                  <position x="580" y="400"/>
                  <position x="530" y="400"/>
                  <position x="530" y="380"/>
                  <position x="480" y="380"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
          </LD>
        </body>
      </pou>
           <pou name="stop_cycle" pouType="functionBlock">
        <interface>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[OUT_MV1 := FALSE;
OUT_MV2 := FALSE;
]]></xhtml:p>
          </ST>
        </body>
      </pou>
      <pou name="valves_handler" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB1">
              <type>
                <INT/>
              </type>
            </variable>
            <variable name="IN_TLB2">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT_MV1">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="OUT_MV2">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="real_value">
              <type>
                <INT/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[
real_value :=  IN1 - 5;

if real_value <= IN_TLB2 then
  OUT_MV2 := FALSE;
  OUT_MV1 := TRUE;
end_if;

if real_value >= IN_TLB1 THEN
  OUT_MV2 := TRUE;
  OUT_MV1 := FALSE;
end_if;


]]></xhtml:p>
          </ST>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="task0" priority="0" interval="T#20ms">
            <pouInstance name="instance0" typeName="program0"/>
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```
