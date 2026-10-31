# Batch 2: benchmarks fbd_counter_reset, fbd_fan_damper, fbd_reactor_2oo3, fbd_seal_in, g_batch_mixer, g_batch_reactor, g_building_lighting, g_burner_purge

## fbd_counter_reset

- Language: FBD
- File: program.xml
- Properties:
- P1 (invariant): !Reset || (OUT == ResetCounterValue)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- counter_reset: a free-running counter with a reset-to-value.
   Reset loads ResetCounterValue, otherwise Cnt increments; OUT follows Cnt.
   Imported from the Beremiz IEC 61131-3 language test (CounterFBD function block),
   re-expressed as a PROGRAM so it stands alone. See benchmark.yml for provenance. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-29T00:00:00" />
  <contentHeader name="fbd_counter_reset"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="drive" pouType="program">
    <interface>
      <inputVars>
        <variable name="Reset"><type><BOOL /></type></variable>
        <variable name="ResetCounterValue"><type><INT /></type></variable>
      </inputVars>
      <outputVars><variable name="OUT"><type><INT /></type></variable></outputVars>
      <localVars><variable name="Cnt"><type><INT /></type></variable></localVars>
    </interface>
    <body><FBD>
            <inVariable localId="1" executionOrderId="0" height="30" width="61" negated="false">
              <position x="321" y="58" />
              <connectionPointOut>
                <relPosition x="61" y="15" />
              </connectionPointOut>
              <expression>Reset</expression>
            </inVariable>
            <outVariable localId="2" executionOrderId="0" height="30" width="39" negated="false">
              <position x="675" y="137" />
              <connectionPointIn>
                <relPosition x="0" y="15" />
                <connection refLocalId="3">
                  <position x="675" y="152" />
                  <position x="589" y="152" />
                </connection>
              </connectionPointIn>
              <expression>OUT</expression>
            </outVariable>
            <inOutVariable localId="3" executionOrderId="0" height="30" width="37" negatedOut="false" negatedIn="false">
              <position x="557" y="137" />
              <connectionPointIn>
                <relPosition x="0" y="15" />
                <connection refLocalId="7" formalParameter="OUT">
                  <position x="557" y="152" />
                  <position x="527" y="152" />
                  <position x="527" y="130" />
                  <position x="517" y="130" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="37" y="15" />
              </connectionPointOut>
              <expression>Cnt</expression>
            </inOutVariable>
            <block localId="4" typeName="ADD" executionOrderId="0" height="80" width="69">
              <position x="328" y="115" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="35" />
                    <connection refLocalId="6">
                      <position x="328" y="150" />
                      <position x="275" y="150" />
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn>
                    <relPosition x="0" y="65" />
                    <connection refLocalId="3">
                      <position x="328" y="180" />
                      <position x="317" y="180" />
                      <position x="317" y="213" />
                      <position x="604" y="213" />
                      <position x="604" y="152" />
                      <position x="594" y="152" />
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="69" y="35" />
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <inVariable localId="5" executionOrderId="0" height="30" width="163" negated="false">
              <position x="222" y="256" />
              <connectionPointOut>
                <relPosition x="163" y="15" />
              </connectionPointOut>
              <expression>ResetCounterValue</expression>
            </inVariable>
            <inVariable localId="6" executionOrderId="0" height="30" width="21" negated="false">
              <position x="254" y="135" />
              <connectionPointOut>
                <relPosition x="21" y="15" />
              </connectionPointOut>
              <expression>1</expression>
            </inVariable>
            <block localId="7" typeName="SEL" executionOrderId="0" height="80" width="69">
              <position x="448" y="100" />
              <inputVariables>
                <variable formalParameter="G">
                  <connectionPointIn>
                    <relPosition x="0" y="30" />
                    <connection refLocalId="1">
                      <position x="448" y="130" />
                      <position x="415" y="130" />
                      <position x="415" y="73" />
                      <position x="382" y="73" />
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN0">
                  <connectionPointIn>
                    <relPosition x="0" y="50" />
                    <connection refLocalId="4" formalParameter="OUT">
                      <position x="448" y="150" />
                      <position x="397" y="150" />
                    </connection>
                  </connectionPointIn>
                </variable>
                <variable formalParameter="IN1">
                  <connectionPointIn>
                    <relPosition x="0" y="70" />
                    <connection refLocalId="5">
                      <position x="448" y="170" />
                      <position x="414" y="170" />
                      <position x="414" y="271" />
                      <position x="385" y="271" />
                    </connection>
                  </connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut>
                    <relPosition x="69" y="30" />
                  </connectionPointOut>
                </variable>
              </outputVariables>
            </block>
          </FBD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="drive" /></task></resource></configuration></configurations></instances>
