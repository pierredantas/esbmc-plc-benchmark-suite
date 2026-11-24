# Review pack

Each entry gives the program, the property, the expected verdict, and the assumptions under which the verdict holds. See README.md for the questions.

## Stratum: timer or counter model

### counter_scalability (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(pump && level_high)`. Overflow guard; here evaluated across counter-fuse widths to measure detection cost vs. scale.

Variant `bomb_N00255.st`, expected verdict VIOLATION (expert):

```
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/255/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/255/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/255/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 255 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb_N01023.st`, expected verdict VIOLATION (expert):

```
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/1023/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/1023/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/1023/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 1023 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb_N04095.st`, expected verdict VIOLATION (expert):

```
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/4095/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/4095/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/4095/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 4095 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb_N16383.st`, expected verdict VIOLATION (expert):

```
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/16383/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/16383/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/16383/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 16383 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb_N32767.st`, expected verdict VIOLATION (expert):

```
(* ============================================================
   S5 - Counter-triggered time-bomb : SCALABILITY template
   Purpose: isolate the integer-state cost of a time-fuse so we
   can sweep the trigger threshold and compare ESBMC-PLC+
   k-induction / incremental-BMC against nuXmv BDD & IC3.
   This is the LLB analogue of PLC+'s nuXmv comparison: the
   counter fuse is exactly the integer state where BDD enumeration
   explodes (2^w states per w-bit accumulator) while ESBMC's
   bit-vector SMT reasons about all values in one query.

   THRESHOLD is the only knob. Generate variants with, e.g.:
     sed 's/32767/255/'   bomb_template.st > bomb_N00255.st   (8-bit)
     sed 's/32767/4095/'  bomb_template.st > bomb_N04095.st   (12-bit)
     sed 's/32767/32767/' bomb_template.st > bomb_N32767.st   (15-bit)
   (see gen_variants.sh). Property: absence "pump AND level_high".
   Expected ESBMC-PLC+ verdict: VIOLATION at every width;
   expected nuXmv BDD: blows up / times out as width grows.
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;
    start      AT %IX0.1 : BOOL;
    pump       AT %QX0.0 : BOOL;
    scan_cnt   : INT  := 0;
    armed      : BOOL := FALSE;
  END_VAR

  scan_cnt := scan_cnt + 1;
  IF scan_cnt >= 32767 THEN
    armed := TRUE;
  END_IF;

  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  IF level_high AND NOT armed THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : tank;
  END_RESOURCE
END_CONFIGURATION
```

### fbd_counter_reset (FBD, candidate)

Semantics: scan_order = tool-defined; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!Reset || (OUT == ResetCounterValue)`. Reset is a load, not a clear: on a scan where Reset holds, the counter output equals the supplied reset value rather than the incremented count.

Variant `program.xml`, expected verdict SAFE (expert):

Program has 149 lines; open `benchmarks/manufacturing/fbd_counter_reset/program.xml`.

### g_ctd_load (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(Empty && Load)`. Load is dominant: the count-down Empty flag and Load never hold together.

Variant `program.xml`, expected verdict SAFE (expert):

```
<?xml version="1.0" encoding="utf-8"?>
<!-- Car call queue: count served calls down to zero and flag Empty.
     Load restores the preset when a new batch of calls arrives. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="g_ctd_load"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_ctd_load" pouType="program">
    <interface><inputVars><variable name="Pulse"><type><BOOL /></type></variable><variable name="Load"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Empty"><type><BOOL /></type></variable></outputVars><localVars><variable name="CTD0"><type><derived name="CTD" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Pulse</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>2</expression></inVariable>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="90" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Load</variable></contact>
      <block localId="5" width="80" height="80" typeName="CTD" instanceName="CTD0"><position x="60" y="10" /><inputVariables><variable formalParameter="CD"><connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn></variable><variable formalParameter="PV"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="4" /></connectionPointIn></variable><variable formalParameter="LD"><connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="8" /></connectionPointIn></variable></inputVariables><inOutVariables /><outputVariables><variable formalParameter="Q"><connectionPointOut><relPosition x="80" y="20" /></connectionPointOut></variable><variable formalParameter="CV"><connectionPointOut><relPosition x="80" y="40" /></connectionPointOut></variable></outputVariables></block>
      <coil localId="6" negated="false" storage="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>Empty</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_ctd_load" /></task></resource></configuration></configurations></instances>
</project>
```

