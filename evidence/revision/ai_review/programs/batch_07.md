# Batch 7: benchmarks g_tank_start_le, g_tank_stop_ge, g_tank_sub_function, g_tank_substitution_coil, g_tank_value_filtering, g_tank_valves, g_timer_latch_mix, g_tof_hold

## g_tank_start_le

- Language: LD-graphical
- File: legitimate_lstart_le.xml
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
  <contentHeader name="legitimate_lstart_le">
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
            <variable name="stop_cycle0">
              <type>
                <derived name="stop_cycle"/>
              </type>
            </variable>
            <variable name="valves_handler0">
              <type>
                <derived name="valves_handler"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="1" height="310" width="10">
              <position x="70" y="40"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="160"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="290"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="260" width="10">
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
                <connection refLocalId="37" formalParameter="ENO">
                  <position x="780" y="220"/>
                  <position x="625" y="220"/>
                  <position x="625" y="200"/>
                  <position x="470" y="200"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="240"/>
                <connection refLocalId="34" formalParameter="ENO">
                  <position x="780" y="330"/>
                  <position x="630" y="330"/>
                  <position x="630" y="340"/>
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
              <position x="200" y="210"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="640" y="240"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="37" formalParameter="OUT_MV1">
                  <position x="640" y="250"/>
                  <position x="535" y="250"/>
                  <position x="535" y="220"/>
                  <position x="470" y="220"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="570" y="260"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="37" formalParameter="OUT_MV2">
                  <position x="570" y="280"/>
                  <position x="520" y="280"/>
                  <position x="520" y="240"/>
                  <position x="470" y="240"/>
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
                  <position x="146" y="140"/>
                  <position x="146" y="60"/>
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
              <position x="200" y="250"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="200" y="290"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <contact localId="25" height="20" width="21" negated="false">
              <position x="380" y="70"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="33" formalParameter="OUT">
                  <position x="380" y="80"/>
                  <position x="330" y="80"/>
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
              <position x="160" y="70"/>
              <connectionPointOut>
                <relPosition x="40" y="20"/>
              </connectionPointOut>
              <expression>IN1</expression>
            </inVariable>
            <inVariable localId="32" height="30" width="30" negated="false">
              <position x="210" y="100"/>
              <connectionPointOut>
                <relPosition x="30" y="20"/>
              </connectionPointOut>
              <expression>5</expression>
            </inVariable>
            <block localId="33" typeName="LE" height="80" width="70">
              <position x="260" y="30"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="1">
                      <position x="260" y="60"/>
                      <position x="80" y="60"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="31">
                      <position x="260" y="80"/>
                      <position x="235" y="80"/>
                      <position x="235" y="90"/>
                      <position x="200" y="90"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="32">
                      <position x="260" y="100"/>
                      <position x="250" y="100"/>
                      <position x="250" y="120"/>
                      <position x="240" y="120"/>
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
            <block localId="34" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="390" y="310"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="38">
                      <position x="390" y="340"/>
                      <position x="315" y="340"/>
                      <position x="315" y="360"/>
                      <position x="240" y="360"/>
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
            <outVariable localId="35" height="30" width="40" negated="false">
              <position x="560" y="360"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="34" formalParameter="OUT_MV1">
                  <position x="560" y="370"/>
                  <position x="535" y="370"/>
                  <position x="535" y="360"/>
                  <position x="480" y="360"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="36" height="30" width="40" negated="false">
              <position x="540" y="400"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="34" formalParameter="OUT_MV2">
                  <position x="540" y="410"/>
                  <position x="530" y="410"/>
                  <position x="530" y="380"/>
                  <position x="480" y="380"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <block localId="37" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="340" y="170"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="340" y="200"/>
                      <position x="181" y="200"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="340" y="220"/>
                      <position x="250" y="220"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="340" y="240"/>
                      <position x="280" y="240"/>
                      <position x="280" y="260"/>
                      <position x="250" y="260"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="340" y="260"/>
                      <position x="295" y="260"/>
                      <position x="295" y="300"/>
                      <position x="250" y="300"/>
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
            <contact localId="38" height="20" width="20" negated="true">
              <position x="220" y="350"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="220" y="360"/>
                  <position x="125" y="360"/>
                  <position x="125" y="330"/>
                  <position x="80" y="330"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="20" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
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

