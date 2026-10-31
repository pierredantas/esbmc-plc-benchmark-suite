# Batch 8: benchmarks g_ton_single, g_tp_pulse, g_traffic_light, g_traffic_light_pedestrian, g_transformer_protect, g_trip_lockout_86, g_two_hand, g_two_hand_fb

## g_ton_single

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Light || Btn

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_ton_single"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_ton_single" pouType="program">
    <interface><inputVars><variable name="Btn"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Light"><type><BOOL /></type></variable></outputVars><localVars><variable name="TON0"><type><derived name="TON" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Btn</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#30ms</expression></inVariable>
      <block localId="5" width="80" height="60" typeName="TON" instanceName="TON0">
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
      <coil localId="6" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Light</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_ton_single" /></task></resource></configuration></configurations></instances>
</project>
```

## g_tp_pulse

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Out || Trig

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Reject gate: a trigger fires a fixed-width pulse, which holds the gate
     open for the full pulse even if the trigger drops. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_tp_pulse"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_tp_pulse" pouType="program">
    <interface><inputVars><variable name="Trig"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Out"><type><BOOL /></type></variable></outputVars><localVars><variable name="TP0"><type><derived name="TP" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Trig</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#30ms</expression></inVariable>
      <block localId="5" width="80" height="80" typeName="TP" instanceName="TP0"><position x="60" y="10" /><inputVariables><variable formalParameter="IN"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PT"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="ET"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <coil localId="6" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Out</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_tp_pulse" /></task></resource></configuration></configurations></instances>
</project>
```

## g_traffic_light

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['ns_green', 'ew_green']

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_traffic_light_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_traffic_light_clean" pouType="program">
      <interface><inputVars><variable name="ns_req"><type><BOOL /></type></variable><variable name="ew_req"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="ns_green"><type><BOOL /></type></variable><variable name="ew_green"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>ew_req</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>ns_req</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>ns_green</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>ew_req</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>ew_green</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_traffic_light_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_traffic_light_pedestrian

- Language: LD-graphical
- File: plc.xml
- Properties:
- P1 (invariant): !(RED_LIGHT && GREEN_LIGHT)
- P2 (invariant): !(PEDESTRIAN_GREEN_LIGHT && GREEN_LIGHT)

