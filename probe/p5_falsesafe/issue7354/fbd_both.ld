<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="x" productName="x" productVersion="1" creationDateTime="2026-08-27T00:00:00" />
  <contentHeader name="st_both"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="p" pouType="program">
    <interface><outputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable></outputVars></interface>
    <body>
      <FBD><inVariable localId="1" height="20" width="60"><position x="10" y="10" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>TRUE</expression></inVariable><outVariable localId="2" height="20" width="60"><position x="100" y="10" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="1"><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn><expression>A</expression></outVariable><outVariable localId="3" height="20" width="60"><position x="100" y="40" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="1"><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn><expression>B</expression></outVariable></FBD><!--

-->
    </body>
  </pou></pous></types>
  <instances><configurations><configuration name="C"><resource name="R"><task name="t" interval="T#10ms" priority="0"><pouInstance name="i" typeName="p" /></task></resource></configuration></configurations></instances>
</project>