## g_tank_stop_ge

- Language: LD-graphical
- File: legitimate_lstop_ge.xml
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
  <contentHeader name="legitimate_lstop_ge">
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
            <leftPowerRail localId="1" height="300" width="10">
              <position x="60" y="60"/>
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
            <rightPowerRail localId="2" height="300" width="10">
              <position x="770" y="70"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29">
                  <position x="770" y="90"/>
                  <position x="700" y="90"/>
                  <position x="700" y="110"/>
                  <position x="621" y="110"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="160"/>
                <connection refLocalId="34" formalParameter="ENO">
                  <position x="770" y="230"/>
                  <position x="625" y="230"/>
                  <position x="625" y="200"/>
                  <position x="470" y="200"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="280"/>
                <connection refLocalId="35" formalParameter="ENO">
                  <position x="770" y="350"/>
                  <position x="470" y="350"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="510" y="100"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="21">
                  <position x="510" y="110"/>
                  <position x="460" y="110"/>
                  <position x="460" y="140"/>
                  <position x="401" y="140"/>
                </connection>
                <connection refLocalId="33" formalParameter="OUT">
                  <position x="510" y="110"/>
                  <position x="460" y="110"/>
                  <position x="460" y="70"/>
                  <position x="390" y="70"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="170" y="200"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="560" y="210"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="34" formalParameter="OUT_MV1">
                  <position x="560" y="220"/>
                  <position x="470" y="220"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="610" y="240"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="34" formalParameter="OUT_MV2">
                  <position x="610" y="260"/>
                  <position x="540" y="260"/>
                  <position x="540" y="240"/>
                  <position x="470" y="240"/>
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
                  <position x="142" y="140"/>
                  <position x="142" y="80"/>
                  <position x="70" y="80"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="160" y="160"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="170"/>
                  <position x="115" y="170"/>
                  <position x="115" y="230"/>
                  <position x="70" y="230"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="170" y="240"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="220" y="280"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <contact localId="25" height="20" width="21" negated="false">
              <position x="160" y="70"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="80"/>
                  <position x="70" y="80"/>
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
              <position x="200" y="90"/>
              <connectionPointOut>
                <relPosition x="40" y="10"/>
              </connectionPointOut>
              <expression>IN1</expression>
            </inVariable>
            <inVariable localId="32" height="30" width="30" negated="false">
              <position x="260" y="110"/>
              <connectionPointOut>
                <relPosition x="30" y="10"/>
              </connectionPointOut>
              <expression>5</expression>
            </inVariable>
            <block localId="33" typeName="GE" height="80" width="70">
              <position x="320" y="20"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="25">
                      <position x="320" y="50"/>
                      <position x="250" y="50"/>
                      <position x="250" y="80"/>
                      <position x="181" y="80"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="31">
                      <position x="320" y="70"/>
                      <position x="280" y="70"/>
                      <position x="280" y="100"/>
                      <position x="240" y="100"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="32">
                      <position x="320" y="90"/>
                      <position x="305" y="90"/>
                      <position x="305" y="105"/>
                      <position x="330" y="105"/>
                      <position x="330" y="120"/>
                      <position x="290" y="120"/>
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
            <block localId="34" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="340" y="170"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="340" y="200"/>
                      <position x="240" y="200"/>
                      <position x="240" y="170"/>
                      <position x="181" y="170"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="340" y="220"/>
                      <position x="220" y="220"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="340" y="240"/>
                      <position x="300" y="240"/>
                      <position x="300" y="260"/>
                      <position x="220" y="260"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="340" y="260"/>
                      <position x="315" y="260"/>
                      <position x="315" y="300"/>
                      <position x="270" y="300"/>
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
            <block localId="35" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="380" y="320"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="36">
                      <position x="380" y="350"/>
                      <position x="295" y="350"/>
                      <position x="295" y="370"/>
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
            <contact localId="36" height="20" width="21" negated="true">
              <position x="190" y="360"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="190" y="370"/>
                  <position x="130" y="370"/>
                  <position x="130" y="340"/>
                  <position x="70" y="340"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <outVariable localId="37" height="30" width="40" negated="false">
              <position x="560" y="360"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="35" formalParameter="OUT_MV1">
                  <position x="560" y="380"/>
                  <position x="515" y="380"/>
                  <position x="515" y="370"/>
                  <position x="470" y="370"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="38" height="30" width="40" negated="false">
              <position x="550" y="400"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="35" formalParameter="OUT_MV2">
                  <position x="550" y="420"/>
                  <position x="510" y="420"/>
                  <position x="510" y="390"/>
                  <position x="470" y="390"/>
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