```xml
<?xml version='1.0' encoding='utf-8'?>
<project xmlns="http://www.plcopen.org/xml/tc6_0201" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xhtml="http://www.w3.org/1999/xhtml" xsi:schemaLocation="http://www.plcopen.org/xml/tc6_0201">
  <fileHeader companyName="Beremiz" productName="Unnamed" productVersion="1" creationDateTime="2012-09-04T16:16:33"/>
  <contentHeader name="traffic_lights" modificationDateTime="2021-10-01T22:28:55">
    <coordinateInfo>
      <fbd>
        <scaling x="0" y="0"/>
      </fbd>
      <ld>
        <scaling x="0" y="0"/>
      </ld>
      <sfc>
        <scaling x="0" y="0"/>
      </sfc>
    </coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes/>
    <pous>
      <pou name="traffic_light_sequence" pouType="functionBlock">
        <interface>
          <inputVars>
            <variable name="SWITCH_BUTTON">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="PEDESTRIAN_BUTTON">
              <type>
                <BOOL/>
              </type>
            </variable>
          </inputVars>
          <outputVars>
            <variable name="RED_LIGHT">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="ORANGE_LIGHT">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="GREEN_LIGHT">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="PEDESTRIAN_RED_LIGHT">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="PEDESTRIAN_GREEN_LIGHT">
              <type>
                <BOOL/>
              </type>
            </variable>
          </outputVars>
          <localVars>
            <variable name="TON1">
              <type>
                <derived name="TON"/>
              </type>
            </variable>
            <variable name="TON2">
              <type>
                <derived name="TON"/>
              </type>
            </variable>
            <variable name="ALLOW_CARS">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="WARN_CARS">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="STOP_CARS">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="ALLOW_PEDESTRIANS">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="STOP_PEDESTRIANS">
              <type>
                <BOOL/>
              </type>
            </variable>
            <variable name="TON3">
              <type>
                <derived name="TON"/>
              </type>
            </variable>
            <variable name="R_TRIG0">
              <type>
                <derived name="R_TRIG"/>
              </type>
            </variable>
            <variable name="R_TRIG1">
              <type>
                <derived name="R_TRIG"/>
              </type>
            </variable>
            <variable name="SR0">
              <type>
                <derived name="SR"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <actions>
          <action name="BLINK_ORANGE_LIGHT">
            <body>
              <LD>
                <leftPowerRail localId="1" height="40" width="3">
                  <position x="54" y="123"/>
                  <connectionPointOut formalParameter="">
                    <relPosition x="3" y="20"/>
                  </connectionPointOut>
                </leftPowerRail>
                <contact localId="2" height="15" width="21" negated="true">
                  <position x="121" y="135"/>
                  <connectionPointIn>
                    <relPosition x="0" y="8"/>
                    <connection refLocalId="1">
                      <position x="121" y="143"/>
                      <position x="56" y="143"/>
                    </connection>
                  </connectionPointIn>
                  <connectionPointOut>
                    <relPosition x="21" y="8"/>
                  </connectionPointOut>
                  <variable>ORANGE_LIGHT</variable>
                </contact>
                <block localId="3" width="97" height="102" typeName="TON" instanceName="TON1">
                  <position x="216" y="103"/>
                  <inputVariables>
                    <variable formalParameter="IN">
                      <connectionPointIn>
                        <relPosition x="0" y="40"/>
                        <connection refLocalId="2">
                          <position x="216" y="143"/>
                          <position x="142" y="143"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                    <variable formalParameter="PT">
                      <connectionPointIn>
                        <relPosition x="0" y="81"/>
                        <connection refLocalId="4">
                          <position x="216" y="184"/>
                          <position x="151" y="184"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                  </inputVariables>
                  <inOutVariables/>
                  <outputVariables>
                    <variable formalParameter="Q">
                      <connectionPointOut>
                        <relPosition x="97" y="40"/>
                      </connectionPointOut>
                    </variable>
                    <variable formalParameter="ET">
                      <connectionPointOut>
                        <relPosition x="97" y="81"/>
                      </connectionPointOut>
                    </variable>
                  </outputVariables>
                </block>
                <inVariable localId="4" height="37" width="76" negated="false">
                  <position x="75" y="166"/>
                  <connectionPointOut>
                    <relPosition x="76" y="18"/>
                  </connectionPointOut>
                  <expression>T#500ms</expression>
                </inVariable>
                <block localId="5" width="97" height="106" typeName="TON" instanceName="TON2">
                  <position x="216" y="251"/>
                  <inputVariables>
                    <variable formalParameter="IN">
                      <connectionPointIn>
                        <relPosition x="0" y="41"/>
                        <connection refLocalId="14">
                          <position x="216" y="292"/>
                          <position x="155" y="292"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                    <variable formalParameter="PT">
                      <connectionPointIn>
                        <relPosition x="0" y="84"/>
                        <connection refLocalId="15">
                          <position x="216" y="335"/>
                          <position x="162" y="335"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                  </inputVariables>
                  <inOutVariables/>
                  <outputVariables>
                    <variable formalParameter="Q">
                      <connectionPointOut>
                        <relPosition x="97" y="41"/>
                      </connectionPointOut>
                    </variable>
                    <variable formalParameter="ET">
                      <connectionPointOut>
                        <relPosition x="97" y="84"/>
                      </connectionPointOut>
                    </variable>
                  </outputVariables>
                </block>
                <coil localId="6" height="15" width="21" storage="reset">
                  <position x="517" y="284"/>
                  <connectionPointIn>
                    <relPosition x="0" y="8"/>
                    <connection refLocalId="10" formalParameter="Q">
                      <position x="517" y="292"/>
                      <position x="427" y="292"/>
                    </connection>
                  </connectionPointIn>
                  <connectionPointOut>
                    <relPosition x="21" y="8"/>
                  </connectionPointOut>
                  <variable>ORANGE_LIGHT</variable>
                </coil>
                <rightPowerRail localId="7" height="40" width="3">
                  <position x="598" y="123"/>
                  <connectionPointIn>
                    <relPosition x="0" y="20"/>
                    <connection refLocalId="8">
                      <position x="598" y="143"/>
                      <position x="530" y="143"/>
                    </connection>
                  </connectionPointIn>
                </rightPowerRail>
                <coil localId="8" height="15" width="21" storage="set">
                  <position x="509" y="135"/>
                  <connectionPointIn>
                    <relPosition x="0" y="8"/>
                    <connection refLocalId="11" formalParameter="Q">
                      <position x="509" y="143"/>
                      <position x="428" y="143"/>
                    </connection>
                  </connectionPointIn>
                  <connectionPointOut>
                    <relPosition x="21" y="8"/>
                  </connectionPointOut>
                  <variable>ORANGE_LIGHT</variable>
                </coil>
                <comment localId="9" height="52" width="318">
                  <position x="51" y="11"/>
                  <content>
                    <xhtml:p><![CDATA[This action makes the orange light blink]]></xhtml:p>
                  </content>
                </comment>
                <block localId="10" width="58" height="40" typeName="R_TRIG" instanceName="R_TRIG0">
                  <position x="370" y="262"/>
                  <inputVariables>
                    <variable formalParameter="CLK">
                      <connectionPointIn>
                        <relPosition x="0" y="30"/>
                        <connection refLocalId="5" formalParameter="Q">
                          <position x="370" y="292"/>
                          <position x="313" y="292"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                  </inputVariables>
                  <inOutVariables/>
                  <outputVariables>
                    <variable formalParameter="Q">
                      <connectionPointOut>
                        <relPosition x="58" y="30"/>
                      </connectionPointOut>
                    </variable>
                  </outputVariables>
                </block>
                <block localId="11" width="58" height="40" typeName="R_TRIG" instanceName="R_TRIG1">
                  <position x="371" y="113"/>
                  <inputVariables>
                    <variable formalParameter="CLK">
                      <connectionPointIn>
                        <relPosition x="0" y="30"/>
                        <connection refLocalId="3" formalParameter="Q">
                          <position x="371" y="143"/>
                          <position x="313" y="143"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                  </inputVariables>
                  <inOutVariables/>
                  <outputVariables>
                    <variable formalParameter="Q">
                      <connectionPointOut>
                        <relPosition x="58" y="30"/>
                      </connectionPointOut>
                    </variable>
                  </outputVariables>
                </block>
                <rightPowerRail localId="12" height="40" width="3">
                  <position x="597" y="272"/>
                  <connectionPointIn>
                    <relPosition x="0" y="20"/>
                    <connection refLocalId="6">
                      <position x="597" y="292"/>
                      <position x="538" y="292"/>
                    </connection>
                  </connectionPointIn>
                </rightPowerRail>
                <leftPowerRail localId="13" height="40" width="3">
                  <position x="67" y="272"/>
                  <connectionPointOut formalParameter="">
                    <relPosition x="3" y="20"/>
                  </connectionPointOut>
                </leftPowerRail>
                <contact localId="14" height="15" width="21">
                  <position x="134" y="284"/>
                  <connectionPointIn>
                    <relPosition x="0" y="8"/>
                    <connection refLocalId="13">
                      <position x="134" y="292"/>
                      <position x="69" y="292"/>
                    </connection>
                  </connectionPointIn>
                  <connectionPointOut>
                    <relPosition x="21" y="8"/>
                  </connectionPointOut>
                  <variable>ORANGE_LIGHT</variable>
                </contact>
                <inVariable localId="15" height="36" width="77" negated="false">
                  <position x="85" y="317"/>
                  <connectionPointOut>
                    <relPosition x="77" y="18"/>
                  </connectionPointOut>
                  <expression>T#500ms</expression>
                </inVariable>
              </LD>
            </body>
          </action>
        </actions>
        <transitions>
          <transition name="STOP">
            <body>
              <FBD>
                <block localId="42" width="59" height="53" typeName="NOT" executionOrderId="0">
                  <position x="237" y="31"/>
                  <inputVariables>
                    <variable formalParameter="IN">
                      <connectionPointIn>
                        <relPosition x="0" y="36"/>
                        <connection refLocalId="43">
                          <position x="237" y="67"/>
                          <position x="202" y="67"/>
                        </connection>
                      </connectionPointIn>
                    </variable>
                  </inputVariables>
                  <inOutVariables/>
                  <outputVariables>
                    <variable formalParameter="OUT">
                      <connectionPointOut>
                        <relPosition x="59" y="36"/>
                      </connectionPointOut>
                    </variable>
                  </outputVariables>
                </block>
                <inVariable localId="43" height="39" width="164" executionOrderId="0" negated="false">
                  <position x="38" y="48"/>
                  <connectionPointOut>
                    <relPosition x="164" y="19"/>
                  </connectionPointOut>
                  <expression>SWITCH_BUTTON</expression>
                </inVariable>
                <outVariable localId="44" height="40" width="46" executionOrderId="0" negated="false">
                  <position x="351" y="47"/>
                  <connectionPointIn>
                    <relPosition x="0" y="20"/>
                    <connection refLocalId="42" formalParameter="OUT">
                      <position x="351" y="67"/>
                      <position x="296" y="67"/>
                    </connection>
                  </connectionPointIn>
                  <expression>STOP</expression>
                </outVariable>
              </FBD>
            </body>
          </transition>
        </transitions>
        <body>
          <SFC>
            <step localId="1" height="37" width="121" name="Standstill" initialStep="true">
              <position x="509" y="31"/>
              <connectionPointIn>
                <relPosition x="60" y="0"/>
                <connection refLocalId="39">
                  <position x="569" y="31"/>
                  <position x="569" y="11"/>
                  <position x="963" y="11"/>
                  <position x="963" y="1151"/>
                  <position x="776" y="1151"/>
                  <position x="776" y="1097"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="60" y="37"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="121" y="18"/>
              </connectionPointOutAction>
            </step>
            <transition localId="2" height="2" width="20">
              <position x="559" y="222"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="1">
                  <position x="569" y="222"/>
                  <position x="569" y="68"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[SWITCH_BUTTON]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <step localId="3" height="30" width="118" name="ORANGE">
              <position x="510" y="250"/>
              <connectionPointIn>
                <relPosition x="59" y="0"/>
                <connection refLocalId="2">
                  <position x="569" y="250"/>
                  <position x="569" y="224"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="59" y="30"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="118" y="15"/>
              </connectionPointOutAction>
            </step>
            <transition localId="6" height="2" width="20">
              <position x="559" y="376"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="15">
                  <position x="569" y="376"/>
                  <position x="569" y="336"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[STOP_CARS]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <actionBlock localId="8" width="231" height="162">
              <position x="711" y="34"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="1">
                  <position x="711" y="49"/>
                  <position x="630" y="49"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="P">
                <relPosition x="0" y="0"/>
                <inline>
                  <ST>
                    <xhtml:p><![CDATA[ORANGE_LIGHT := 1;]]></xhtml:p>
                  </ST>
                </inline>
              </action>
              <action localId="0">
                <relPosition x="0" y="0"/>
                <reference name="BLINK_ORANGE_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_GREEN_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="GREEN_LIGHT"/>
              </action>
            </actionBlock>
            <actionBlock localId="9" width="232" height="125">
              <position x="711" y="250"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="3">
                  <position x="711" y="265"/>
                  <position x="628" y="265"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="GREEN_LIGHT"/>
              </action>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="ORANGE_LIGHT"/>
              </action>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="D" duration="T#2s">
                <relPosition x="0" y="0"/>
                <reference name="STOP_CARS"/>
              </action>
            </actionBlock>
            <step localId="10" height="34" width="92" name="RED">
              <position x="523" y="411"/>
              <connectionPointIn>
                <relPosition x="46" y="0"/>
                <connection refLocalId="6">
                  <position x="569" y="411"/>
                  <position x="569" y="378"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="46" y="34"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="92" y="17"/>
              </connectionPointOutAction>
            </step>
            <actionBlock localId="11" width="235" height="103">
              <position x="710" y="413"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="10">
                  <position x="710" y="428"/>
                  <position x="615" y="428"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="ORANGE_LIGHT"/>
              </action>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="D" duration="T#2s">
                <relPosition x="0" y="0"/>
                <reference name="ALLOW_PEDESTRIANS"/>
              </action>
            </actionBlock>
            <transition localId="12" height="2" width="20">
              <position x="559" y="533"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="7">
                  <position x="569" y="533"/>
                  <position x="569" y="487"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[ALLOW_PEDESTRIANS]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <selectionDivergence localId="15" height="1" width="154">
              <position x="415" y="335"/>
              <connectionPointIn>
                <relPosition x="154" y="0"/>
                <connection refLocalId="3">
                  <position x="569" y="335"/>
                  <position x="569" y="280"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="154" y="1"/>
              </connectionPointOut>
            </selectionDivergence>
            <transition localId="16" height="2" width="20">
              <position x="405" y="377"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="15">
                  <position x="415" y="377"/>
                  <position x="415" y="336"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <reference name="STOP"/>
              </condition>
            </transition>
            <jumpStep localId="17" height="13" width="12" targetName="Standstill">
              <position x="409" y="418"/>
              <connectionPointIn>
                <relPosition x="6" y="0"/>
                <connection refLocalId="16">
                  <position x="415" y="418"/>
                  <position x="415" y="379"/>
                </connection>
              </connectionPointIn>
            </jumpStep>
            <transition localId="4" height="2" width="20">
              <position x="400" y="528"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="7">
                  <position x="410" y="528"/>
                  <position x="410" y="487"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <reference name="STOP"/>
              </condition>
            </transition>
            <jumpStep localId="5" height="13" width="12" targetName="Standstill">
              <position x="404" y="553"/>
              <connectionPointIn>
                <relPosition x="6" y="0"/>
                <connection refLocalId="4">
                  <position x="410" y="553"/>
                  <position x="410" y="530"/>
                </connection>
              </connectionPointIn>
            </jumpStep>
            <selectionDivergence localId="7" height="1" width="159">
              <position x="410" y="486"/>
              <connectionPointIn>
                <relPosition x="159" y="0"/>
                <connection refLocalId="10">
                  <position x="569" y="486"/>
                  <position x="569" y="445"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="159" y="1"/>
              </connectionPointOut>
            </selectionDivergence>
            <step localId="18" height="32" width="177" name="PEDESTRIAN_GREEN">
              <position x="481" y="572"/>
              <connectionPointIn>
                <relPosition x="88" y="0"/>
                <connection refLocalId="12">
                  <position x="569" y="572"/>
                  <position x="569" y="535"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="88" y="32"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="177" y="16"/>
              </connectionPointOutAction>
            </step>
            <actionBlock localId="19" width="247" height="110">
              <position x="708" y="573"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="18">
                  <position x="708" y="588"/>
                  <position x="658" y="588"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_GREEN_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="D" duration="T#10s">
                <relPosition x="0" y="0"/>
                <reference name="STOP_PEDESTRIANS"/>
              </action>
            </actionBlock>
            <transition localId="20" height="2" width="20">
              <position x="400" y="653"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="22">
                  <position x="410" y="653"/>
                  <position x="410" y="626"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[NOT SWITCH_BUTTON]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <jumpStep localId="21" height="13" width="12" targetName="Standstill">
              <position x="404" y="694"/>
              <connectionPointIn>
                <relPosition x="6" y="0"/>
                <connection refLocalId="20">
                  <position x="410" y="694"/>
                  <position x="410" y="655"/>
                </connection>
              </connectionPointIn>
            </jumpStep>
            <selectionDivergence localId="22" height="1" width="159">
              <position x="410" y="625"/>
              <connectionPointIn>
                <relPosition x="159" y="0"/>
                <connection refLocalId="18">
                  <position x="569" y="625"/>
                  <position x="569" y="615"/>
                  <position x="569" y="615"/>
                  <position x="569" y="604"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="159" y="1"/>
              </connectionPointOut>
            </selectionDivergence>
            <transition localId="23" height="2" width="20">
              <position x="559" y="709"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="22">
                  <position x="569" y="709"/>
                  <position x="569" y="626"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[STOP_PEDESTRIANS]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <step localId="24" height="30" width="148" name="PEDESTRIAN_RED">
              <position x="495" y="748"/>
              <connectionPointIn>
                <relPosition x="74" y="0"/>
                <connection refLocalId="23">
                  <position x="569" y="748"/>
                  <position x="569" y="711"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="74" y="30"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="148" y="15"/>
              </connectionPointOutAction>
            </step>
            <actionBlock localId="25" width="239" height="110">
              <position x="708" y="748"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="24">
                  <position x="708" y="763"/>
                  <position x="643" y="763"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="PEDESTRIAN_GREEN_LIGHT"/>
              </action>
              <action localId="0" qualifier="D" duration="T#2s">
                <relPosition x="0" y="0"/>
                <reference name="ALLOW_CARS"/>
              </action>
            </actionBlock>
            <transition localId="26" height="2" width="20">
              <position x="400" y="857"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="28">
                  <position x="410" y="857"/>
                  <position x="410" y="816"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <connectionPointIn>
                  <connection refLocalId="48">
                    <position x="400" y="858"/>
                    <position x="290" y="858"/>
                  </connection>
                </connectionPointIn>
              </condition>
            </transition>
            <jumpStep localId="27" height="13" width="12" targetName="Standstill">
              <position x="404" y="898"/>
              <connectionPointIn>
                <relPosition x="6" y="0"/>
                <connection refLocalId="26">
                  <position x="410" y="898"/>
                  <position x="410" y="859"/>
                </connection>
              </connectionPointIn>
            </jumpStep>
            <selectionDivergence localId="28" height="1" width="159">
              <position x="410" y="815"/>
              <connectionPointIn>
                <relPosition x="159" y="0"/>
                <connection refLocalId="24">
                  <position x="569" y="815"/>
                  <position x="569" y="778"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="159" y="1"/>
              </connectionPointOut>
            </selectionDivergence>
            <transition localId="29" height="2" width="20">
              <position x="559" y="879"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="28">
                  <position x="569" y="879"/>
                  <position x="569" y="816"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[ALLOW_CARS]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <step localId="30" height="33" width="92" name="GREEN">
              <position x="523" y="930"/>
              <connectionPointIn>
                <relPosition x="46" y="0"/>
                <connection refLocalId="29">
                  <position x="569" y="930"/>
                  <position x="569" y="881"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="46" y="33"/>
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="92" y="16"/>
              </connectionPointOutAction>
            </step>
            <actionBlock localId="31" width="227" height="110">
              <position x="709" y="931"/>
              <connectionPointIn>
                <relPosition x="0" y="15"/>
                <connection refLocalId="30">
                  <position x="709" y="946"/>
                  <position x="615" y="946"/>
                </connection>
              </connectionPointIn>
              <action localId="0" qualifier="S">
                <relPosition x="0" y="0"/>
                <reference name="GREEN_LIGHT"/>
              </action>
              <action localId="0" qualifier="R">
                <relPosition x="0" y="0"/>
                <reference name="RED_LIGHT"/>
              </action>
              <action localId="0" qualifier="D" duration="T#20s">
                <relPosition x="0" y="0"/>
                <reference name="WARN_CARS"/>
              </action>
            </actionBlock>
            <block localId="32" width="89" height="94" typeName="TON" instanceName="TON3">
              <position x="308" y="1053"/>
              <inputVariables>
                <variable formalParameter="IN">
                  <connectionPointIn>
                    <relPosition x="0" y="38"/>
                    <connection refLocalId="44" formalParameter="Q1">
                      <position x="308" y="1091"/>
                      <position x="291" y="1091"/>
                      <position x="291" y="1065"/>
                      <position x="275" y="1065"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="PT">
                  <connectionPointIn>
                    <relPosition x="0" y="75"/>
                    <connection refLocalId="34">
                      <position x="308" y="1128"/>
                      <position x="270" y="1128"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="Q">
                  <connectionPointOut>
                    <relPosition x="89" y="38"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="ET">
                  <connectionPointOut>
                    <relPosition x="89" y="75"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <inVariable localId="33" height="36" width="168" negated="false">
              <position x="15" y="1047"/>
              <connectionPointOut>
                <relPosition x="168" y="18"/>
              </connectionPointOut>
              <expression>PEDESTRIAN_BUTTON</expression>
            </inVariable>
            <inVariable localId="34" height="33" width="53" negated="false">
              <position x="217" y="1112"/>
              <connectionPointOut>
                <relPosition x="53" y="16"/>
              </connectionPointOut>
              <expression>T#2s</expression>
            </inVariable>
            <block localId="35" width="67" height="60" typeName="OR">
              <position x="459" y="1061"/>
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="32" formalParameter="Q">
                      <position x="459" y="1091"/>
                      <position x="397" y="1091"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="36">
                      <position x="459" y="1111"/>
                      <position x="427" y="1111"/>
                      <position x="427" y="1195"/>
                      <position x="260" y="1195"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="67" y="30"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <inVariable localId="36" height="30" width="97" negated="false">
              <position x="163" y="1182"/>
              <connectionPointOut>
                <relPosition x="97" y="15"/>
              </connectionPointOut>
              <expression>WARN_CARS</expression>
            </inVariable>
            <transition localId="37" height="2" width="20">
              <position x="559" y="1090"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="38">
                  <position x="569" y="1090"/>
                  <position x="569" y="1060"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <connectionPointIn>
                  <connection refLocalId="35" formalParameter="OUT">
                    <position x="559" y="1091"/>
                    <position x="526" y="1091"/>
                  </connection>
                </connectionPointIn>
              </condition>
            </transition>
            <selectionDivergence localId="38" height="1" width="207">
              <position x="569" y="1059"/>
              <connectionPointIn>
                <relPosition x="0" y="0"/>
                <connection refLocalId="30">
                  <position x="569" y="1059"/>
                  <position x="569" y="963"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1"/>
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="207" y="1"/>
              </connectionPointOut>
            </selectionDivergence>
            <transition localId="39" height="2" width="20">
              <position x="766" y="1095"/>
              <connectionPointIn>
                <relPosition x="10" y="0"/>
                <connection refLocalId="38">
                  <position x="776" y="1095"/>
                  <position x="776" y="1060"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2"/>
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <xhtml:p><![CDATA[NOT SWITCH_BUTTON]]></xhtml:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <jumpStep localId="41" height="13" width="12" targetName="ORANGE">
              <position x="563" y="1137"/>
              <connectionPointIn>
                <relPosition x="6" y="0"/>
                <connection refLocalId="37">
                  <position x="569" y="1137"/>
                  <position x="569" y="1092"/>
                </connection>
              </connectionPointIn>
            </jumpStep>
            <block localId="44" width="51" height="60" typeName="SR" instanceName="SR0">
              <position x="224" y="1035"/>
              <inputVariables>
                <variable formalParameter="S1">
                  <connectionPointIn>
                    <relPosition x="0" y="30"/>
                    <connection refLocalId="33">
                      <position x="224" y="1065"/>
                      <position x="183" y="1065"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="R">
                  <connectionPointIn>
                    <relPosition x="0" y="50"/>
                    <connection refLocalId="32" formalParameter="Q">
                      <position x="224" y="1085"/>
                      <position x="203" y="1085"/>
                      <position x="203" y="1167"/>
                      <position x="416" y="1167"/>
                      <position x="416" y="1091"/>
                      <position x="397" y="1091"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="Q1">
                  <connectionPointOut>
                    <relPosition x="51" y="30"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <comment localId="45" height="767" width="753">
              <position x="973" y="21"/>
              <content>
                <xhtml:p><![CDATA[*** Description of SFC action qualifiers ***

N : non-stored - The action code body is executed or the Boolean variable is set as
long as the step is active.

R : overriding reset &#8211; When the step has previously been executed with the S
(including DS, DS, and SL) qualifier, the R qualifier will stop the execution of the
code or reset the Boolean variable.

S : set (stored) - The action code body is executed or the Boolean variable is set.
This state is stored as soon as the step becomes active. It can only be reset
explicitly by associating the same action to a different step using the qualifier 'R'.

L : time limited - The action code body is executed or the Boolean variable is set as
long as the step is active but maximal for the fixed time interval.

D : time delayed - The action code body is executed or the Boolean variable is set
after the fixed delay time has elapsed. The action remains active as long as the step
is active. If the step is active shorter than the fixed delay time the action does not
become active.

P : pulse - As soon as the step is active the action code body is executed or the
Boolean variable is set for one operating cycle. (Note: The code body will then
execute for one additional operating cycle with the Step.X variable FALSE.)

SD : stored and time delayed - the action code body is executed or the Boolean
variable is stored and set when the fixed delay time has elapsed after the step
activation, even if the step becomes inactive. The action remains active until it is
reset. If the step is active shorter than the fixed delay time the action becomes active
anyway.

DS : delayed and stored - The action code body is executed or the Boolean variable
is set when the fixed delay time has elapsed after the step activation. The action
remains active until it is reset. If the step is active shorter than the fixed delay time
the action does not become active.

SL : stored and time limited - The action code body is executed or the Boolean
variable is set and stored for a fixed time interval as soon as the step is active. If the
step is active shorter than the time interval the action is active for the whole time
interval anyway. If the action is reset during the time interval the action becomes
inactive as soon as the action is reset.
]]></xhtml:p>
              </content>
            </comment>
            <comment localId="46" height="224" width="375">
              <position x="8" y="326"/>
              <content>
                <xhtml:p><![CDATA[Conditions can be written in any IEC 61131-3 language.
They can be implemented in defferent ways:
- reference to external implementation;
- inline implementation;
- written in FBD or LD on SFC diagram and connected to the condition.

See below examples of all these types.]]></xhtml:p>
              </content>
            </comment>
            <leftPowerRail localId="47" height="40" width="3">
              <position x="189" y="838"/>
              <connectionPointOut formalParameter="">
                <relPosition x="3" y="20"/>
              </connectionPointOut>
            </leftPowerRail>
            <contact localId="48" height="15" width="21" negated="true">
              <position x="269" y="850"/>
              <connectionPointIn>
                <relPosition x="0" y="8"/>
                <connection refLocalId="47">
                  <position x="269" y="858"/>
                  <position x="192" y="858"/>
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="21" y="8"/>
              </connectionPointOut>
              <variable>SWITCH_BUTTON</variable>
            </contact>
            <comment localId="13" height="86" width="379">
              <position x="9" y="28"/>
              <content>
                <xhtml:p><![CDATA[Sequential function chart (SFC) is commonly used to describe state machines.]]></xhtml:p>
              </content>
            </comment>
          </SFC>
        </body>
      </pou>
      <pou name="main_program" pouType="program">
        <interface>
          <localVars>
            <variable name="trafic_light_sequence0">
              <type>
                <derived name="traffic_light_sequence"/>
              </type>
            </variable>
            <variable name="SwitchButton">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="PedestrianButton">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="RedLight">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="OrangeLight">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="GreenLight">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="PedestrianRedLight">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
            <variable name="PedestrianGreenLight">
              <type>
                <derived name="HMI_BOOL"/>
              </type>
            </variable>
          </localVars>
        </interface>
        <body>
          <FBD>
            <block localId="1" width="350" height="836" typeName="traffic_light_sequence" instanceName="trafic_light_sequence0" executionOrderId="0">
              <position x="494" y="462"/>
              <inputVariables>
                <variable formalParameter="SWITCH_BUTTON">
                  <connectionPointIn>
                    <relPosition x="0" y="101"/>
                    <connection refLocalId="103">
                      <position x="494" y="563"/>
                      <position x="446" y="563"/>
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="PEDESTRIAN_BUTTON">
                  <connectionPointIn>
                    <relPosition x="0" y="264"/>
                    <connection refLocalId="104">
                      <position x="494" y="726"/>
                      <position x="438" y="726"/>
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables/>
              <outputVariables>
                <variable formalParameter="RED_LIGHT">
                  <connectionPointOut>
                    <relPosition x="350" y="101"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="ORANGE_LIGHT">
                  <connectionPointOut>
                    <relPosition x="350" y="264"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="GREEN_LIGHT">
                  <connectionPointOut>
                    <relPosition x="350" y="427"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="PEDESTRIAN_RED_LIGHT">
                  <connectionPointOut>
                    <relPosition x="350" y="590"/>
                  </connectionPointOut>
                </variable>
                <variable formalParameter="PEDESTRIAN_GREEN_LIGHT">
                  <connectionPointOut>
                    <relPosition x="350" y="753"/>
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <comment localId="24" height="287" width="1008">
              <position x="22" y="13"/>
              <content>
                <xhtml:p><![CDATA[This example implements control of traffic lights.

Basically it shows following features of Beremiz:
- web interface (SCADA) using integrated web server in SVGHMI extension;
- interaction with web UI;
- functional blocks in SFC language.




SVGHMI is extensions to build web interface to PLC. It has *integrated* web-server. So it's NOT necessary to install Apache, lighttpd or nginx for that!!!

As the program is running in PLC, web UI will be available at http://localhost:8009/.

Web interface is build as SVG file in Inkscape. To edit SVG file click 'Inkscape' button in 0x: SVGHMI extension. 
Inkscape is a free and open-source vector graphics editor. It's not part of Beremiz and needs to be installed separately.
]]></xhtml:p>
              </content>
            </comment>
            <comment localId="102" height="134" width="734">
              <position x="21" y="303"/>
              <content>
                <xhtml:p><![CDATA[In this example FB like 'Button', 'Led' and 'Text' are used. 
Back_id and sele_id inputs of these blocks are IDs  of graphic primitives in SVG file.
This is the way how elements in SVG are bound to elements in PLC program.
You can find out or edit these IDs in Inkscape.]]></xhtml:p>
              </content>
            </comment>
            <inVariable localId="103" executionOrderId="0" height="24" width="106" negated="false">
              <position x="340" y="551"/>
              <connectionPointOut>
                <relPosition x="106" y="12"/>
              </connectionPointOut>
              <expression>SwitchButton</expression>
            </inVariable>
            <inVariable localId="104" executionOrderId="0" height="24" width="138" negated="false">
              <position x="300" y="714"/>
              <connectionPointOut>
                <relPosition x="138" y="12"/>
              </connectionPointOut>
              <expression>PedestrianButton</expression>
            </inVariable>
            <outVariable localId="105" executionOrderId="0" height="24" width="74" negated="false">
              <position x="891" y="551"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="1" formalParameter="RED_LIGHT">
                  <position x="891" y="563"/>
                  <position x="844" y="563"/>
                </connection>
              </connectionPointIn>
              <expression>RedLight</expression>
            </outVariable>
            <outVariable localId="106" executionOrderId="0" height="24" width="98" negated="false">
              <position x="880" y="714"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="1" formalParameter="ORANGE_LIGHT">
                  <position x="880" y="726"/>
                  <position x="844" y="726"/>
                </connection>
              </connectionPointIn>
              <expression>OrangeLight</expression>
            </outVariable>
            <outVariable localId="107" executionOrderId="0" height="24" width="90" negated="false">
              <position x="881" y="877"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="1" formalParameter="GREEN_LIGHT">
                  <position x="881" y="889"/>
                  <position x="844" y="889"/>
                </connection>
              </connectionPointIn>
              <expression>GreenLight</expression>
            </outVariable>
            <outVariable localId="108" executionOrderId="0" height="24" width="154" negated="false">
              <position x="882" y="1040"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="1" formalParameter="PEDESTRIAN_RED_LIGHT">
                  <position x="882" y="1052"/>
                  <position x="844" y="1052"/>
                </connection>
              </connectionPointIn>
              <expression>PedestrianRedLight</expression>
            </outVariable>
            <outVariable localId="109" executionOrderId="0" height="24" width="170" negated="false">
              <position x="873" y="1203"/>
              <connectionPointIn>
                <relPosition x="0" y="12"/>
                <connection refLocalId="1" formalParameter="PEDESTRIAN_GREEN_LIGHT">
                  <position x="873" y="1215"/>
                  <position x="844" y="1215"/>
                </connection>
              </connectionPointIn>
              <expression>PedestrianGreenLight</expression>
            </outVariable>
          </FBD>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="config">
        <resource name="resource1">
          <task name="test_task" interval="T#100ms" priority="0">
            <pouInstance name="main_instance" typeName="main_program"/>
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_transformer_protect

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(transformer_on && oil_temp_high)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_transformer_protect_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_transformer_protect_clean" pouType="program">
    <interface><inputVars><variable name="energize_cmd"><type><BOOL /></type></variable><variable name="oil_temp_high"><type><BOOL /></type></variable><variable name="lockout"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="transformer_on"><type><BOOL /></type></variable><variable name="trip"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>oil_temp_high</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>energize_cmd</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>lockout</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>transformer_on</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>oil_temp_high</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>trip</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_transformer_protect_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_trip_lockout_86

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(lockout && reclose)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_trip_lockout_86_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_trip_lockout_86_clean" pouType="program">
    <interface><inputVars><variable name="protection_trip"><type><BOOL /></type></variable><variable name="manual_reset"><type><BOOL /></type></variable><variable name="reclose_request"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="lockout"><type><BOOL /></type></variable><variable name="reclose"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>protection_trip</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>lockout</variable></contact><contact localId="5" negated="true" storage="none" edge="none"><position x="40" y="20" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>manual_reset</variable></contact><coil localId="6" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="3" /><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>lockout</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>reclose_request</variable></contact><contact localId="8" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>lockout</variable></contact><contact localId="12" negated="true" storage="none" edge="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>protection_trip</variable></contact><coil localId="9" negated="false" storage="none"><position x="80" y="40" /><connectionPointIn><connection refLocalId="12" /></connectionPointIn><connectionPointOut /><variable>reclose</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_trip_lockout_86_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_two_hand

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Stroke || (LH && RH)

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

## g_two_hand_fb

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !Stroke || (LH && RH)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_two_hand_fb"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="TwoHandII" pouType="functionBlock">
      <interface>
        <inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars>
        <outputVars><variable name="Stroke"><type><BOOL /></type></variable></outputVars>
        <localVars><variable name="BothOff"><type><BOOL /></type></variable><variable name="Armed"><type><BOOL /></type></variable></localVars>
      </interface>
      <body><ST><xhtml:p><![CDATA[BothOff := NOT LH AND NOT RH;
Armed := (Armed OR BothOff) AND NOT Stroke;
Stroke := (Stroke OR Armed) AND LH AND RH;
]]></xhtml:p></ST></body>
    </pou>
    <pou name="g_two_hand_fb" pouType="program">
      <interface><inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Stroke"><type><BOOL /></type></variable></outputVars><localVars><variable name="THC0"><type><derived name="TwoHandII" /></type></variable></localVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <inVariable localId="3" height="20" width="60"><position x="20" y="30" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>LH</expression></inVariable>
        <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>RH</expression></inVariable>
        <block localId="5" width="120" height="80" typeName="TwoHandII" instanceName="THC0">
          <position x="100" y="10" />
          <inputVariables>
            <variable formalParameter="EN"><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="0" /></connectionPointIn></variable>
            <variable formalParameter="LH"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="3" /></connectionPointIn></variable>
            <variable formalParameter="RH"><connectionPointIn><relPosition x="0" y="70" /><connection refLocalId="4" /></connectionPointIn></variable>
          </inputVariables>
          <inOutVariables />
          <outputVariables>
            <variable formalParameter="ENO"><connectionPointOut><relPosition x="120" y="10" /></connectionPointOut></variable>
            <variable formalParameter="Stroke"><connectionPointOut><relPosition x="120" y="40" /></connectionPointOut></variable>
          </outputVariables>
        </block>
        <outVariable localId="6" height="20" width="60" negated="false"><position x="260" y="40" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="5" formalParameter="Stroke"><position x="220" y="50" /></connection></connectionPointIn><expression>Stroke</expression></outVariable>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_two_hand_fb" /></task></resource></configuration></configurations></instances>
</project>
```
