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
