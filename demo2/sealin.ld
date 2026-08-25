<?xml version="1.0" encoding="utf-8"?>
<!-- Motor start/stop with seal-in (latching) and an emergency stop.
     Start ---| |---+---|/|--- ( Run )     Run := (Start OR Run) AND NOT EStop
                    |   EStop
     Run   ---| |---+
     The Run contact feeds the coil's own output back in: that is the seal-in.
     EStop sits AFTER the OR junction, so it breaks both branches.       -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Demo" productName="Demo" productVersion="1" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="sealin"><coordinateInfo><ld><scaling x="1" y="1" /></ld></coordinateInfo></contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="drive" pouType="program">
        <interface>
          <inputVars>
            <variable name="Start"><type><BOOL /></type></variable>
            <variable name="EStop"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="Run"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <LD>
            <leftPowerRail localId="0">
              <position x="0" y="0" /><connectionPointOut formalParameter="none" />
            </leftPowerRail>
            <!-- branch 1: Start -->
            <contact localId="10" negated="false" storage="none" edge="none">
              <position x="20" y="10" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut /><variable>Start</variable>
            </contact>
            <!-- branch 2: the seal-in, Run feeding back -->
            <contact localId="11" negated="false" storage="none" edge="none">
              <position x="20" y="30" />
              <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
              <connectionPointOut /><variable>Run</variable>
            </contact>
            <!-- OR junction merges both branches into the EStop contact -->
            <contact localId="12" negated="true" storage="none" edge="none">
              <position x="45" y="10" />
              <connectionPointIn>
                <connection refLocalId="10" />
                <connection refLocalId="11" />
              </connectionPointIn>
              <connectionPointOut /><variable>EStop</variable>
            </contact>
            <coil localId="13" negated="false" storage="none">
              <position x="70" y="10" />
              <connectionPointIn><connection refLocalId="12" /></connectionPointIn>
              <connectionPointOut /><variable>Run</variable>
            </coil>
            <rightPowerRail localId="2147483646">
              <position x="90" y="0" /><connectionPointIn />
            </rightPowerRail>
          </LD>
        </body>
      </pou>
    </pous>
  </types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="PT0.01S" priority="0"><pouInstance name="inst0" typeName="drive" /></task>
  </resource></configuration></configurations></instances>
</project>
