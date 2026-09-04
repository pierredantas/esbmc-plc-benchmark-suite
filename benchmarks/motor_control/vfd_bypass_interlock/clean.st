(* ============================================================
   VFD Bypass Interlock : CLEAN baseline
   Safety: The Variable Frequency Drive output contactor and the
   Direct-On-Line bypass contactor must never be closed 
   simultaneously, preventing severe short-circuits.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM vfd_bypass
  VAR
    req_vfd AT %IX0.0 : BOOL;
    req_bypass AT %IX0.1 : BOOL;
    vfd_out AT %QX0.0 : BOOL;
    bypass_cont AT %QX0.1 : BOOL;
  END_VAR

  vfd_out := req_vfd AND NOT bypass_cont;
  bypass_cont := req_bypass AND NOT vfd_out;
END_PROGRAM
