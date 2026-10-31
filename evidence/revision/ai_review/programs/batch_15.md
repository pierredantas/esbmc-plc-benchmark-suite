# Batch 15: benchmarks st_swat_timer1, st_three_pump_lockout, st_two_hand, tank_overflow, welder_gas_shield_interlock

## st_swat_timer1

- Language: ST
- File: sleg_timer1_0.st
- Properties:
- P1 (termination): None

```iecst
FUNCTION_BLOCK check_pumps
  VAR_INPUT
    IN1 : DINT;
    IN2 : DINT;
  END_VAR
  VAR_OUTPUT
    OUT : BOOL;
  END_VAR

  if IN1 < IN2 then
    OUT:=TRUE;
  end_if;
  if IN1 >= IN2 then
    OUT:= FALSE;
  end_if;

END_FUNCTION_BLOCK

PROGRAM PLC1
  VAR_INPUT
    level : DINT;
    request : DINT;
  END_VAR
  VAR_OUTPUT
    pumps_state : BOOL;
    pumps : BOOL;
    valve : BOOL;
  END_VAR
  VAR
    low : BOOL;
    high : BOOL;
    open_req : BOOL;
    close_req : BOOL;
    low_1 : DINT := 40;
    high_1 : DINT := 80;
    check_pumps0 : check_pumps;
    TON0 : TON;
    _TMP_LE3_ENO : BOOL;
    _TMP_LE3_OUT : BOOL;
    _TMP_GE7_ENO : BOOL;
    _TMP_GE7_OUT : BOOL;
    _TMP_EQ23_ENO : BOOL;
    _TMP_EQ23_OUT : BOOL;
    _TMP_EQ24_ENO : BOOL;
    _TMP_EQ24_OUT : BOOL;
  END_VAR

  TON0(IN := TRUE, PT := T#10000s);
  check_pumps0(EN := TON0.Q, IN1 := level, IN2 := high_1);
  IF check_pumps0.ENO THEN
      pumps_state := check_pumps0.OUT;
  END_IF;
  _TMP_LE3_OUT := LE(EN := TRUE, IN1 := level, IN2 := low_1, ENO => _TMP_LE3_ENO);
  low := _TMP_LE3_OUT;
  _TMP_GE7_OUT := GE(EN := TRUE, IN1 := level, IN2 := high_1, ENO => _TMP_GE7_ENO);
  high := _TMP_GE7_OUT;
  _TMP_EQ23_OUT := EQ(EN := TRUE, IN1 := request, IN2 := 1, ENO => _TMP_EQ23_ENO);
  open_req := _TMP_EQ23_OUT;
  _TMP_EQ24_OUT := EQ(EN := TRUE, IN1 := request, IN2 := 0, ENO => _TMP_EQ24_ENO);
  close_req := _TMP_EQ24_OUT;
  pumps := NOT(high) AND (low OR pumps);
  valve := NOT(close_req) AND (open_req AND NOT(low) OR valve);
END_PROGRAM

PROGRAM PLC3
  VAR_INPUT
    level : DINT;
  END_VAR
  VAR_OUTPUT
    pump : BOOL;
  END_VAR
  VAR
    low : BOOL;
    high : BOOL;
    low_3 : DINT := 0;
    high_3 : DINT := 10;
    _TMP_LE13_ENO : BOOL;
    _TMP_LE13_OUT : BOOL;
    _TMP_GE12_ENO : BOOL;
    _TMP_GE12_OUT : BOOL;
  END_VAR

  _TMP_LE13_OUT := LE(EN := TRUE, IN1 := level, IN2 := low_3, ENO => _TMP_LE13_ENO);
  low := _TMP_LE13_OUT;
  _TMP_GE12_OUT := GE(EN := TRUE, IN1 := level, IN2 := high_3, ENO => _TMP_GE12_ENO);
  high := _TMP_GE12_OUT;
  pump := NOT(low) AND (high OR pump);
END_PROGRAM

PROGRAM PLC2
  VAR_INPUT
    level : DINT;
  END_VAR
  VAR_OUTPUT
    request : BOOL;
  END_VAR
  VAR
    open_req : BOOL;
    close_req : BOOL;
    low_2 : DINT := 10;
    high_2 : DINT := 20;
    _TMP_LE10_ENO : BOOL;
    _TMP_LE10_OUT : BOOL;
    _TMP_GE11_ENO : BOOL;
    _TMP_GE11_OUT : BOOL;
  END_VAR

  _TMP_LE10_OUT := LE(EN := TRUE, IN1 := level, IN2 := low_2, ENO => _TMP_LE10_ENO);
  open_req := _TMP_LE10_OUT;
  _TMP_GE11_OUT := GE(EN := TRUE, IN1 := level, IN2 := high_2, ENO => _TMP_GE11_ENO);
  close_req := _TMP_GE11_OUT;
  request := NOT(close_req) AND (open_req OR request);
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    TASK task1(INTERVAL := T#20ms,PRIORITY := 0);
    TASK task2(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : PLC1;
    PROGRAM instance1 WITH task1 : PLC2;
    PROGRAM instance2 WITH task2 : PLC3;
  END_RESOURCE
END_CONFIGURATION
```