</project>
```

## fbd_fan_damper

- Language: FBD
- File: clean.xml
- Properties:
- P1 (invariant): !(fan && !damper_open)
- P2 (invariant): !(fan && smoke)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Supply air fan with a motorised isolation damper and a duct smoke detector.
     fan := fan_cmd AND damper_open AND NOT smoke
     Starting the fan against a shut damper pulls the duct into vacuum;
     running it during a smoke alarm distributes smoke through the building. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="fbd_fan_damper_clean">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="air_handler" pouType="program">
        <interface>
          <inputVars>
            <variable name="fan_cmd"><type><BOOL /></type></variable>
            <variable name="damper_open"><type><BOOL /></type></variable>
            <variable name="smoke"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="fan"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <FBD>
            <inVariable localId="1" height="20" width="80">
              <position x="20" y="20" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>fan_cmd</expression>
            </inVariable>
            <inVariable localId="2" height="20" width="80">
              <position x="20" y="60" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>damper_open</expression>
            </inVariable>
            <inVariable localId="3" height="20" width="80">
              <position x="20" y="100" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>smoke</expression>
            </inVariable>
            <block localId="4" width="60" height="40" typeName="NOT">
              <position x="140" y="100" />
              <inputVariables>
                <variable formalParameter="IN">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="5" width="60" height="80" typeName="AND">
              <position x="240" y="20" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="1" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="2" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN3">
                  <connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="4" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="6" height="20" width="80">
              <position x="380" y="40" />
              <connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="5" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
              <expression>fan</expression>
            </outVariable>
          </FBD>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="air_handler" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## fbd_reactor_2oo3

- Language: FBD
- File: clean.xml
- Properties:
- P1 (invariant): !((ps1 && ps2) || (ps2 && ps3) || (ps1 && ps3)) || trip
- P2 (invariant): !trip || ((ps1 && ps2) || (ps2 && ps3) || (ps1 && ps3))

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Batch reactor overpressure trip voted two out of three pressure switches.
     trip := (ps1 AND ps2) OR (ps2 AND ps3) OR (ps1 AND ps3)
     One stuck-high switch must not trip production; two genuine highs must
     trip, or the vessel stays pressurised behind a closed relief path. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="fbd_reactor_2oo3_clean">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="trip_logic" pouType="program">
        <interface>
          <inputVars>
            <variable name="ps1"><type><BOOL /></type></variable>
            <variable name="ps2"><type><BOOL /></type></variable>
            <variable name="ps3"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="trip"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <FBD>
            <inVariable localId="1" height="20" width="80">
              <position x="20" y="20" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>ps1</expression>
            </inVariable>
            <inVariable localId="2" height="20" width="80">
              <position x="20" y="80" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>ps2</expression>
            </inVariable>
            <inVariable localId="3" height="20" width="80">
              <position x="20" y="140" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>ps3</expression>
            </inVariable>
            <block localId="4" width="60" height="60" typeName="AND">
              <position x="160" y="20" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="1" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="2" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="5" width="60" height="60" typeName="AND">
              <position x="160" y="90" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="2" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="3" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="6" width="60" height="60" typeName="AND">
              <position x="160" y="160" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="1" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="3" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="7" width="60" height="80" typeName="OR">
              <position x="300" y="60" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="4" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="5" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN3">
                  <connectionPointIn><relPosition x="0" y="60" /><connection refLocalId="6" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="8" height="20" width="80">
              <position x="440" y="80" />
              <connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="7" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
              <expression>trip</expression>
            </outVariable>
          </FBD>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="trip_logic" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## fbd_seal_in

- Language: FBD
- File: program.xml
- Properties:
- P1 (invariant): !Run || !Stop

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- seal_in: self-holding (seal-in) coil with stop.
     Function Block Diagram rendering of ld_seal_in / g_seal_in.
     Run := (Start OR Run) AND NOT Stop -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="fbd_seal_in">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="drive" pouType="program">
        <interface>
          <inputVars>
            <variable name="Start"><type><BOOL /></type></variable>
            <variable name="Stop"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="Run"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <FBD>
            <inVariable localId="1" height="20" width="80">
              <position x="20" y="20" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>Start</expression>
            </inVariable>
            <inVariable localId="2" height="20" width="80">
              <position x="20" y="60" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>Run</expression>
            </inVariable>
            <inVariable localId="3" height="20" width="80">
              <position x="20" y="140" />
              <connectionPointOut><relPosition x="80" y="10" /></connectionPointOut>
              <expression>Stop</expression>
            </inVariable>
            <block localId="4" width="60" height="60" typeName="OR">
              <position x="160" y="20" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="1" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="2" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="5" width="60" height="40" typeName="NOT">
              <position x="160" y="130" />
              <inputVariables>
                <variable formalParameter="IN">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <block localId="6" width="60" height="60" typeName="AND">
              <position x="300" y="60" />
              <inputVariables>
                <variable formalParameter="IN1">
                  <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="4" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
                <variable formalParameter="IN2">
                  <connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="5" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
                </variable>
              </inputVariables>
              <inOutVariables />
              <outputVariables>
                <variable formalParameter="OUT">
                  <connectionPointOut><relPosition x="60" y="20" /></connectionPointOut>
                </variable>
              </outputVariables>
            </block>
            <outVariable localId="7" height="20" width="80">
              <position x="440" y="80" />
              <connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="6" formalParameter="OUT" ><position x="0" y="0" /><position x="0" y="0" /></connection></connectionPointIn>
              <expression>Run</expression>
            </outVariable>
          </FBD>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="drive" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## g_batch_mixer

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(mixer && lid_open)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_batch_mixer_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_batch_mixer_clean" pouType="program">
    <interface><inputVars><variable name="mix_cmd"><type><BOOL /></type></variable><variable name="lid_open"><type><BOOL /></type></variable><variable name="enable"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="mixer"><type><BOOL /></type></variable><variable name="alarm"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>lid_open</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>mix_cmd</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>enable</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>mixer</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>lid_open</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>alarm</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_batch_mixer_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_batch_reactor

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(feed_valve && overpressure)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_batch_reactor_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_batch_reactor_clean" pouType="program">
    <interface><inputVars><variable name="feed_cmd"><type><BOOL /></type></variable><variable name="overpressure"><type><BOOL /></type></variable><variable name="enable"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="feed_valve"><type><BOOL /></type></variable><variable name="vent"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>overpressure</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>feed_cmd</variable></contact><contact localId="5" negated="false" storage="none" edge="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>enable</variable></contact><coil localId="6" negated="false" storage="none"><position x="80" y="10" /><connectionPointIn><connection refLocalId="5" /></connectionPointIn><connectionPointOut /><variable>feed_valve</variable></coil><contact localId="7" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>overpressure</variable></contact><coil localId="8" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>vent</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_batch_reactor_clean" /></task></resource></configuration></configurations></instances>
</project>
```

