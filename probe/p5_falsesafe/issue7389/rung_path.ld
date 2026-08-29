<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="R" productName="R" productVersion="1" creationDateTime="2026-08-29T00:00:00" />
  <contentHeader name="gt"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="drive" pouType="program">
    <interface>
      <inputVars>
        <variable name="level"><type><INT /></type></variable>
        <variable name="limit"><type><INT /></type></variable>
      </inputVars>
      <outputVars><variable name="alarm"><type><BOOL /></type></variable></outputVars>
    </interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <inVariable localId="1" height="20" width="60"><position x="20" y="20" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>level</expression></inVariable>
      <inVariable localId="2" height="20" width="60"><position x="20" y="50" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>limit</expression></inVariable>
      <block localId="3" width="60" height="40" typeName="GT">
        <position x="120" y="20" />
        <inputVariables>
          <variable formalParameter="IN1"><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="1" /></connectionPointIn></variable>
          <variable formalParameter="IN2"><connectionPointIn><relPosition x="0" y="30" /><connection refLocalId="2" /></connectionPointIn></variable>
        </inputVariables>
        <inOutVariables />
        <outputVariables><variable formalParameter="OUT"><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut></variable></outputVariables>
      </block>
      <coil localId="4" negated="false" storage="none">
        <position x="220" y="20" />
        <connectionPointIn><connection refLocalId="3" formalParameter="OUT" /></connectionPointIn>
        <connectionPointOut /><variable>alarm</variable>
      </coil>
      <rightPowerRail localId="2147483646"><position x="300" y="0" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="drive" /></task></resource></configuration></configurations></instances>
</project>