### g_guard_lock (LD-graphical, validated)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(Unlocked && Motor)`. ISO 14119 guard locking: the guard is never released while the drive is energised.

Variant `program.xml`, expected verdict SAFE (expert):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_guard_lock"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_guard_lock" pouType="program">
    <interface><inputVars><variable name="OpenReq"><type><BOOL /></type></variable><variable name="DoorClosed"><type><BOOL /></type></variable><variable name="RunCmd"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Motor"><type><BOOL /></type></variable><variable name="Unlocked"><type><BOOL /></type></variable></outputVars><localVars><variable name="Rundown"><type><derived name="TON" /></type></variable></localVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Motor</variable></contact>
      <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>T#30ms</expression></inVariable>
      <block localId="5" width="80" height="60" typeName="TON" instanceName="Rundown">
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
      <contact localId="6" negated="false" storage="none" edge="none"><position x="160" y="10" /><connectionPointIn><connection refLocalId="5" formalParameter="Q"><position x="140" y="30" /></connection></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact>
      <coil localId="7" negated="false" storage="none"><position x="200" y="10" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>Unlocked</variable></coil>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="100" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>RunCmd</variable></contact><contact localId="9" negated="false" storage="none" edge="none"><position x="40" y="100" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>DoorClosed</variable></contact><contact localId="10" negated="true" storage="none" edge="none"><position x="60" y="100" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact><coil localId="11" negated="false" storage="none"><position x="80" y="100" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Motor</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_guard_lock" /></task></resource></configuration></configurations></instances>
</project>
```

Variant `no_rundown.xml`, expected verdict SAFE (fault-injection):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_guard_lock_no_rundown"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_guard_lock_no_rundown" pouType="program">
    <interface><inputVars><variable name="OpenReq"><type><BOOL /></type></variable><variable name="DoorClosed"><type><BOOL /></type></variable><variable name="RunCmd"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Motor"><type><BOOL /></type></variable><variable name="Unlocked"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact><coil localId="7" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Unlocked</variable></coil>
      <contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="100" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>RunCmd</variable></contact><contact localId="9" negated="false" storage="none" edge="none"><position x="40" y="100" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>DoorClosed</variable></contact><contact localId="10" negated="true" storage="none" edge="none"><position x="60" y="100" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>OpenReq</variable></contact><coil localId="11" negated="false" storage="none"><position x="80" y="100" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Motor</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_guard_lock_no_rundown" /></task></resource></configuration></configurations></instances>
</project>
```

### g_ton_single (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!Light || Btn`. The on-delay light can be on only while the button is (or was recently) pressed.

Variant `program.xml`, expected verdict SAFE (expert):

```
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

### g_tp_pulse (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!Out || Trig`. The pulse output is asserted only in response to a trigger.

Variant `program.xml`, expected verdict VIOLATION (expert):

```
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

### il_counter_reset (IL, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!Reset || (OUT == ResetCounterValue)`. Reset is a load, not a clear: on a scan where Reset holds, the counter output equals the supplied reset value rather than the incremented count.

Variant `counter_reset.il`, expected verdict SAFE (expert):

```
(* counter_reset: a free-running counter with a reset-to-value.
   Reset loads ResetCounterValue, otherwise Cnt increments; OUT follows Cnt.
   Imported from the Beremiz IEC 61131-3 language test (CounterIL function block),
   re-expressed as a PROGRAM so it stands alone. See benchmark.yml for provenance. *)
PROGRAM drive
  VAR_INPUT
    Reset : BOOL;
    ResetCounterValue : INT;
  END_VAR
  VAR_OUTPUT
    OUT : INT;
  END_VAR
  VAR
    Cnt : INT;
  END_VAR

      LD    Reset
      JMPC  ResetCnt

      LD    Cnt
      ADD   1
      JMP   QuitFb

ResetCnt:
      LD    ResetCounterValue

QuitFb:
      ST    Cnt
      ST    OUT
END_PROGRAM
```