## g_tank_sub_function

- Language: LD-graphical
- File: legitimate_lsub_function.xml
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
  <contentHeader name="legitimate_lsub_function">
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
            <variable name="FILTERED_VALUE">
              <type>
                <INT/>
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
            <leftPowerRail localId="1" height="480" width="10">
              <position x="20" y="10"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="170"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="310"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="460"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="460" width="10">
              <position x="730" y="10"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="6">
                  <position x="730" y="30"/>
                  <position x="491" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="170"/>
                <connection refLocalId="25" formalParameter="ENO">
                  <position x="730" y="180"/>
                  <position x="550" y="180"/>
                  <position x="550" y="140"/>
                  <position x="370" y="140"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="290"/>
                <connection refLocalId="30" formalParameter="ENO">
                  <position x="730" y="300"/>
                  <position x="590" y="300"/>
                  <position x="590" y="290"/>
                  <position x="450" y="290"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="440"/>
                <connection refLocalId="32" formalParameter="ENO">
                  <position x="730" y="450"/>
                  <position x="575" y="450"/>
                  <position x="575" y="460"/>
                  <position x="420" y="460"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="3" height="20" width="21" negated="false">
              <position x="140" y="20"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="30"/>
                  <position x="30" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="280" y="18"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="3">
                  <position x="280" y="30"/>
                  <position x="220" y="30"/>
                  <position x="220" y="32"/>
                  <position x="161" y="32"/>
                </connection>
                <connection refLocalId="21">
                  <position x="280" y="30"/>
                  <position x="221" y="30"/>
                  <position x="221" y="102"/>
                  <position x="171" y="102"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="12"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <coil localId="6" height="20" width="21" negated="false">
              <position x="470" y="18"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="4">
                  <position x="470" y="30"/>
                  <position x="301" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="12"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </coil>
            <inVariable localId="18" height="30" width="130" negated="false">
              <position x="90" y="320"/>
              <connectionPointOut>
                <relPosition x="130" y="10"/>
              </connectionPointOut>
              <expression>FILTERED_VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="570" y="330"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="30" formalParameter="OUT_MV1">
                  <position x="570" y="340"/>
                  <position x="510" y="340"/>
                  <position x="510" y="310"/>
                  <position x="450" y="310"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="490" y="360"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="30" formalParameter="OUT_MV2">
                  <position x="490" y="380"/>
                  <position x="470" y="380"/>
                  <position x="470" y="330"/>
                  <position x="450" y="330"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="150" y="90"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="150" y="100"/>
                  <position x="90" y="100"/>
                  <position x="90" y="30"/>
                  <position x="30" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="140" y="280"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="290"/>
                  <position x="85" y="290"/>
                  <position x="85" y="320"/>
                  <position x="30" y="320"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="170" y="360"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="200" y="400"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <block localId="25" typeName="SUB" height="80" width="70">
              <position x="300" y="110"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="1">
                      <position x="300" y="140"/>
                      <position x="165" y="140"/>
                      <position x="165" y="180"/>
                      <position x="30" y="180"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="28">
                      <position x="300" y="160"/>
                      <position x="196" y="160"/>
                      <position x="196" y="180"/>
                      <position x="170" y="180"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="26">
                      <position x="300" y="180"/>
                      <position x="220" y="180"/>
                      <position x="220" y="240"/>
                      <position x="190" y="240"/>
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
            <inVariable localId="26" height="30" width="30" negated="false">
              <position x="160" y="220"/>
              <connectionPointOut>
                <relPosition x="30" y="20"/>
              </connectionPointOut>
              <expression>10</expression>
            </inVariable>
            <inVariable localId="28" height="30" width="50" negated="false">
              <position x="120" y="170"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="29" height="30" width="130" negated="false">
              <position x="390" y="190"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="25" formalParameter="OUT">
                  <position x="390" y="200"/>
                  <position x="380" y="200"/>
                  <position x="380" y="160"/>
                  <position x="370" y="160"/>
                </connection>
              </connectionPointIn>
              <expression>FILTERED_VALUE</expression>
            </outVariable>
            <block localId="30" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="320" y="260"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="320" y="290"/>
                      <position x="161" y="290"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="320" y="310"/>
                      <position x="240" y="310"/>
                      <position x="240" y="340"/>
                      <position x="220" y="340"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="320" y="330"/>
                      <position x="275" y="330"/>
                      <position x="275" y="380"/>
                      <position x="220" y="380"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="320" y="350"/>
                      <position x="285" y="350"/>
                      <position x="285" y="420"/>
                      <position x="250" y="420"/>
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
            <contact localId="31" height="20" width="21" negated="true">
              <position x="140" y="470"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="480"/>
                  <position x="85" y="480"/>
                  <position x="85" y="470"/>
                  <position x="30" y="470"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <block localId="32" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="330" y="430"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="31">
                      <position x="330" y="460"/>
                      <position x="245" y="460"/>
                      <position x="245" y="480"/>
                      <position x="160" y="480"/>
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
            <outVariable localId="33" height="30" width="40" negated="false">
              <position x="530" y="470"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="32" formalParameter="OUT_MV1">
                  <position x="530" y="490"/>
                  <position x="475" y="490"/>
                  <position x="475" y="480"/>
                  <position x="420" y="480"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="34" height="30" width="40" negated="false">
              <position x="530" y="510"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="32" formalParameter="OUT_MV2">
                  <position x="530" y="530"/>
                  <position x="475" y="530"/>
                  <position x="475" y="500"/>
                  <position x="420" y="500"/>
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

