# Review sheet: 12 programs anchored to a standard

For each program: the clause it cites, our property, and the mutants that no property kills. A surviving mutant may be harmless, or may be a behavior that the clause requires and that no property checks.

## g_burner_purge (LD-graphical)

- **Clause cited:** Authored from the light-off order in EN 298: purge, prove flame, then admit main gas, with a lockout that needs a manual reset
- **Safety intent:** The main gas valve must open only after the purge has completed and the flame is proven.
- **Property:** P1: !MainValve || (PurgeDone && FlameProven)
- **Discriminator:** lockout_check.props.yaml: P1 !Lockout || FlameFail (base VIOLATION)
- **Mutants:** 11; killed by the property 2; killed only by the discriminator 0; surviving 9
  - contact CallForHeat (feeds Fan) negated false->true
  - contact Lockout (feeds Lockout) negated false->true
  - contact FlameFail (feeds Lockout) negated false->true
  - contact ResetBtn (feeds Lockout) negated true->false
  - contact CallForHeat (feeds Pilot) negated false->true
  - contact PurgeDone (feeds Pilot) negated false->true
  - contact Lockout (feeds Pilot) negated true->false
  - contact CallForHeat (feeds MainValve) negated false->true
  - contact Lockout (feeds MainValve) negated true->false
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_door_reversal (LD-graphical)

- **Clause cited:** Authored from the reversal requirement for power-operated doors in EN 13241: an obstruction sends the door back to open rather than pausing it
- **Safety intent:** The door must never drive down while the photo-eye beam is broken.
- **Property:** P1: !(MoveDown && Beam)
- **Discriminator:** reversal_check.props.yaml: P1 !Reversing || Beam (base VIOLATION)
- **Mutants:** 8; killed by the property 1; killed only by the discriminator 0; surviving 7
  - contact Reversing (feeds Reversing) negated false->true
  - contact Beam (feeds Reversing) negated false->true
  - contact TopLimit (feeds Reversing) negated true->false
  - contact CloseCmd (feeds MoveDown) negated false->true
  - contact Reversing (feeds MoveDown) negated true->false
  - contact OpenCmd (feeds MoveUp) negated false->true
  - contact Reversing (feeds MoveUp) negated false->true
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_estop_reset (LD-graphical)

- **Clause cited:** Authored from the reset requirement in ISO 13850 and ISO 13849-1: the safety function is restored by a separate manual action, never by releasing the actuator
- **Safety intent:** The drive must never be energised while the emergency stop is actuated.
- **Property:** P1: !(Run && EStop)
- **Discriminator:** restart_check.props.yaml: P1 Safe || EStop (base VIOLATION)
- **Mutants:** 9; killed by the property 0; killed only by the discriminator 0; surviving 9
  - contact Reset_prev (feeds ResetEdge) negated false->true
  - contact Reset (feeds ResetEdge) negated true->false
  - contact Safe (feeds Safe) negated false->true
  - contact ResetEdge (feeds Safe) negated false->true
  - contact EStop (feeds Safe) negated true->false
  - contact Safe (feeds Run) negated false->true
  - contact Start (feeds Run) negated false->true
  - contact EStop (feeds Run) negated true->false
  - contact Reset (feeds Reset_prev) negated false->true
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_guard_lock (LD-graphical)

- **Clause cited:** Authored from the guard-locking requirement in ISO 14119: the guard stays locked until the hazardous movement has stopped, not until the drive command drops
- **Safety intent:** The safety guard must never be released while the drive is energised.
- **Property:** P1: !(Unlocked && Motor)
- **Discriminator:** rundown_check.props.yaml: P1 !OpenReq || Motor || Unlocked (base VIOLATION)
- **Mutants:** 5; killed by the property 2; killed only by the discriminator 0; surviving 3
  - contact Motor (feeds Unlocked) negated true->false
  - contact RunCmd (feeds Motor) negated false->true
  - contact DoorClosed (feeds Motor) negated false->true
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_phase_hold_permissive (LD-graphical)

- **Clause cited:** Authored for this suite, modeling an ISA-88 phase HELD state entered on agitator-permissive loss
- **Safety intent:** A phase held on permissive loss must keep the heater off; only explicitly clearing the hold may re-enable heating.
- **Property:** P1: !(held && heater)
- **Mutants:** 7; killed by the property 1; killed only by the discriminator 0; surviving 6
  - contact run_command (feeds held) negated false->true
  - contact agitator_ok (feeds held) negated true->false
  - contact held (feeds held) negated false->true
  - contact resume_command (feeds held) negated true->false
  - contact run_command (feeds heater) negated false->true
  - contact agitator_ok (feeds heater) negated false->true
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_two_hand (LD-graphical)

- **Clause cited:** Authored from the Type II requirements in ISO 13851: synchronous actuation, anti-tie-down and anti-repeat, so a taped actuator cannot start a cycle
- **Safety intent:** The ram must descend only while both hand actuators are held; releasing either one must stop the stroke.
- **Property:** P1: !Stroke || (LH && RH)
- **Discriminator:** tiedown_check.props.yaml: P1 !(LH && RH) || Stroke (base VIOLATION)
- **Mutants:** 9; killed by the property 2; killed only by the discriminator 1; surviving 6
  - contact LH (feeds BothOff) negated true->false
  - contact RH (feeds BothOff) negated true->false
  - contact Armed (feeds Armed) negated false->true
  - contact Stroke (feeds Armed) negated true->false
  - contact Stroke (feeds Stroke) negated false->true
  - contact Armed (feeds Stroke) negated false->true
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## g_two_hand_fb (LD-graphical)