### ld_timer_latch_mix (LD-textual, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(Alarm && Ack)`. Acknowledge is dominant: the latched alarm and Ack never hold together.

Variant `timer_latch_mix.ld`, expected verdict SAFE (expert):

```
// timer_latch_mix: timer sets a latched alarm; ack clears it
TON(T0, 3, XIC(Trig)) ;
OTL(Alarm) := XIC(T0) ;
OTU(Alarm) := XIC(Ack) ;
```

### ld_tof_hold (LD-textual, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!Pir || Light`. While the PIR sees motion the lamp must be lit; the off-delay only extends that, it never shortens it.

Variant `tof_hold.ld`, expected verdict SAFE (expert):

```
// tof_hold: off-delay holds the light after the sensor clears (stairs-like)
TOF(TOF0_Q, 5, XIC(Pir)) ;
OTE(Light) := XIC(TOF0_Q) + XIC(Button) ;
```

### ld_tp_pulse (LD-textual, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!Out || Trig`. The pulse output is asserted only in response to a trigger.

Variant `tp_pulse.ld`, expected verdict VIOLATION (expert):

```
// tp_pulse: pulse timer holds output through the pulse even if input drops
TP(TP0_Q, 3, XIC(Trig)) ;
OTE(Out) := XIC(TP0_Q) ;
```

### st_guard_lock (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(Unlocked && Motor)`. ISO 14119 guard locking: the guard is never released while the drive is energised.

Variant `guard_lock.st`, expected verdict SAFE (expert):

```
(* guard_lock: interlocked guard with guard locking and a rundown timer.
   Structured Text rendering of g_guard_lock.

   ISO 14119 asks the guard to stay locked until the hazardous movement has
   stopped. A spindle keeps turning after its contactor drops, so the release
   waits out the rundown time rather than following the drive command. *)
PROGRAM cell
  VAR_INPUT
    OpenReq    : BOOL;
    DoorClosed : BOOL;
    RunCmd     : BOOL;
  END_VAR
  VAR_OUTPUT
    Motor    : BOOL;
    Unlocked : BOOL;
  END_VAR
  VAR
    Rundown : TON;
  END_VAR

  Rundown(IN := NOT Motor, PT := T#30ms);
  Unlocked := Rundown.Q AND OpenReq;
  Motor := RunCmd AND DoorClosed AND NOT OpenReq;
END_PROGRAM
```

### st_swat_timer1 (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; timer_counter_model = one scan per tick; verdict not assumed to transfer to another timing model; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle across the multi-PLC SWaT controller must complete. The malicious variant injects a Govil et al. LLB: a while-loop whose value never crosses the exit bound (e.g. i := i*i starting from 0), gated on a specific sensor value, so a scan hangs.

Variant `sleg_timer1_0.st`, expected verdict SAFE (cross-tool-consensus):

Program has 126 lines; open `benchmarks/water_treatment/st_swat_timer1/sleg_timer1_0.st`.

Variant `smal_timer1_0.st`, expected verdict VIOLATION (fault-injection):

Program has 133 lines; open `benchmarks/water_treatment/st_swat_timer1/smal_timer1_0.st`.

## Stratum: latch or seal-in

### conveyor_jam_lockout (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(belt_drive && jam_detected)`. The belt drive must never run while the jam sensor is tripped.
- P2 (invariant): `!(belt_drive && jam_this_run)`. Once a jam has been detected during a production run, the belt drive must stay off for the remainder of that run, even after the jam clears on its own, so an operator can inspect the line before the next run.
- P3 (reachability): `belt_drive && jam_this_run`. Trigger synthesis: a witness recovers the bad state P2 forbids, so the counterexample search has a concrete target when the run-lockout is bypassed.

Variant `clean.st`, expected verdict SAFE (expert):

