(* ============================================================
   Fire Service Recall : CLEAN baseline
   Safety: Active fire or smoke detection must place the car
   in recall_mode. The doors must never open in response to 
   standard hall calls during an active recall.
   Expected ESBMC-PLC+ verdict: SAFE (k-induction).
   ============================================================ *)
PROGRAM fire_recall
  VAR
    fire_alarm AT %IX0.0 : BOOL;
    smoke_detect AT %IX0.1 : BOOL;
    req_hall_call AT %IX0.2 : BOOL;
    recall_mode AT %QX0.0 : BOOL;
    doors_open AT %QX0.1 : BOOL;
  END_VAR

  recall_mode := fire_alarm OR smoke_detect;
  doors_open := req_hall_call AND NOT recall_mode;
END_PROGRAM