## st_three_pump_lockout

- Language: ST
- File: clean.st
- Properties:
- P1 (mutual_exclusion): ['pump_a', 'pump_b', 'pump_c']
- P2 (reachability): pump_a && pump_b

```iecst
(* ============================================================
   Three-pump station lockout : CLEAN baseline
   Safety: at most one of pump_a, pump_b, pump_c may run at a
   time (shared discharge header cannot take combined flow).
   Expected verdict: SAFE.
   ============================================================ *)
PROGRAM three_pump
  VAR
    req_a AT %IX0.0 : BOOL;
    req_b AT %IX0.1 : BOOL;
    req_c AT %IX0.2 : BOOL;
    pump_a AT %QX0.0 : BOOL;
    pump_b AT %QX0.1 : BOOL;
    pump_c AT %QX0.2 : BOOL;
  END_VAR

  IF req_a THEN
    pump_a := TRUE;
    pump_b := FALSE;
    pump_c := FALSE;
  ELSIF req_b THEN
    pump_a := FALSE;
    pump_b := TRUE;
    pump_c := FALSE;
  ELSIF req_c THEN
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := TRUE;
  ELSE
    pump_a := FALSE;
    pump_b := FALSE;
    pump_c := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : three_pump;
  END_RESOURCE
END_CONFIGURATION
```

## st_two_hand

- Language: ST
- File: two_hand.st
- Properties:
- P1 (invariant): !Stroke || (LH && RH)

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

## tank_overflow

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !(pump && level_high)
- P2 (reachability): pump && level_high

```iecst
(* ============================================================
   S1 - Tank level control : CLEAN (benign) baseline
   Domain: water/chemical tank fill with high-level interlock.
   Safety: the pump must never run while the tank is full.
   Govil et al. taxonomy: N/A (this is the benign host program).
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM tank
  VAR
    level_high AT %IX0.0 : BOOL;   (* sensor: tank full          *)
    start      AT %IX0.1 : BOOL;   (* operator: request fill     *)
    pump       AT %QX0.0 : BOOL;   (* actuator: fill pump        *)
  END_VAR

  (* Fill while requested and not yet full *)
  IF start AND NOT level_high THEN
    pump := TRUE;
  END_IF;

  (* Safety interlock: full tank always stops the pump *)
  IF level_high THEN
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

## welder_gas_shield_interlock

- Language: ST
- File: clean.st
- Properties:
- P1 (invariant): !arc_on || (gas_flow_ok && trigger_pull)
- P2 (reachability): arc_on && !gas_flow_ok

```iecst
(* ============================================================
   MIG welder shielding-gas interlock : demo program, not in the
   suite.
   Safety intent: the arc (weld current) must never strike unless
   BOTH the shielding-gas flow is confirmed AND the torch trigger
   is pulled; the arc must also be blocked whenever the gas flow
   sensor drops out mid-weld.
   ============================================================ *)
PROGRAM welder_control
  VAR
    gas_flow_ok   AT %IX0.0 : BOOL;
    trigger_pull  AT %IX0.1 : BOOL;
    arc_on        AT %QX0.0 : BOOL;
  END_VAR

  IF NOT gas_flow_ok THEN
    arc_on := FALSE;
  ELSIF trigger_pull AND gas_flow_ok THEN
    arc_on := TRUE;
  ELSE
    arc_on := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : welder_control;
  END_RESOURCE
END_CONFIGURATION
```