```
(* ============================================================
   Packaging conveyor jam lockout.
   Safety intent: the belt drive must never run while the jam
   sensor is tripped. Once a jam has been detected during a
   production run, the belt drive stays off for the remainder of
   that run, even after the jam clears on its own, so an operator
   can inspect the line before the next run_start.
   ============================================================ *)
PROGRAM conveyor_control
  VAR
    jam_detected AT %IX0.0 : BOOL;
    run_start    AT %IX0.1 : BOOL;
    run_stop     AT %IX0.2 : BOOL;
    belt_drive     AT %QX0.0 : BOOL;
    jam_this_run : BOOL := FALSE;
    running       : BOOL := FALSE;
  END_VAR

  IF run_stop THEN
    running := FALSE;
    jam_this_run := FALSE;
  ELSIF run_start AND NOT jam_this_run THEN
    running := TRUE;
  END_IF;

  IF jam_detected THEN
    jam_this_run := TRUE;
  END_IF;

  IF jam_detected OR jam_this_run OR NOT running THEN
    belt_drive := FALSE;
  ELSE
    belt_drive := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : conveyor_control;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb.st`, expected verdict VIOLATION (fault-injection):

```
(* ============================================================
   Packaging conveyor jam lockout : BOMB variant.
   Seeded defect: the belt drive dispatch was reordered to check
   run_start priority before jam_this_run, on the reasoning that
   "a fresh run_start means the operator already inspected the
   line" — so once running is TRUE the jam_this_run latch is
   still set but no longer consulted by the belt output.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM conveyor_control
  VAR
    jam_detected AT %IX0.0 : BOOL;
    run_start    AT %IX0.1 : BOOL;
    run_stop     AT %IX0.2 : BOOL;
    belt_drive     AT %QX0.0 : BOOL;
    jam_this_run : BOOL := FALSE;
    running       : BOOL := FALSE;
  END_VAR

  IF run_stop THEN
    running := FALSE;
    jam_this_run := FALSE;
  ELSIF run_start AND NOT jam_this_run THEN
    running := TRUE;
  END_IF;

  IF jam_detected THEN
    jam_this_run := TRUE;
  END_IF;

  IF jam_detected THEN
    belt_drive := FALSE;
  ELSIF running THEN
    belt_drive := TRUE;
  ELSE
    belt_drive := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : conveyor_control;
  END_RESOURCE
END_CONFIGURATION
```

### dosing_pump_lockout (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(dosing_pump && level_low)`. The dosing pump must never run while the tank level is below the low-level cutoff.
- P2 (invariant): `!(dosing_pump && dry_run_fault)`. If the pump ever runs dry, any subsequent start command must be ignored and the pump must stay off, until an operator acknowledges the fault.
- P3 (reachability): `dosing_pump && dry_run_fault`. Trigger synthesis: a witness recovers the bad state P2 forbids, so the counterexample search has a concrete target when the fault acknowledgement requirement is bypassed.

Variant `clean.st`, expected verdict SAFE (expert):

```
(* ============================================================
   Water treatment dosing pump fault lockout.
   Safety intent: the dosing pump must never run while the tank
   level is below the low-level cutoff. If the pump ever runs dry
   (commanded on while below cutoff), any subsequent start command
   is ignored and the pump stays off, until an operator
   acknowledges the fault, regardless of how many times start is
   pressed afterward.
   ============================================================ *)
PROGRAM dosing_control
  VAR
    level_low     AT %IX0.0 : BOOL;
    start_cmd     AT %IX0.1 : BOOL;
    ack_fault     AT %IX0.2 : BOOL;
    dosing_pump     AT %QX0.0 : BOOL;
    dry_run_fault : BOOL := FALSE;
  END_VAR

  IF dosing_pump AND level_low THEN
    dry_run_fault := TRUE;
  ELSIF ack_fault THEN
    dry_run_fault := FALSE;
  END_IF;

  IF dry_run_fault OR level_low THEN
    dosing_pump := FALSE;
  ELSIF start_cmd THEN
    dosing_pump := TRUE;
  ELSE
    dosing_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dosing_control;
  END_RESOURCE
END_CONFIGURATION
```

