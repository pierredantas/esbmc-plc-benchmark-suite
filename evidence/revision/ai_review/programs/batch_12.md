# Batch 12: benchmarks protection_lockout_cascade, purge_fault_lockout, reactor_pressure_lockout, reject_gate_triple_output, sensor_forge, sfc_batch_fill_drain, sfc_counter_reset, sfc_elevator_door

## protection_lockout_cascade

- Language: LD-textual
- File: clean.ld
- Properties:
- P1 (invariant): protection_trip -> !breaker_close
- P2 (reachability): protection_trip && breaker_close

```text
// Protection trip cascading into lockout latch – clean
OTE(trip_latch) := XIC(protection_trip) + (XIC(trip_latch) * XIO(local_reset)) ;
OTE(lockout_latch) := XIC(trip_latch) + (XIC(lockout_latch) * XIO(supervisor_reset)) ;
OTE(breaker_close) := XIC(close_req) * XIO(lockout_latch) ;
```

## purge_fault_lockout

- Language: LD-textual
- File: clean.ld
- Properties:
- P1 (invariant): purge_fail -> !burner_enable
- P2 (reachability): purge_fail && burner_enable

```text
// Burner purge fault lockout – clean
OTE(fault_latch) := XIC(purge_fail) + (XIC(fault_latch) * XIO(manual_reset)) ;
OTE(fault_indicator) := XIC(fault_latch) ;
OTE(burner_enable) := XIC(burner_req) * XIO(fault_latch) ;
```

## reactor_pressure_lockout

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(feed_pump && pressure_high)
- P2 (invariant): !(feed_pump && fault_flag)
- P3 (reachability): feed_pump && fault_flag

```iecst
(* ============================================================
   Chemical reactor overpressure lockout.
   Safety intent: the feed pump must never run while reactor
   pressure is above the safe limit. If pressure ever exceeds the
   safe limit, the reactor is considered faulted and the feed
   pump remains shut down, even after pressure falls back into
   range, until an operator manually clears the fault.
   ============================================================ *)
PROGRAM reactor_control
  VAR
    pressure_high  AT %IX0.0 : BOOL;
    clear_fault    AT %IX0.1 : BOOL;
    feed_request   AT %IX0.2 : BOOL;
    feed_pump        AT %QX0.0 : BOOL;
    fault_flag : BOOL := FALSE;
  END_VAR

  IF pressure_high THEN
    fault_flag := TRUE;
  ELSIF clear_fault THEN
    fault_flag := FALSE;
  END_IF;

  IF fault_flag OR pressure_high THEN
    feed_pump := FALSE;
  ELSIF feed_request THEN
    feed_pump := TRUE;
  ELSE
    feed_pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : reactor_control;
  END_RESOURCE
END_CONFIGURATION
```

## reject_gate_triple_output

- Language: LD-textual
- File: clean.ld
- Properties:
- P1 (invariant): defect_detect -> gate_actuate
- P2 (reachability): defect_detect && !gate_actuate

```text
// Reject gate fault latch with three independent readouts – clean
OTE(reject_latch) := XIC(defect_detect) + (XIC(reject_latch) * XIO(op_reset)) ;
OTE(gate_actuate) := XIC(reject_latch) ;
OTE(counter_enable) := XIC(reject_latch) * XIC(line_running) ;
OTE(line_stop) := XIC(reject_latch) * XIO(bypass_key) ;
```

## sensor_forge

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): reported_open == valve_open
- P2 (reachability): reported_open && !valve_open

```iecst
(* ============================================================
   S3 - Pressure relief with HMI reporting : CLEAN baseline
   A relief valve opens on over-pressure; the value reported to
   the HMI/SCADA must always equal the real valve command
   (no spoofing). Safety/integrity invariant:
        reported_open  ==  valve_open
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM relief
  VAR
    over_press AT %IX0.0 : BOOL;   (* pressure switch *)
    valve_open    AT %QX0.0 : BOOL; (* real actuator command  *)
    reported_open AT %QX0.1 : BOOL; (* value sent to the HMI  *)
  END_VAR

  IF over_press THEN
    valve_open := TRUE;
  ELSE
    valve_open := FALSE;
  END_IF;

  (* Honest reporting: HMI mirrors the real command *)
  reported_open := valve_open;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : relief;
  END_RESOURCE
END_CONFIGURATION
```

