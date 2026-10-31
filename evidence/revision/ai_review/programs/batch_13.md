# Batch 13: benchmarks st_burner_purge, st_comb_and, st_compressor_cycle, st_counter_reset, st_door_reversal, st_estop_reset, st_guard_lock, st_pump_alternation

## st_burner_purge

- Language: ST
- File: burner_purge.st
- Properties:
- P1 (invariant): !MainValve || (PurgeDone && FlameProven)

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

## st_comb_and

- Language: ST
- File: comb_and.st
- Properties:
- P1 (invariant): !Y || (A && B && C)

```iecst
(* comb_and: three series contacts driving one coil.
   Structured Text rendering of ld_comb_and / g_comb_and.
   Y := A AND B AND C *)
PROGRAM drive
  VAR_INPUT
    A : BOOL;
    B : BOOL;
    C : BOOL;
  END_VAR
  VAR_OUTPUT
    Y : BOOL;
  END_VAR

  Y := A AND B AND C;
END_PROGRAM
```

## st_compressor_cycle

- Language: ST
- File: compressor_cycle.st
- Properties:
- P1 (invariant): !(Load && PressHigh)

```iecst
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

## st_counter_reset

- Language: ST
- File: counter_reset.st
- Properties:
- P1 (invariant): !Reset || (OUT == ResetCounterValue)

```iecst
(* counter_reset: a free-running counter with a reset-to-value.
   Reset loads ResetCounterValue, otherwise Cnt increments; OUT follows Cnt.
   Imported from the Beremiz IEC 61131-3 language test (CounterST function block),
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

  IF Reset THEN
    Cnt := ResetCounterValue;
  ELSE
    Cnt := Cnt + 1;
  END_IF;

  OUT := Cnt;
END_PROGRAM
```

## st_door_reversal

- Language: ST
- File: door_reversal.st
- Properties:
- P1 (invariant): !(MoveDown && Beam)

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

## st_estop_reset

- Language: ST
- File: estop_reset.st
- Properties:
- P1 (invariant): !(Run && EStop)

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

## st_guard_lock

- Language: ST
- File: guard_lock.st
- Properties:
- P1 (invariant): !(Unlocked && Motor)

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

## st_pump_alternation

- Language: ST
- File: pump_alternation.st
- Properties:
- P1 (mutual_exclusion): ['PumpA', 'PumpB']

```iecst
(* pump_alternation: duty-standby pump station.
   Structured Text rendering of g_pump_alternation.

   One pump runs at a time so the standby stays available. Duty changes hands
   each time the well empties, which is what keeps the second pump from sitting
   unstarted for a season. *)
PROGRAM station
  VAR_INPUT
    LevelHigh : BOOL;
    LevelLow  : BOOL;
  END_VAR
  VAR_OUTPUT
    Call  : BOOL;
    Duty  : BOOL;
    PumpA : BOOL;
    PumpB : BOOL;
  END_VAR

  Call := (Call OR LevelHigh) AND NOT LevelLow;
  Duty := (Duty AND NOT LevelLow) OR (NOT Duty AND LevelLow);
  PumpA := Call AND NOT Duty;
  PumpB := Call AND Duty;
END_PROGRAM
```
