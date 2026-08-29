<?xml version="1.0" encoding="utf-8"?>
<!-- Analog feasibility probe: integer raw-to-engineering scaling in LD.
     scaled := raw * span / divisor, with divisor an input so it may be 0. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Probe" productName="Probe" productVersion="1" creationDateTime="2026-08-29T00:00:00" />
  <contentHeader name="scale_probe">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types><dataTypes /><pous><pou name="drive" pouType="program">
    <interface>
      <inputVars>
        <variable name="enable"><type><BOOL /></type></variable>
        <variable name="raw"><type><INT /></type></variable>
        <variable name="divisor"><type><INT /></type></variable>
      </inputVars>
      <outputVars>
        <variable name="scaled"><type><INT /></type></variable>
        <variable name="ok"><type><BOOL /></type></variable>
      </outputVars>
    </interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="10" negated="false" storage="none" edge="none">
        <position x="20" y="10" />
        <connectionPointIn><connection refLocalId="0" /></connectionPointIn>
        <connectionPointOut /><variable>enable</variable>
      </contact>
      <inVariable localId="11" height="20" width="60"><position x="20" y="40" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>raw</expression></inVariable>
      <inVariable localId="12" height="20" width="60"><position x="20" y="70" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>divisor</expression></inVariable>
      <block localId="13" width="60" height="40" typeName="DIV">
        <position x="120" y="40" />
        <inputVariables>
          <variable formalParameter="IN1"><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="11" /></connectionPointIn></variable>
          <variable formalParameter="IN2"><connectionPointIn><relPosition x="0" y="30" /><connection refLocalId="12" /></connectionPointIn></variable>
        </inputVariables>
        <inOutVariables />
        <outputVariables><variable formalParameter="OUT"><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut></variable></outputVariables>
      </block>
      <outVariable localId="14" height="20" width="60"><position x="220" y="40" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="13" formalParameter="OUT" /></connectionPointIn><expression>scaled</expression></outVariable>
      <coil localId="15" negated="false" storage="none">
        <position x="60" y="10" />
        <connectionPointIn><connection refLocalId="10" /></connectionPointIn>
        <connectionPointOut /><variable>ok</variable>
      </coil>
      <rightPowerRail localId="2147483646"><position x="300" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="drive" /></task></resource></configuration></configurations></instances>
</project>