- **Clause cited:** The ISO 13851 Type II logic of g_two_hand moved into a reusable function block, the shape certified safety libraries ship it in
- **Safety intent:** The ram must descend only while both hand actuators are held; releasing either one must stop the stroke.
- **Property:** P1: !Stroke || (LH && RH)
- **Discriminator:** tiedown_check.props.yaml: P1 !(LH && RH) || Stroke (base VIOLATION)
- **Mutants:** 9; killed by the property 2; killed only by the discriminator 1; surviving 6
  - ST body: AND -> OR in: BothOff := NOT LH AND NOT RH;
  - ST body: OR -> AND in: Armed := (Armed OR BothOff) AND NOT Stroke;
  - ST body: OR -> AND in: Stroke := (Stroke OR Armed) AND LH AND RH;
  - ST body: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
  - ST body: NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
  - ST body: NOT -> (removed) in: Armed := (Armed OR BothOff) AND NOT Stroke;
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## st_burner_purge (ST)

- **Clause cited:** Structured Text rendering of g_burner_purge, for cross-language comparison of the same machine
- **Safety intent:** 
- **Property:** P1: !MainValve || (PurgeDone && FlameProven)
- **Mutants:** 10; killed by the property 3; killed only by the discriminator 0; surviving 7
  - AND -> OR in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
  - AND -> OR in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
  - AND -> OR in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
  - OR -> AND in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
  - NOT -> (removed) in: Lockout := (Lockout OR FlameFail) AND NOT ResetBtn;
  - NOT -> (removed) in: Pilot := CallForHeat AND PurgeDone AND NOT Lockout;
  - NOT -> (removed) in: MainValve := CallForHeat AND PurgeDone AND FlameProven AND NOT Lockout;
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## st_door_reversal (ST)

- **Clause cited:** Structured Text rendering of g_door_reversal, for cross-language comparison of the same machine
- **Safety intent:** 
- **Property:** P1: !(MoveDown && Beam)
- **Mutants:** 8; killed by the property 3; killed only by the discriminator 0; surviving 5
  - AND -> OR in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
  - OR -> AND in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
  - OR -> AND in: MoveUp := OpenCmd OR Reversing;
  - NOT -> (removed) in: Reversing := (Reversing OR Beam) AND NOT TopLimit;
  - NOT -> (removed) in: MoveDown := CloseCmd AND NOT Beam AND NOT Reversing;
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## st_estop_reset (ST)

- **Clause cited:** Structured Text rendering of g_estop_reset, for cross-language comparison of the same safety function
- **Safety intent:** 
- **Property:** P1: !(Run && EStop)
- **Mutants:** 8; killed by the property 0; killed only by the discriminator 0; surviving 8
  - AND -> OR in: ResetEdge := Reset_prev AND NOT Reset;
  - AND -> OR in: Safe := (Safe OR ResetEdge) AND NOT EStop;
  - AND -> OR in: Run := Safe AND Start AND NOT EStop;
  - AND -> OR in: Run := Safe AND Start AND NOT EStop;
  - OR -> AND in: Safe := (Safe OR ResetEdge) AND NOT EStop;
  - NOT -> (removed) in: ResetEdge := Reset_prev AND NOT Reset;
  - NOT -> (removed) in: Safe := (Safe OR ResetEdge) AND NOT EStop;
  - NOT -> (removed) in: Run := Safe AND Start AND NOT EStop;
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## st_guard_lock (ST)

- **Clause cited:** Structured Text rendering of g_guard_lock, for cross-language comparison of the same safety function
- **Safety intent:** 
- **Property:** P1: !(Unlocked && Motor)
- **Mutants:** 5; killed by the property 4; killed only by the discriminator 0; surviving 1
  - NOT -> (removed) in: Rundown(IN := NOT Motor, PT := T#30ms);
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____

## st_two_hand (ST)

- **Clause cited:** Structured Text rendering of g_two_hand, for cross-language comparison of the same machine
- **Safety intent:** 
- **Property:** P1: !Stroke || (LH && RH)
- **Mutants:** 9; killed by the property 2; killed only by the discriminator 0; surviving 7
  - AND -> OR in: BothOff := NOT LH AND NOT RH;
  - AND -> OR in: Armed := (Armed OR BothOff) AND NOT Stroke;
  - OR -> AND in: Armed := (Armed OR BothOff) AND NOT Stroke;
  - OR -> AND in: Stroke := (Stroke OR Armed) AND LH AND RH;
  - NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
  - NOT -> (removed) in: BothOff := NOT LH AND NOT RH;
  - NOT -> (removed) in: Armed := (Armed OR BothOff) AND NOT Stroke;
- **Reviewer: does the program implement the clause? (yes / no / partly):** ____
- **Comment:** ____