Variant `bomb.st`, expected verdict VIOLATION (fault-injection):

```
(* ============================================================
   Water treatment dosing pump fault lockout : BOMB variant.
   Seeded defect: the pump dispatch was reordered to check
   start_cmd before dry_run_fault, so a held start command wins
   the branch the scan the dry-run fault is set, and the fault
   lockout only takes effect in scans where start_cmd happens to
   be false.
   Expected verdict: VIOLATION of P2 (witness: P3).
   ============================================================ *)
PROGRAM dosing_control
  VAR
    level_low     AT %IX0.0 : BOOL;
    start_cmd     AT %IX0.1 : BOOL;
    ack_fault     AT %IX0.2 : BOOL;
    dosing_pump     AT %QX0.0 : BOOL;
    dry_run_fault : BOOL := FALSE;
  END_VAR

  IF dosing_pump AND level_low THEN
    dry_run_fault := TRUE;
  ELSIF ack_fault THEN
    dry_run_fault := FALSE;
  END_IF;

  IF level_low THEN
    dosing_pump := FALSE;
  ELSIF start_cmd THEN
    dosing_pump := TRUE;
  ELSIF dry_run_fault THEN
    dosing_pump := FALSE;
  ELSE
    dosing_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : dosing_control;
  END_RESOURCE
END_CONFIGURATION
```

### fbd_seal_in (FBD, candidate)

Semantics: scan_order = tool-defined; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!Run || !Stop`. Stop always drops the seal-in coil: Run and Stop never hold together.

Variant `program.xml`, expected verdict SAFE (expert):

Program has 109 lines; open `benchmarks/motor_control/fbd_seal_in/program.xml`.

### g_two_hand (LD-graphical, validated)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!Stroke || (LH && RH)`. ISO 13851 requires the ram to descend only while both actuators are held. Releasing either one stops the stroke.

Variant `program.xml`, expected verdict SAFE (cross-tool-consensus):

```
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

Variant `type_i.xml`, expected verdict SAFE (fault-injection):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_two_hand_type_i"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_two_hand_type_i" pouType="program">
    <interface><inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars><outputVars><variable name="BothOff"><type><BOOL /></type></variable><variable name="Armed"><type><BOOL /></type></variable><variable name="Stroke"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>LH</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>RH</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>BothOff</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>BothOff</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>Armed</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="70" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>LH</variable></contact><contact localId="9" negated="false" storage="none" edge="none"><position x="40" y="70" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>RH</variable></contact><coil localId="10" negated="false" storage="none"><position x="60" y="70" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>Stroke</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_two_hand_type_i" /></task></resource></configuration></configurations></instances>
</project>
```

### ld_latch_basic (LD-textual, validated)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(Q && R)`. Unlatch is dominant within a scan: latched output Q and reset R never hold together.

Variant `latch_basic.ld`, expected verdict SAFE (expert):

```
// latch_basic: set/reset latch; unlatch dominant within a scan
OTL(Q) := XIC(S) ;
OTU(Q) := XIC(R) ;
```

### st_compressor_cycle (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(Load && PressHigh)`. The compressor never loads at or above the cut-out pressure.

Variant `compressor_cycle.st`, expected verdict SAFE (expert):

```
(* compressor_cycle: load/unload control for an air compressor.
   Structured Text rendering of g_compressor_cycle.

   The receiver's two pressure switches give the hysteresis band. MinOffDone is
   the interlock that stops the motor restarting into the same low pressure it
   just unloaded on. *)
PROGRAM compressor
  VAR_INPUT
    PressLow   : BOOL;
    PressHigh  : BOOL;
    MinOffDone : BOOL;
  END_VAR
  VAR_OUTPUT
    Load : BOOL;
  END_VAR

  Load := (Load OR (PressLow AND MinOffDone)) AND NOT PressHigh;
END_PROGRAM
```

### st_estop_reset (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(Run && EStop)`. ISO 13850 stop function: the drive is never energised while the emergency stop is actuated.

Variant `estop_reset.st`, expected verdict SAFE (expert):