## g_tank_substitution_coil

- Language: LD-graphical
- File: legitimate_lsubstitution_coil.xml
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
  <contentHeader name="legitimate_lsubstitution_coil">
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
            <variable name="cycle0">
              <type>
                <derived name="ac_cycle"/>
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
            <leftPowerRail localId="1" height="330" width="10">
              <position x="70" y="10"/>
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
            <rightPowerRail localId="2" height="310" width="10">
              <position x="660" y="30"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="27" formalParameter="ENO">
                  <position x="660" y="50"/>
                  <position x="454" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="150"/>
                <connection refLocalId="29" formalParameter="ENO">
                  <position x="660" y="180"/>
                  <position x="545" y="180"/>
                  <position x="545" y="150"/>
                  <position x="430" y="150"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="290"/>
                <connection refLocalId="30" formalParameter="ENO">
                  <position x="660" y="320"/>
                  <position x="535" y="320"/>
                  <position x="535" y="280"/>
                  <position x="420" y="280"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="4" height="20" width="21" negated="true">
              <position x="280" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="21">
                  <position x="280" y="50"/>
                  <position x="230" y="50"/>
                  <position x="230" y="70"/>
                  <position x="181" y="70"/>
                </connection>
                <connection refLocalId="25">
                  <position x="280" y="50"/>
                  <position x="230" y="50"/>
                  <position x="230" y="30"/>
                  <position x="181" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>STOP</variable>
            </contact>
            <inVariable localId="18" height="30" width="50" negated="false">
              <position x="190" y="160"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="490" y="180"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29" formalParameter="OUT_MV1">
                  <position x="490" y="200"/>
                  <position x="480" y="200"/>
                  <position x="480" y="170"/>
                  <position x="430" y="170"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="470" y="230"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="29" formalParameter="OUT_MV2">
                  <position x="470" y="250"/>
                  <position x="460" y="250"/>
                  <position x="460" y="190"/>
                  <position x="430" y="190"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="160" y="60"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="70"/>
                  <position x="125" y="70"/>
                  <position x="125" y="30"/>
                  <position x="80" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="170" y="130"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="170" y="140"/>
                  <position x="125" y="140"/>
                  <position x="125" y="180"/>
                  <position x="80" y="180"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="190" y="210"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="190" y="250"/>
              <connectionPointOut>
                <relPosition x="50" y="20"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <contact localId="25" height="20" width="21" negated="false">
              <position x="160" y="20"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="30"/>
                  <position x="80" y="30"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>START</variable>
            </contact>
            <block localId="27" typeName="ac_cycle" instanceName="cycle0" height="60" width="74">
              <position x="380" y="20"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="4">
                      <position x="380" y="50"/>
                      <position x="301" y="50"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="4">
                      <position x="380" y="70"/>
                      <position x="340" y="70"/>
                      <position x="340" y="50"/>
                      <position x="301" y="50"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="ENO">
                  <connectionPointOut>
                    <relPosition x="74" y="30"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="74" y="50"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="28" height="30" width="80" negated="false">
              <position x="480" y="90"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="27" formalParameter="OUT">
                  <position x="480" y="110"/>
                  <position x="470" y="110"/>
                  <position x="470" y="80"/>
                  <position x="464" y="80"/>
                  <position x="464" y="70"/>
                  <position x="454" y="70"/>
                </connection>
              </connectionPointIn>
              <expression>CYCLE_ON</expression>
            </outVariable>
            <block localId="29" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="300" y="120"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="300" y="150"/>
                      <position x="240" y="150"/>
                      <position x="240" y="140"/>
                      <position x="191" y="140"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="18">
                      <position x="300" y="170"/>
                      <position x="270" y="170"/>
                      <position x="270" y="180"/>
                      <position x="240" y="180"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="300" y="190"/>
                      <position x="260" y="190"/>
                      <position x="260" y="220"/>
                      <position x="240" y="220"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="300" y="210"/>
                      <position x="275" y="210"/>
                      <position x="275" y="270"/>
                      <position x="240" y="270"/>
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
            <block localId="30" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="330" y="250"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="33">
                      <position x="330" y="280"/>
                      <position x="280" y="280"/>
                      <position x="280" y="330"/>
                      <position x="171" y="330"/>
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
            <outVariable localId="31" height="30" width="40" negated="false">
              <position x="480" y="290"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="30" formalParameter="OUT_MV1">
                  <position x="480" y="310"/>
                  <position x="450" y="310"/>
                  <position x="450" y="300"/>
                  <position x="420" y="300"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="32" height="30" width="40" negated="false">
              <position x="480" y="330"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="30" formalParameter="OUT_MV2">
                  <position x="480" y="350"/>
                  <position x="445" y="350"/>
                  <position x="445" y="320"/>
                  <position x="420" y="320"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="33" height="20" width="21" negated="true">
              <position x="150" y="320"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="150" y="330"/>
                  <position x="115" y="330"/>
                  <position x="115" y="320"/>
                  <position x="80" y="320"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
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
      <pou name="ac_cycle" pouType="functionBlock">
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
            <xhtml:p><![CDATA[
OUT:=IN1;

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

## g_tank_value_filtering

- Language: LD-graphical
- File: legitimate_lvalue_filtering.xml
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
  <contentHeader name="legitimate_lvalue_filtering">
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
            <variable name="value_filtering0">
              <type>
                <derived name="value_filtering"/>
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
            <leftPowerRail localId="1" height="310" width="10">
              <position x="70" y="30"/>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="20"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="150"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="10" y="290"/>
              </connectionPointOut>
            </leftPowerRail>
            <rightPowerRail localId="2" height="290" width="10">
              <position x="810" y="30"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="6">
                  <position x="810" y="50"/>
                  <position x="491" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="150"/>
                <connection refLocalId="27" formalParameter="ENO">
                  <position x="810" y="180"/>
                  <position x="732" y="180"/>
                  <position x="732" y="150"/>
                  <position x="550" y="150"/>
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="0" y="270"/>
                <connection refLocalId="28" formalParameter="ENO">
                  <position x="810" y="300"/>
                  <position x="655" y="300"/>
                  <position x="655" y="350"/>
                  <position x="500" y="350"/>
                </connection>
              </connectionPointIn>
            </rightPowerRail>
            <contact localId="3" height="20" width="21" negated="false">
              <position x="140" y="40"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="140" y="50"/>
                  <position x="80" y="50"/>
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
                  <position x="181" y="90"/>
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
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="650" y="160"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="27" formalParameter="OUT_MV1">
                  <position x="650" y="180"/>
                  <position x="600" y="180"/>
                  <position x="600" y="170"/>
                  <position x="550" y="170"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="650" y="210"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="27" formalParameter="OUT_MV2">
                  <position x="650" y="220"/>
                  <position x="575" y="220"/>
                  <position x="575" y="190"/>
                  <position x="550" y="190"/>
                </connection>
              </connectionPointIn>
              <expression>MV2</expression>
            </outVariable>
            <contact localId="21" height="20" width="21" negated="false">
              <position x="160" y="80"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="160" y="90"/>
                  <position x="120" y="90"/>
                  <position x="120" y="50"/>
                  <position x="80" y="50"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <contact localId="22" height="20" width="21" negated="false">
              <position x="260" y="130"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="260" y="140"/>
                  <position x="140" y="140"/>
                  <position x="140" y="180"/>
                  <position x="80" y="180"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <inVariable localId="23" height="30" width="50" negated="false">
              <position x="280" y="250"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="290" y="290"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB2</expression>
            </inVariable>
            <block localId="25" typeName="value_filtering" instanceName="value_filtering0" height="60" width="130">
              <position x="170" y="170"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="1">
                      <position x="170" y="200"/>
                      <position x="140" y="200"/>
                      <position x="140" y="180"/>
                      <position x="80" y="180"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="26">
                      <position x="170" y="220"/>
                      <position x="150" y="220"/>
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
            <inVariable localId="26" height="30" width="50" negated="false">
              <position x="100" y="210"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <block localId="27" typeName="valves_handler" instanceName="valves_handler0" height="100" width="130">
              <position x="420" y="120"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="22">
                      <position x="420" y="150"/>
                      <position x="345" y="150"/>
                      <position x="345" y="140"/>
                      <position x="281" y="140"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="25" formalParameter="OUT">
                      <position x="420" y="170"/>
                      <position x="340" y="170"/>
                      <position x="340" y="220"/>
                      <position x="300" y="220"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="70"/>
                    <connection refLocalId="23">
                      <position x="420" y="190"/>
                      <position x="355" y="190"/>
                      <position x="355" y="260"/>
                      <position x="330" y="260"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="90"/>
                    <connection refLocalId="24">
                      <position x="420" y="210"/>
                      <position x="370" y="210"/>
                      <position x="370" y="300"/>
                      <position x="340" y="300"/>
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
            <block localId="28" typeName="stop_cycle" instanceName="stop_cycle0" height="80" width="90">
              <position x="410" y="320"/>
              <inputVariables>
                <variable formalParameter="EN">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="29">
                      <position x="410" y="350"/>
                      <position x="300" y="350"/>
                      <position x="300" y="330"/>
                      <position x="191" y="330"/>
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
            <contact localId="29" height="20" width="21" negated="true">
              <position x="170" y="320"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="1">
                  <position x="170" y="330"/>
                  <position x="125" y="330"/>
                  <position x="125" y="320"/>
                  <position x="80" y="320"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="10"/>
              </connectionPointOut>
              <variable>CYCLE_ON</variable>
            </contact>
            <outVariable localId="5" height="30" width="50" negated="false" executionOrderId="0">
              <position x="650" y="370"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="28" formalParameter="OUT_MV1">
                  <position x="650" y="380"/>
                  <position x="570" y="380"/>
                  <position x="570" y="370"/>
                  <position x="500" y="370"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="7" height="30" width="50" negated="false" executionOrderId="0">
              <position x="650" y="410"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="28" formalParameter="OUT_MV2">
                  <position x="650" y="430"/>
                  <position x="570" y="430"/>
                  <position x="570" y="390"/>
                  <position x="500" y="390"/>
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
      <pou name="value_filtering" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="IN1">
              <type>
                <INT/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="OUT">
              <type>
                <INT/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="value_real">
              <type>
                <INT/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <ST>
            <xhtml:p><![CDATA[
value_real := IN1 - 5;
OUT := value_real;
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

## g_tank_valves

- Language: LD-graphical
- File: legitimate_lvalves_handler.xml
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
  <contentHeader name="legitimate_lvalves_handler">
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
                  <position x="590" y="230"/>
                  <position x="590" y="310"/>
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
              <position x="150" y="160"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>VALUE</expression>
            </inVariable>
            <outVariable localId="19" height="30" width="50" negated="false">
              <position x="470" y="180"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="25" formalParameter="OUT_MV1">
                  <position x="470" y="190"/>
                  <position x="460" y="190"/>
                  <position x="460" y="170"/>
                  <position x="390" y="170"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="20" height="30" width="50" negated="false">
              <position x="470" y="230"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="25" formalParameter="OUT_MV2">
                  <position x="470" y="250"/>
                  <position x="445" y="250"/>
                  <position x="445" y="190"/>
                  <position x="390" y="190"/>
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
              <position x="140" y="200"/>
              <connectionPointOut>
                <relPosition x="50" y="10"/>
              </connectionPointOut>
              <expression>TLB1</expression>
            </inVariable>
            <inVariable localId="24" height="30" width="50" negated="false">
              <position x="140" y="250"/>
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
                      <position x="200" y="170"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB1">
                  <connectionPointIn>
                    <relPosition x="0" y="80"/>
                    <connection refLocalId="23">
                      <position x="260" y="190"/>
                      <position x="225" y="190"/>
                      <position x="225" y="210"/>
                      <position x="190" y="210"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN_TLB2">
                  <connectionPointIn>
                    <relPosition x="0" y="110"/>
                    <connection refLocalId="24">
                      <position x="260" y="220"/>
                      <position x="230" y="220"/>
                      <position x="230" y="270"/>
                      <position x="190" y="270"/>
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
              <position x="450" y="340"/>
              <connectionPointIn>
                <relPosition x="0" y="10"/>
                <connection refLocalId="27" formalParameter="OUT_MV1">
                  <position x="450" y="350"/>
                  <position x="400" y="350"/>
                  <position x="400" y="330"/>
                  <position x="370" y="330"/>
                </connection>
              </connectionPointIn>
              <expression>MV1</expression>
            </outVariable>
            <outVariable localId="29" height="30" width="40" negated="false">
              <position x="450" y="390"/>
              <connectionPointIn>
                <relPosition x="0" y="20"/>
                <connection refLocalId="27" formalParameter="OUT_MV2">
                  <position x="450" y="410"/>
                  <position x="385" y="410"/>
                  <position x="385" y="350"/>
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

## g_timer_latch_mix

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !(Alarm && Ack)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Door obstruction alarm: a sustained obstruction sets a latched alarm,
     and an operator acknowledgement clears it. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_timer_latch_mix"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_timer_latch_mix" pouType="program">
    <interface><inputVars><variable name="Trig"><type><BOOL /></type></variable><variable name="Ack"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Alarm"><type><BOOL /></type></variable></outputVars><localVars><variable name="T0"><type><derived name="TON" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Trig</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#30ms</expression></inVariable>
      <block localId="5" width="80" height="80" typeName="TON" instanceName="T0"><position x="60" y="10" /><inputVariables><variable formalParameter="IN"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PT"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="ET"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <coil localId="6" negated="false" storage="set"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Alarm</variable></coil>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Ack</variable></contact>
      <coil localId="9" negated="false" storage="reset"><position x="160" y="90" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>Alarm</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /><connection refLocalId="9" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_timer_latch_mix" /></task></resource></configuration></configurations></instances>
</project>
```

## g_tof_hold

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Pir || Light

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Stairwell light: an off-delay holds the lamp after the PIR clears,
     and a manual button drives it directly. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_tof_hold"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_tof_hold" pouType="program">
    <interface><inputVars><variable name="Pir"><type><BOOL /></type></variable><variable name="Button"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Light"><type><BOOL /></type></variable></outputVars><localVars><variable name="TOF0"><type><derived name="TOF" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Pir</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#50ms</expression></inVariable>
      <block localId="5" width="80" height="80" typeName="TOF" instanceName="TOF0"><position x="60" y="10" /><inputVariables><variable formalParameter="IN"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PT"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="ET"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Button</variable></contact>
      <coil localId="7" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>Light</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_tof_hold" /></task></resource></configuration></configurations></instances>
</project>
```