## sfc_batch_fill_drain

- Language: SFC
- File: clean.xml
- Properties:
- P1 (mutual_exclusion): ['fill_valve', 'drain_valve']

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Batch vessel cycle: Idle -> Filling -> Reacting -> Draining -> Idle.
     fill_valve is held while Filling, drain_valve while Draining.
     Opening both at once dumps unreacted feed straight to the effluent
     line, which is a loss of containment rather than a lost batch. -->
<project xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="sfc_batch_fill_drain_clean">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="batch_cycle" pouType="program">
        <interface>
          <inputVars>
            <variable name="start"><type><BOOL /></type></variable>
            <variable name="level_high"><type><BOOL /></type></variable>
            <variable name="reaction_done"><type><BOOL /></type></variable>
            <variable name="level_low"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="fill_valve"><type><BOOL /></type></variable>
            <variable name="drain_valve"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <SFC>
            <step localId="1" name="Idle" initialStep="true">
              <position x="200" y="20" />
              <connectionPointIn><relPosition x="40" y="0" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
            </step>
            <transition localId="2">
              <position x="200" y="80" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="1" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[start]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="3" name="Filling">
              <position x="200" y="120" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="2" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
              <connectionPointOutAction formalParameter="none"><relPosition x="80" y="20" /></connectionPointOutAction>
            </step>
            <actionBlock localId="4">
              <position x="300" y="120" />
              <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn>
              <action localId="40" qualifier="N"><relPosition x="0" y="0" /><reference name="fill_valve" /></action>
            </actionBlock>
            <transition localId="5">
              <position x="200" y="180" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="3" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[level_high]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="6" name="Reacting">
              <position x="200" y="220" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="5" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
            </step>
            <transition localId="7">
              <position x="200" y="280" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="6" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[reaction_done]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="8" name="Draining">
              <position x="200" y="320" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="7" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
              <connectionPointOutAction formalParameter="none"><relPosition x="80" y="20" /></connectionPointOutAction>
            </step>
            <actionBlock localId="9">
              <position x="300" y="320" />
              <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="8" /></connectionPointIn>
              <action localId="90" qualifier="N"><relPosition x="0" y="0" /><reference name="drain_valve" /></action>
            </actionBlock>
            <transition localId="10">
              <position x="200" y="380" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="8" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[level_low]]></xhtml:p></ST></inline></condition>
            </transition>
            <jumpStep localId="11" targetName="Idle">
              <position x="200" y="420" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="10" /></connectionPointIn>
            </jumpStep>
          </SFC>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="batch_cycle" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```

## sfc_counter_reset

- Language: SFC
- File: program.xml
- Properties:
- P1 (invariant): !Reset || (OUT == ResetCounterValue)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- counter_reset: a free-running counter with a reset-to-value.
   Reset loads ResetCounterValue, otherwise Cnt increments; OUT follows Cnt.
   Imported from the Beremiz IEC 61131-3 language test (CounterSFC function block),
   re-expressed as a PROGRAM so it stands alone. See benchmark.yml for provenance. -->
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-29T00:00:00" />
  <contentHeader name="sfc_counter_reset"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous><pou name="drive" pouType="program">
    <interface>
      <inputVars>
        <variable name="Reset"><type><BOOL /></type></variable>
        <variable name="ResetCounterValue"><type><INT /></type></variable>
      </inputVars>
      <outputVars><variable name="OUT"><type><INT /></type></variable></outputVars>
      <localVars><variable name="Cnt"><type><INT /></type></variable></localVars>
    </interface>
    <body><SFC xmlns:html="http://www.w3.org/1999/xhtml">
            <step localId="1" name="Start" initialStep="true" height="34" width="90">
              <position x="241" y="14" />
              <connectionPointOut formalParameter="">
                <relPosition x="45" y="34" />
              </connectionPointOut>
            </step>
            <selectionDivergence localId="2" height="1" width="431">
              <position x="70" y="86" />
              <connectionPointIn>
                <relPosition x="216" y="0" />
                <connection refLocalId="1">
                  <position x="286" y="86" />
                  <position x="286" y="42" />
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="0" y="1" />
              </connectionPointOut>
              <connectionPointOut formalParameter="">
                <relPosition x="431" y="1" />
              </connectionPointOut>
            </selectionDivergence>
            <transition localId="3" height="2" width="20">
              <position x="491" y="132" />
              <connectionPointIn>
                <relPosition x="10" y="0" />
                <connection refLocalId="2">
                  <position x="501" y="132" />
                  <position x="501" y="87" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2" />
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <html:p>Reset</html:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <transition localId="4" height="2" width="20" executionOrderId="0">
              <position x="60" y="135" />
              <connectionPointIn>
                <relPosition x="10" y="0" />
                <connection refLocalId="2">
                  <position x="70" y="135" />
                  <position x="70" y="87" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2" />
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <html:p>NOT Reset</html:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <step localId="5" name="ResetCounter" initialStep="false" height="30" width="134">
              <position x="434" y="190" />
              <connectionPointIn>
                <relPosition x="67" y="0" />
                <connection refLocalId="3">
                  <position x="501" y="190" />
                  <position x="501" y="134" />
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="67" y="30" />
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="134" y="15" />
              </connectionPointOutAction>
            </step>
            <actionBlock localId="6" height="63" width="254">
              <position x="641" y="190" />
              <connectionPointIn>
                <relPosition x="0" y="15" />
                <connection refLocalId="5">
                  <position x="641" y="205" />
                  <position x="568" y="205" />
                </connection>
              </connectionPointIn>
              <action localId="0">
                <relPosition x="0" y="0" />
                <inline>
                  <ST>
                    <html:p>Cnt := ResetCounterValue;</html:p>
                  </ST>
                </inline>
              </action>
              <action localId="0">
                <relPosition x="0" y="0" />
                <inline>
                  <ST>
                    <html:p>OUT := Cnt;</html:p>
                  </ST>
                </inline>
              </action>
            </actionBlock>
            <step localId="7" name="Count" initialStep="false" height="30" width="85" executionOrderId="0">
              <position x="28" y="191" />
              <connectionPointIn>
                <relPosition x="42" y="0" />
                <connection refLocalId="4">
                  <position x="70" y="191" />
                  <position x="70" y="137" />
                </connection>
              </connectionPointIn>
              <connectionPointOut formalParameter="">
                <relPosition x="42" y="30" />
              </connectionPointOut>
              <connectionPointOutAction formalParameter="">
                <relPosition x="85" y="15" />
              </connectionPointOutAction>
            </step>
            <actionBlock localId="8" height="52" width="164" executionOrderId="0">
              <position x="154" y="191" />
              <connectionPointIn>
                <relPosition x="0" y="15" />
                <connection refLocalId="7">
                  <position x="154" y="206" />
                  <position x="113" y="206" />
                </connection>
              </connectionPointIn>
              <action localId="0">
                <relPosition x="0" y="0" />
                <inline>
                  <ST>
                    <html:p>Cnt := Cnt + 1;</html:p>
                  </ST>
                </inline>
              </action>
              <action localId="0">
                <relPosition x="0" y="0" />
                <inline>
                  <ST>
                    <html:p>OUT := Cnt;</html:p>
                  </ST>
                </inline>
              </action>
            </actionBlock>
            <selectionConvergence localId="10" height="1" width="431">
              <position x="70" y="273" />
              <connectionPointIn>
                <relPosition x="0" y="0" />
                <connection refLocalId="13">
                  <position x="70" y="273" />
                  <position x="70" y="244" />
                </connection>
              </connectionPointIn>
              <connectionPointIn>
                <relPosition x="431" y="0" />
                <connection refLocalId="14">
                  <position x="501" y="273" />
                  <position x="501" y="250" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="216" y="1" />
              </connectionPointOut>
            </selectionConvergence>
            <jumpStep localId="12" targetName="Start" height="13" width="12">
              <position x="280" y="317" />
              <connectionPointIn>
                <relPosition x="6" y="0" />
                <connection refLocalId="10">
                  <position x="286" y="317" />
                  <position x="286" y="274" />
                </connection>
              </connectionPointIn>
            </jumpStep>
            <transition localId="13" height="2" width="20" executionOrderId="0">
              <position x="60" y="242" />
              <connectionPointIn>
                <relPosition x="10" y="0" />
                <connection refLocalId="7">
                  <position x="70" y="242" />
                  <position x="70" y="215" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2" />
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <html:p>Reset</html:p>
                  </ST>
                </inline>
              </condition>
            </transition>
            <transition localId="14" height="2" width="20" executionOrderId="0">
              <position x="491" y="248" />
              <connectionPointIn>
                <relPosition x="10" y="0" />
                <connection refLocalId="5">
                  <position x="501" y="248" />
                  <position x="501" y="220" />
                </connection>
              </connectionPointIn>
              <connectionPointOut>
                <relPosition x="10" y="2" />
              </connectionPointOut>
              <condition>
                <inline name="">
                  <ST>
                    <html:p>NOT Reset</html:p>
                  </ST>
                </inline>
              </condition>
            </transition>
          </SFC></body>
  </pou></pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="drive" /></task></resource></configuration></configurations></instances>
</project>
```