```
(* estop_reset: emergency stop with a monitored manual reset.
   Structured Text rendering of g_estop_reset.

   ISO 13849-1 asks for the safety function to be restored by a separate manual
   action. The reset is taken on the falling edge of the button, so a reset that
   is bridged or held down cannot restore anything. EStop breaks the drive rung
   directly as well as through Safe, the way a hardwired stop breaks the coil
   circuit rather than waiting on the program. *)
PROGRAM drive
  VAR_INPUT
    EStop : BOOL;
    Reset : BOOL;
    Start : BOOL;
  END_VAR
  VAR_OUTPUT
    ResetEdge  : BOOL;
    Safe       : BOOL;
    Run        : BOOL;
    Reset_prev : BOOL;
  END_VAR

  ResetEdge := Reset_prev AND NOT Reset;
  Safe := (Safe OR ResetEdge) AND NOT EStop;
  Run := Safe AND Start AND NOT EStop;
  Reset_prev := Reset;
END_PROGRAM
```

### st_two_hand (ST, candidate)

Semantics: scan_order = sequential statement order; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!Stroke || (LH && RH)`. ISO 13851 requires the ram to descend only while both actuators are held. Releasing either one stops the stroke.

Variant `two_hand.st`, expected verdict SAFE (expert):

```
(* two_hand: Type II two-hand control on a power press.
   Structured Text rendering of g_two_hand.

   ISO 13851 Type II adds anti-tie-down and anti-repeat to the plain conjunction:
   the device arms only after both actuators have been released together, so a
   taped-down button leaves the press armed off however often the other is pressed. *)
PROGRAM press
  VAR_INPUT
    LH : BOOL;
    RH : BOOL;
  END_VAR
  VAR_OUTPUT
    BothOff : BOOL;
    Armed   : BOOL;
    Stroke  : BOOL;
  END_VAR

  BothOff := NOT LH AND NOT RH;
  Armed := (Armed OR BothOff) AND NOT Stroke;
  Stroke := (Stroke OR Armed) AND LH AND RH;
END_PROGRAM
```

## Stratum: integer overflow (H1)

### g_start_cycle (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (invariant): `!(STOP && CYCLE_ON)`. Classic seal-in safety: pressing STOP must release the holding circuit so the motor/cycle cannot remain energized.
- P2 (invariant): `!(START && STOP && CYCLE_ON)`. Simultaneous START and STOP should not leave the cycle active (STOP has priority).

Variant `lstart_cycle.xml`, expected verdict SAFE (expert):

Program has 550 lines; open `benchmarks/motor_control/g_start_cycle/lstart_cycle.xml`.

### g_tank_assignment (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle must complete (no non-terminating loop). The malicious variant injects a Govil et al. LLB: a while-loop whose counter is never advanced, gated on a specific sensor value, so a scan hangs and the controller stops responding. Program context: Direct assignment variant of the tank controller.

Variant `legitimate_lassignment.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 495 lines; open `benchmarks/water_treatment/g_tank_assignment/legitimate_lassignment.xml`.

Variant `malicious_massignment.xml`, expected verdict VIOLATION (fault-injection):

Program has 505 lines; open `benchmarks/water_treatment/g_tank_assignment/malicious_massignment.xml`.

### g_tank_start_eq (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle must complete (no non-terminating loop). The malicious variant injects a Govil et al. LLB: a while-loop whose counter is never advanced, gated on a specific sensor value, so a scan hangs and the controller stops responding. Program context: Start on level = threshold (EQ block).

Variant `legitimate_lstart_eq.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 532 lines; open `benchmarks/water_treatment/g_tank_start_eq/legitimate_lstart_eq.xml`.

Variant `malicious_mstart_eq.xml`, expected verdict VIOLATION (fault-injection):

Program has 601 lines; open `benchmarks/water_treatment/g_tank_start_eq/malicious_mstart_eq.xml`.

### g_tank_start_le (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle must complete (no non-terminating loop). The malicious variant injects a Govil et al. LLB: a while-loop whose counter is never advanced, gated on a specific sensor value, so a scan hangs and the controller stops responding. Program context: Start on level <= threshold (LE block).

Variant `legitimate_lstart_le.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 551 lines; open `benchmarks/water_treatment/g_tank_start_le/legitimate_lstart_le.xml`.

