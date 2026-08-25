<?xml version="1.0" encoding="utf-8"?>
<!-- Forward/reverse motor interlock, 2 rungs of ladder.
     Rung 1:  fwd ---| |----|/|--- ( Motor_A )      Motor_A := fwd            <-- BUG: interlock removed
                            rev
     Rung 2:  rev ---| |------------( Motor_B )      Motor_B := rev
     NOTE: ESBMC-PLC v8.4 requires the .ld extension, but the CONTENT is PLCopen XML. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Demo" productName="Demo" productVersion="1" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="interlock_bug">
    <coordinateInfo><ld><scaling x="1" y="1" /></ld></coordinateInfo>
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
            <variable name="Motor_A"><type><BOOL /></type></variable>
            <variable name="Motor_B"><type><BOOL /></type></variable>
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
            <coil localId="12" negated="false" storage="none">
              <position x="60" y="10" />
              <connectionPointIn><connection refLocalId="10" /></connectionPointIn>
              <connectionPointOut /><variable>Motor_A</variable>
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
              <connectionPointOut /><variable>Motor_B</variable>
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