## g_building_lighting

- Language: LD-graphical
- File: clean.xml
- Properties:
- P1 (invariant): !(lights && master_off)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-07-09T00:00:00" />
  <contentHeader name="g_building_lighting_clean"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="g_building_lighting_clean" pouType="program">
      <interface><inputVars><variable name="demand"><type><BOOL /></type></variable><variable name="master_off"><type><BOOL /></type></variable><variable name="maint"><type><BOOL /></type></variable></inputVars><outputVars><variable name="lights"><type><BOOL /></type></variable><variable name="setback"><type><BOOL /></type></variable></outputVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <contact localId="3" negated="true" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>master_off</variable></contact><contact localId="4" negated="false" storage="none" edge="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>demand</variable></contact><coil localId="5" negated="false" storage="none"><position x="60" y="10" /><connectionPointIn><connection refLocalId="4" /></connectionPointIn><connectionPointOut /><variable>lights</variable></coil><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="30" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>master_off</variable></contact><coil localId="7" negated="false" storage="none"><position x="40" y="30" /><connectionPointIn><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>setback</variable></coil>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0">
    <task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_building_lighting_clean" /></task>
  </resource></configuration></configurations></instances>
</project>
```

## g_burner_purge

- Language: LD-graphical
- File: program.xml
- Properties:
- P1 (invariant): !MainValve || (PurgeDone && FlameProven)

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_burner_purge"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="g_burner_purge" pouType="program">
    <interface><inputVars><variable name="CallForHeat"><type><BOOL /></type></variable><variable name="PurgeDone"><type><BOOL /></type></variable><variable name="FlameProven"><type><BOOL /></type></variable><variable name="FlameFail"><type><BOOL /></type></variable><variable name="ResetBtn"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Fan"><type><BOOL /></type></variable><variable name="Lockout"><type><BOOL /></type></variable><variable name="Pilot"><type><BOOL /></type></variable><variable name="MainValve"><type><BOOL /></type></variable></outputVars></interface>
    <body><LD>
      <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
      <contact localId="3" negated="false" storage="none" edge="none"><position x="20" y="10" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><coil localId="4" negated="false" storage="none"><position x="40" y="10" /><connectionPointIn><connection refLocalId="3" /></connectionPointIn><connectionPointOut /><variable>Fan</variable></coil><contact localId="5" negated="false" storage="none" edge="none"><position x="20" y="40" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><contact localId="6" negated="false" storage="none" edge="none"><position x="20" y="50" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>FlameFail</variable></contact><contact localId="7" negated="true" storage="none" edge="none"><position x="40" y="40" /><connectionPointIn><connection refLocalId="5" /><connection refLocalId="6" /></connectionPointIn><connectionPointOut /><variable>ResetBtn</variable></contact><coil localId="8" negated="false" storage="none"><position x="60" y="40" /><connectionPointIn><connection refLocalId="7" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></coil><contact localId="9" negated="false" storage="none" edge="none"><position x="20" y="80" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><contact localId="10" negated="false" storage="none" edge="none"><position x="40" y="80" /><connectionPointIn><connection refLocalId="9" /></connectionPointIn><connectionPointOut /><variable>PurgeDone</variable></contact><contact localId="11" negated="true" storage="none" edge="none"><position x="60" y="80" /><connectionPointIn><connection refLocalId="10" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><coil localId="12" negated="false" storage="none"><position x="80" y="80" /><connectionPointIn><connection refLocalId="11" /></connectionPointIn><connectionPointOut /><variable>Pilot</variable></coil><contact localId="13" negated="false" storage="none" edge="none"><position x="20" y="110" /><connectionPointIn><connection refLocalId="0" /></connectionPointIn><connectionPointOut /><variable>CallForHeat</variable></contact><contact localId="14" negated="false" storage="none" edge="none"><position x="40" y="110" /><connectionPointIn><connection refLocalId="13" /></connectionPointIn><connectionPointOut /><variable>PurgeDone</variable></contact><contact localId="15" negated="false" storage="none" edge="none"><position x="60" y="110" /><connectionPointIn><connection refLocalId="14" /></connectionPointIn><connectionPointOut /><variable>FlameProven</variable></contact><contact localId="16" negated="true" storage="none" edge="none"><position x="80" y="110" /><connectionPointIn><connection refLocalId="15" /></connectionPointIn><connectionPointOut /><variable>Lockout</variable></contact><coil localId="17" negated="false" storage="none"><position x="100" y="110" /><connectionPointIn><connection refLocalId="16" /></connectionPointIn><connectionPointOut /><variable>MainValve</variable></coil>
      <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
    </LD></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_burner_purge" /></task></resource></configuration></configurations></instances>
</project>
```