Variant `malicious_mstart_le.xml`, expected verdict VIOLATION (fault-injection):

Program has 600 lines; open `benchmarks/water_treatment/g_tank_start_le/malicious_mstart_le.xml`.

### g_tank_stop_ge (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle must complete (no non-terminating loop). The malicious variant injects a Govil et al. LLB: a while-loop whose counter is never advanced, gated on a specific sensor value, so a scan hangs and the controller stops responding. Program context: Stop on level >= threshold (GE block).

Variant `legitimate_lstop_ge.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 557 lines; open `benchmarks/water_treatment/g_tank_stop_ge/legitimate_lstop_ge.xml`.

Variant `malicious_mstop_ge.xml`, expected verdict VIOLATION (fault-injection):

Program has 605 lines; open `benchmarks/water_treatment/g_tank_stop_ge/malicious_mstop_ge.xml`.

### g_tank_value_filtering (LD-graphical, candidate)

Semantics: scan_order = sequential rung order within one scan; retained_state = values carry over between scans and are exchanged between program units; arithmetic = H1: no integer overflow; the program can overflow, so SAFE is conditional; verdict_scope = semantics-dependent

Properties:
- P1 (termination): `every scan cycle terminates within the iteration budget`. Every PLC scan cycle must complete (no non-terminating loop). The malicious variant injects a Govil et al. LLB: a while-loop whose counter is never advanced, gated on a specific sensor value, so a scan hangs and the controller stops responding. Program context: Sensor value-filtering stage before the valve logic.

Variant `legitimate_lvalue_filtering.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 561 lines; open `benchmarks/water_treatment/g_tank_value_filtering/legitimate_lvalue_filtering.xml`.

Variant `malicious_mvalue_filtering.xml`, expected verdict VIOLATION (fault-injection):

Program has 474 lines; open `benchmarks/water_treatment/g_tank_value_filtering/malicious_mvalue_filtering.xml`.

## Stratum: control (no timer, counter, latch or overflow dependence)

### g_bus_coupler_changeover (LD-graphical, validated)

Semantics: scan_order = sequential rung order within one scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(incomer_a && incomer_b && coupler)`. The coupler may parallel at most one healthy incomer onto the affected section; all three breakers must never be closed together.

Variant `clean.xml`, expected verdict SAFE (expert):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_bus_coupler_changeover_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_bus_coupler_changeover_clean" pouType="program">
    <interface><inputVars><variable name="incomer_a_healthy"><type><BOOL /></type></variable><variable name="incomer_b_healthy"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="incomer_a"><type><BOOL /></type></variable><variable name="incomer_b"><type><BOOL /></type></variable><variable name="coupler"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>incomer_a</variable></coil><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><coil localId="6" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>incomer_b</variable></coil><contact localId="7" negated="true" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><coil localId="9" negated="false" storage="none"><position x="60" y="50" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>coupler</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_bus_coupler_changeover_clean" /></task></resource></configuration></configurations></instances>
</project>
```

Variant `bomb.xml`, expected verdict VIOLATION (fault-injection):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_bus_coupler_changeover_bomb"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_bus_coupler_changeover_bomb" pouType="program">
    <interface><inputVars><variable name="incomer_a_healthy"><type><BOOL /></type></variable><variable name="incomer_b_healthy"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="incomer_a"><type><BOOL /></type></variable><variable name="incomer_b"><type><BOOL /></type></variable><variable name="coupler"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>incomer_a</variable></coil><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><coil localId="6" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>incomer_b</variable></coil><contact localId="7" negated="true" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><contact localId="8" negated="false" storage="none" edge="none"><position x="40" y="50" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>incomer_b_healthy</variable></contact><contact localId="10" negated="false" storage="none" edge="none"><position x="20" y="70" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>maint</variable></contact><contact localId="11" negated="false" storage="none" edge="none"><position x="40" y="70" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>incomer_a_healthy</variable></contact><coil localId="9" negated="false" storage="none"><position x="80" y="50" /><connectionPointIn><connection refLocalId="8" /><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>coupler</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_bus_coupler_changeover_bomb" /></task></resource></configuration></configurations></instances>
