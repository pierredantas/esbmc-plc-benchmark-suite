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
