<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="x" productName="x" productVersion="1" creationDateTime="2026-08-27T00:00:00" />
  <contentHeader name="st_both"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="p" pouType="program">
    <interface><outputVars><variable name="A"><type><BOOL /></type></variable><variable name="B"><type><BOOL /></type></variable></outputVars></interface>
    <body>
      <ST><xhtml xmlns="http://www.w3.org/1999/xhtml">A := TRUE;
B := TRUE;
</xhtml></ST>
    </body>
  </pou></pous></types>
  <instances><configurations><configuration name="C"><resource name="R"><task name="t" interval="T#10ms" priority="0"><pouInstance name="i" typeName="p" /></task></resource></configuration></configurations></instances>
</project>
