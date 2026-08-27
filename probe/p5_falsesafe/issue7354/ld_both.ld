<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="x" productName="x" productVersion="1" creationDateTime="2026-08-27T00:00:00" />
  <contentHeader name="ld_both"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="p" pouType="program">
    <interface><outputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable></outputVars></interface>
    <body>
      <LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <coil localId="1" negated="false" storage="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>A</variable></coil>
        <coil localId="2" negated="false" storage="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>B</variable></coil>
        <rightPowerRail localId="9"><position x="99" y="0" /><connectionPointIn><connection refLocalId="1" /><connection refLocalId="2" /></connectionPointIn></rightPowerRail>
      </LD>
    </body>
  </pou></pous></types>
  <instances><configurations><configuration name="C"><resource name="R"><task name="t" interval="T#10ms" priority="0"><pouInstance name="i" typeName="p" /></task></resource></configuration></configurations></instances>
</project>
