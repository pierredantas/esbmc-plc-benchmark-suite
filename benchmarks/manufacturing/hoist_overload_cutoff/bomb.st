(* ============================================================
   Crane hoist overload cutoff : BOMB variant.
   Seeded defect: the overload_tripped check was reordered from a
   leading guard to a trailing ELSIF, apparently to give the raise
   command "priority" for responsiveness. Since IF/ELSIF short-
   circuits on the first true branch, an operator holding
   raise_command energises hoist_raise even while the overload
   sensor is tripped; the ELSIF overload_tripped branch is now only
   reached when nobody is commanding a raise, which is exactly when
   the interlock was never needed.
   Expected verdict: VIOLATION of P1 (witness: P2).
   ============================================================ *)
PROGRAM hoist_control
  VAR
    overload_tripped AT %IX0.0 : BOOL;
    raise_command    AT %IX0.1 : BOOL;
    lower_command    AT %IX0.2 : BOOL;
    hoist_raise       AT %QX0.0 : BOOL;
    hoist_lower       AT %QX0.1 : BOOL;
  END_VAR

  IF raise_command AND NOT lower_command THEN
    hoist_raise := TRUE;
  ELSIF overload_tripped THEN
    hoist_raise := FALSE;
  ELSE
    hoist_raise := FALSE;
  END_IF;

  hoist_lower := lower_command AND NOT raise_command;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : hoist_control;
  END_RESOURCE
END_CONFIGURATION