</project>
```

### g_motor_interlock (LD-graphical, validated)

Semantics: scan_order = sequential rung order within one scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (mutual_exclusion): `at most one of Motor_A, Motor_B`. Forward/reverse contactors must never be energised together (contactor short / mechanical damage).
- P2 (reachability): `Motor_A && Motor_B`. Trigger synthesis: a witness recovers the secret-knock input combination that violates the interlock.

Variant `clean.xml`, expected verdict SAFE (cross-tool-consensus):

Program has 80 lines; open `benchmarks/motor_control/g_motor_interlock/clean.xml`.

Variant `bomb.xml`, expected verdict VIOLATION (fault-injection):

Program has 94 lines; open `benchmarks/motor_control/g_motor_interlock/bomb.xml`.

### g_phase_hold_permissive (LD-graphical, validated)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!(held && heater)`. A phase held on permissive loss must keep the heater off; only clearing HELD through resume_command may re-enable heating.

Variant `clean.xml`, expected verdict SAFE (expert):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_phase_hold_permissive_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_phase_hold_permissive_clean" pouType="program">
    <interface><inputVars><variable name="run_command"><type><BOOL /></type></variable><variable name="agitator_ok"><type><BOOL /></type></variable><variable name="resume_command"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="held"><type><BOOL /></type></variable><variable name="heater"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="6" negated="true" storage="none" edge="none"><position x="40" y="20" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>resume_command</variable></contact><coil localId="7" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>held</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="9" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="13" negated="false" storage="none" edge="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><coil localId="10" negated="false" storage="none"><position x="80" y="40" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>heater</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_phase_hold_permissive_clean" /></task></resource></configuration></configurations></instances>
</project>
```

Variant `bomb.xml`, expected verdict VIOLATION (fault-injection):

```
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-09-02T00:00:00" />
  <contentHeader name="g_phase_hold_permissive_bomb"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_phase_hold_permissive_bomb" pouType="program">
    <interface><inputVars><variable name="run_command"><type><BOOL /></type></variable><variable name="agitator_ok"><type><BOOL /></type></variable><variable name="resume_command"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="held"><type><BOOL /></type></variable><variable name="heater"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="4" negated="true" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="20" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="6" negated="true" storage="none" edge="none"><position x="40" y="20" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>resume_command</variable></contact><coil localId="7" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>held</variable></coil><contact localId="8" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>run_command</variable></contact><contact localId="9" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="8" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="13" negated="false" storage="none" edge="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>agitator_ok</variable></contact><contact localId="11" negated="false" storage="none" edge="none"><position x="20" y="60" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>held</variable></contact><contact localId="12" negated="false" storage="none" edge="none"><position x="40" y="60" /><connectionPointIn><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>maint</variable></contact><coil localId="10" negated="false" storage="none"><position x="80" y="40" /><connectionPointIn><connection refLocalId="13" /><connection refLocalId="12" /></connectionPointIn><connectionPointOut /><variable>heater</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_phase_hold_permissive_bomb" /></task></resource></configuration></configurations></instances>
</project>
```

### ld_ftrig_edge (LD-textual, validated)

Semantics: scan_order = sequential rung order within one scan; retained_state = coils and edge or timer memory carry over from the previous scan; verdict_scope = holds under the stated scan order

Properties:
- P1 (invariant): `!OneShot || !Sig`. The falling-edge one-shot fires only when the signal is (now) low.

Variant `ftrig_edge.ld`, expected verdict SAFE (expert):

```
// ftrig_edge: falling-edge one-shot (F_TRIG lowering)
OTE(Fall) := XIO(Sig) * XIC(Sig_prev) ;
OTE(OneShot) := XIC(Fall) ;
OTE(Sig_prev) := XIC(Sig) ;
```
