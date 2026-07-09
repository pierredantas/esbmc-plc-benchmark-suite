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
