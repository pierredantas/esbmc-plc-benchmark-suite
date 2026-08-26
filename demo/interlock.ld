<?xml version="1.0" encoding="utf-8"?>
<!-- Reversing starter: ONE motor, TWO contactors.
     KM_CW  closes to run the motor clockwise
     KM_CCW closes to run it counter-clockwise (anticlockwise)
     Closing both at once shorts two supply phases through the reversing
     contacts, so the interlock below is a wiring-protection requirement,
     not a process preference.

     Rung 1:  KM_CW  := fwd AND NOT rev   (fwd contact, then a normally
              closed rev contact, driving the KM_CW coil)
     Rung 2:  KM_CCW := rev
-->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Demo" productName="Demo" productVersion="1" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="interlock">
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
          </inputVars>
          <outputVars>
            <variable name="KM_CW"><type><BOOL /></type></variable>
            <variable name="KM_CCW"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="0">
              <position x="0" y="0" /><connectionPointOut formalParameter="none" />
            </leftPowerRail>

            <!-- Rung 1 -->
            <contact localId="10" negated="false" storage="none" edge="none">
              <position x="20" y="10" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut /><variable>fwd</variable>
            </contact>
            <contact localId="11" negated="true" storage="none" edge="none">
              <position x="40" y="10" />
              <connectionPointIn><connection refLocalId="10" /></connectionPointIn>
              <connectionPointOut /><variable>rev</variable>
            </contact>
            <coil localId="12" negated="false" storage="none">
              <position x="60" y="10" />
              <connectionPointIn><connection refLocalId="11" /></connectionPointIn>
              <connectionPointOut /><variable>KM_CW</variable>
            </coil>

            <!-- Rung 2 -->
            <contact localId="20" negated="false" storage="none" edge="none">
              <position x="20" y="30" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut /><variable>rev</variable>
            </contact>
            <coil localId="21" negated="false" storage="none">
              <position x="60" y="30" />
              <connectionPointIn><connection refLocalId="20" /></connectionPointIn>
              <connectionPointOut /><variable>KM_CCW</variable>
            </coil>

            <rightPowerRail localId="2147483646">
              <position x="80" y="0" /><connectionPointIn />
            </rightPowerRail>
          </LD>
        </body>
      </pou>
    </pous>
  </types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="PT0.01S" priority="0">
      <pouInstance name="inst0" typeName="drive" />
    </task>
  </resource></configuration></configurations></instances>
</project>
