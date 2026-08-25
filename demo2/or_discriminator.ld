<?xml version="1.0" encoding="utf-8"?>
<!-- Two parallel branches into one coil:   Run := A OR B
     A ---| |---+---( Run )
                |
     B ---| |---+                                                    -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="x" productName="x" productVersion="1" creationDateTime="2026-01-01T00:00:00" />
  <contentHeader name="ortest"><coordinateInfo><ld><scaling x="1" y="1" /></ld></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="drive" pouType="program">
      <interface>
        <inputVars>
          <variable name="A"><type><BOOL /></type></variable>
          <variable name="B"><type><BOOL /></type></variable>
        </inputVars>
        <outputVars><variable name="Run"><type><BOOL /></type></variable></outputVars>
      </interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="10" negated="false" storage="none" edge="none">
          <position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn>
          <connectionPointOut /><variable>A</variable>
        </contact>
        <contact localId="11" negated="false" storage="none" edge="none">
          <position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn>
          <connectionPointOut /><variable>B</variable>
        </contact>
        <coil localId="12" negated="false" storage="none">
          <position x="50" y="10" />
          <connectionPointIn><connection refLocalId="10" /><connection refLocalId="11" /></connectionPointIn>
          <connectionPointOut /><variable>Run</variable>
        </coil>
        <rightPowerRail localId="2147483646"><position x="70" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="C"><resource name="R">
    <task name="t" interval="PT0.01S" priority="0"><pouInstance name="i" typeName="drive" /></task>
  </resource></configuration></configurations></instances>
</project>