## sfc_elevator_door

- Language: SFC
- File: clean.xml
- Properties:
- P1 (invariant): !(moving && door_open)

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Elevator car door cycle: Idle -> Opening -> Closing -> Travelling -> Idle.
     door_open is held while Opening, moving while Travelling.
     A car that travels with the door open exposes the open shaft to
     anyone standing in the doorway. -->
<project xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns="http://www.plcopen.org/xml/tc6_0200">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-26T00:00:00" />
  <contentHeader name="sfc_elevator_door_clean">
    <coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo>
  </contentHeader>
  <types>
    <dataTypes />
    <pous>
      <pou name="car_control" pouType="program">
        <interface>
          <inputVars>
            <variable name="call"><type><BOOL /></type></variable>
            <variable name="dwell_done"><type><BOOL /></type></variable>
            <variable name="door_closed"><type><BOOL /></type></variable>
            <variable name="at_floor"><type><BOOL /></type></variable>
          </inputVars>
          <outputVars>
            <variable name="door_open"><type><BOOL /></type></variable>
            <variable name="moving"><type><BOOL /></type></variable>
          </outputVars>
        </interface>
        <body>
          <SFC>
            <step localId="1" name="Idle" initialStep="true">
              <position x="200" y="20" />
              <connectionPointIn><relPosition x="40" y="0" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
            </step>
            <transition localId="2">
              <position x="200" y="80" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="1" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[call]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="3" name="Opening">
              <position x="200" y="120" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="2" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
              <connectionPointOutAction formalParameter="none"><relPosition x="80" y="20" /></connectionPointOutAction>
            </step>
            <actionBlock localId="4">
              <position x="300" y="120" />
              <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="3" /></connectionPointIn>
              <action localId="40" qualifier="N"><relPosition x="0" y="0" /><reference name="door_open" /></action>
            </actionBlock>
            <transition localId="5">
              <position x="200" y="180" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="3" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[dwell_done]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="6" name="Closing">
              <position x="200" y="220" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="5" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
            </step>
            <transition localId="7">
              <position x="200" y="280" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="6" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[door_closed]]></xhtml:p></ST></inline></condition>
            </transition>
            <step localId="8" name="Travelling">
              <position x="200" y="320" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="7" /></connectionPointIn>
              <connectionPointOut formalParameter="none"><relPosition x="40" y="40" /></connectionPointOut>
              <connectionPointOutAction formalParameter="none"><relPosition x="80" y="20" /></connectionPointOutAction>
            </step>
            <actionBlock localId="9">
              <position x="300" y="320" />
              <connectionPointIn><relPosition x="0" y="20" /><connection refLocalId="8" /></connectionPointIn>
              <action localId="90" qualifier="N"><relPosition x="0" y="0" /><reference name="moving" /></action>
            </actionBlock>
            <transition localId="10">
              <position x="200" y="380" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="8" /></connectionPointIn>
              <connectionPointOut><relPosition x="40" y="10" /></connectionPointOut>
              <condition><inline name="cond"><ST><xhtml:p><![CDATA[at_floor]]></xhtml:p></ST></inline></condition>
            </transition>
            <jumpStep localId="11" targetName="Idle">
              <position x="200" y="420" />
              <connectionPointIn><relPosition x="40" y="0" /><connection refLocalId="10" /></connectionPointIn>
            </jumpStep>
          </SFC>
        </body>
      </pou>
    </pous>
  </types>
  <instances>
    <configurations>
      <configuration name="Config0">
        <resource name="Res0">
          <task name="tcyclic" interval="T#10ms" priority="0">
            <pouInstance name="inst0" typeName="car_control" />
          </task>
        </resource>
      </configuration>
    </configurations>
  </instances>
</project>
```
