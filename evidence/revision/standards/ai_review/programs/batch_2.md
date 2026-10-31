# Batch 2: g_two_hand_fb, st_burner_purge, st_door_reversal, st_estop_reset, st_guard_lock, st_two_hand

## g_two_hand_fb

- Language: LD-graphical
- Clause cited by the descriptor: The ISO 13851 Type II logic of g_two_hand moved into a reusable function block, the shape certified safety libraries ship it in
- Safety intent: The ram must descend only while both hand actuators are held; releasing either one must stop the stroke.
- Property (checked and holds): P1: !Stroke || (LH && RH)  (ISO 13851 requires the ram to descend only while both actuators are held. Releasing either one stops the stroke.)
- Discriminator `tiedown_check.props.yaml` (not a requirement; it separates a compliant program from a non-compliant one): P1: !(LH && RH) || Stroke  (Both actuators held always produces a stroke. A Type II device with anti-tie-down must refute this.); on this program it is VIOLATION

Program `program.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <fileHeader companyName="Anonymous" productName="Benchmark Suite" productVersion="1.0" creationDateTime="2026-08-28T00:00:00" />
  <contentHeader name="g_two_hand_fb"><coordinateInfo><fbd><scaling x="1" y="1" /></fbd><ld><scaling x="1" y="1" /></ld><sfc><scaling x="1" y="1" /></sfc></coordinateInfo></contentHeader>
  <types><dataTypes /><pous>
    <pou name="TwoHandII" pouType="functionBlock">
      <interface>
        <inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars>
        <outputVars><variable name="Stroke"><type><BOOL /></type></variable></outputVars>
        <localVars><variable name="BothOff"><type><BOOL /></type></variable><variable name="Armed"><type><BOOL /></type></variable></localVars>
      </interface>
      <body><ST><xhtml:p><![CDATA[BothOff := NOT LH AND NOT RH;
Armed := (Armed OR BothOff) AND NOT Stroke;
Stroke := (Stroke OR Armed) AND LH AND RH;
]]></xhtml:p></ST></body>
    </pou>
    <pou name="g_two_hand_fb" pouType="program">
      <interface><inputVars><variable name="LH"><type><BOOL /></type></variable><variable name="RH"><type><BOOL /></type></variable></inputVars><outputVars><variable name="Stroke"><type><BOOL /></type></variable></outputVars><localVars><variable name="THC0"><type><derived name="TwoHandII" /></type></variable></localVars></interface>
      <body><LD>
        <leftPowerRail localId="0"><position x="0" y="0" /><connectionPointOut formalParameter="none" /></leftPowerRail>
        <inVariable localId="3" height="20" width="60"><position x="20" y="30" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>LH</expression></inVariable>
        <inVariable localId="4" height="20" width="60"><position x="20" y="60" /><connectionPointOut><relPosition x="60" y="10" /></connectionPointOut><expression>RH</expression></inVariable>
        <block localId="5" width="120" height="80" typeName="TwoHandII" instanceName="THC0">
          <position x="100" y="10" />
          <inputVariables>
            <variable formalParameter="EN"><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="0" /></connectionPointIn></variable>
            <variable formalParameter="LH"><connectionPointIn><relPosition x="0" y="40" /><connection refLocalId="3" /></connectionPointIn></variable>
            <variable formalParameter="RH"><connectionPointIn><relPosition x="0" y="70" /><connection refLocalId="4" /></connectionPointIn></variable>
          </inputVariables>
          <inOutVariables />
          <outputVariables>
            <variable formalParameter="ENO"><connectionPointOut><relPosition x="120" y="10" /></connectionPointOut></variable>
            <variable formalParameter="Stroke"><connectionPointOut><relPosition x="120" y="40" /></connectionPointOut></variable>
          </outputVariables>
        </block>
        <outVariable localId="6" height="20" width="60" negated="false"><position x="260" y="40" /><connectionPointIn><relPosition x="0" y="10" /><connection refLocalId="5" formalParameter="Stroke"><position x="220" y="50" /></connection></connectionPointIn><expression>Stroke</expression></outVariable>
        <rightPowerRail localId="2147483646"><position x="400" y="0" /><connectionPointIn /></rightPowerRail>
      </LD></body>
    </pou>
  </pous></types>
  <instances><configurations><configuration name="Config0"><resource name="Res0"><task name="tcyclic" interval="T#10ms" priority="0"><pouInstance name="inst0" typeName="g_two_hand_fb" /></task></resource></configuration></configurations></instances>
</project>
```

The same program as Boolean equations, read mechanically from the XML (`:=` assigns; coils are evaluated in the order listed; `[set]` and `[reset]` are latching coils):

```

```

Mutants that no property kills (6):

- S1: ST body: AND -> OR in: BothOff := NOT LH AND NOT RH;
- S2: ST body: OR -> AND in: Armed := (Armed OR BothOff) AND NOT Stroke;
- S3: ST body: OR -> AND in: Stroke := (Stroke OR Armed) AND LH AND RH;
- S4: ST body: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
- S5: ST body: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
- S6: ST body: NOT -> (removed) in: Armed := (Armed OR BothOff) AND NOT Stroke;

## st_burner_purge

- Language: ST
- Clause cited by the descriptor: Structured Text rendering of g_burner_purge, for cross-language comparison of the same machine
- Safety intent: 
- Property (checked and holds): P1: !MainValve || (PurgeDone && FlameProven)  (EN 298 light-off order: the main gas valve opens only after the purge has completed and the flame is proven.)

Program `burner_purge.st`:

```iecst
(* burner_purge: purge, light-off and lockout for a gas burner.
   Structured Text rendering of g_burner_purge.

   EN 298 fixes the order: fan first, main gas only after the purge has completed
   and the flame is proven. The lockout latches on a flame fault and needs the
   reset button, because a burner that retries on its own fills the chamber. *)
PROGRAM burner
  VAR_INPUT
    CallForHeat : BOOL;
    PurgeDone   : BOOL;
    FlameProven : BOOL;
    FlameFail   : BOOL;
    ResetBtn    : BOOL;
  END_VAR
  VAR_OUTPUT
    Fan       : BOOL;
    Lockout   : BOOL;
    Pilot     : BOOL;
    MainValve : BOOL;
  END_VAR

  Fan := CallForHeat;
  Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
  Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
  MainValve := CallForHeat AND PurgeDone AND FlameProven AND NOT Lockout;
END_PROGRAM
```

Mutants that no property kills (7):

- S1: AND -> OR in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
- S2: AND -> OR in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
- S3: AND -> OR in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
- S4: OR -> AND in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
- S5: NOT -> (removed) in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
- S6: NOT -> (removed) in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
- S7: NOT -> (removed) in: MainValve := CallForHeat AND PurgeDone AND FlameProven AND NOT Lockout;

## st_door_reversal

- Language: ST
- Clause cited by the descriptor: Structured Text rendering of g_door_reversal, for cross-language comparison of the same machine
- Safety intent: 
- Property (checked and holds): P1: !(MoveDown && Beam)  (The door never drives down while the photo-eye beam is broken.)

Program `door_reversal.st`:

```iecst
(* door_reversal: sectional door with photo-eye reversal.
   Structured Text rendering of g_door_reversal.

   EN 13241 asks for a reversal, not a pause. Reversing latches when the beam
   breaks and holds until the top limit, so clearing the obstruction does not
   put the door back into its closing stroke. *)
PROGRAM door
  VAR_INPUT
    CloseCmd : BOOL;
    OpenCmd  : BOOL;
    Beam     : BOOL;
    TopLimit : BOOL;
  END_VAR
  VAR_OUTPUT
    Reversing : BOOL;
    MoveDown  : BOOL;
    MoveUp    : BOOL;
  END_VAR

  Reversing := (Reversing OR Beam) AND NOT TopLimit;
  MoveDown := CloseCmd AND NOT Beam AND NOT Reversing;
  MoveUp := OpenCmd OR Reversing;
END_PROGRAM
```

Mutants that no property kills (5):

- S1: AND -> OR in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
- S2: OR -> AND in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
- S3: OR -> AND in: MoveUp := OpenCmd OR Reversing;
- S4: NOT -> (removed) in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
- S5: NOT -> (removed) in: MoveDown := CloseCmd AND NOT Beam AND NOT Reversing;

## st_estop_reset

- Language: ST
- Clause cited by the descriptor: Structured Text rendering of g_estop_reset, for cross-language comparison of the same safety function
- Safety intent: 
- Property (checked and holds): P1: !(Run && EStop)  (ISO 13850 stop function: the drive is never energised while the emergency stop is actuated.)

Program `estop_reset.st`:

```iecst
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

Mutants that no property kills (8):

- S1: AND -> OR in: ResetEdge := Reset_prev AND NOT Reset;
- S2: AND -> OR in: Safe := (Safe OR ResetEdge) AND NOT EStop;
- S3: AND -> OR in: Run := Safe AND Start AND NOT EStop;
- S4: AND -> OR in: Run := Safe AND Start AND NOT EStop;
- S5: OR -> AND in: Safe := (Safe OR ResetEdge) AND NOT EStop;
- S6: NOT -> (removed) in: ResetEdge := Reset_prev AND NOT Reset;
- S7: NOT -> (removed) in: Safe := (Safe OR ResetEdge) AND NOT EStop;
- S8: NOT -> (removed) in: Run := Safe AND Start AND NOT EStop;

## st_guard_lock

- Language: ST
- Clause cited by the descriptor: Structured Text rendering of g_guard_lock, for cross-language comparison of the same safety function
- Safety intent: 
- Property (checked and holds): P1: !(Unlocked && Motor)  (ISO 14119 guard locking: the guard is never released while the drive is energised.)

Program `guard_lock.st`:

```iecst
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

Mutants that no property kills (1):

- S1: NOT -> (removed) in: Rundown(IN := NOT Motor, PT := T#30ms);

## st_two_hand

- Language: ST
- Clause cited by the descriptor: Structured Text rendering of g_two_hand, for cross-language comparison of the same machine
- Safety intent: 
- Property (checked and holds): P1: !Stroke || (LH && RH)  (ISO 13851 requires the ram to descend only while both actuators are held. Releasing either one stops the stroke.)

Program `two_hand.st`:

```iecst
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

Mutants that no property kills (7):

- S1: AND -> OR in: BothOff := NOT LH AND NOT RH;
- S2: AND -> OR in: Armed := (Armed OR BothOff) AND NOT Stroke;
- S3: OR -> AND in: Armed := (Armed OR BothOff) AND NOT Stroke;
- S4: OR -> AND in: Stroke := (Stroke OR Armed) AND LH AND RH;
- S5: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
- S6: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
- S7: NOT -> (removed) in: Armed := (Armed OR BothOff) AND NOT Stroke;
