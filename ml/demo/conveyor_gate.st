(* ============================================================
   Conveyor infeed gate : demo program, not in the benchmark suite.
   Safety intent: the infeed gate must never open while the
   downstream jam sensor is active, and the conveyor motor must
   never run while the gate is open (product would fall through).
   ============================================================ *)
PROGRAM gate_control
  VAR
    jam_sensor   AT %IX0.0 : BOOL;  (* downstream jam detected *)
    start_button AT %IX0.1 : BOOL;
    stop_button  AT %IX0.2 : BOOL;
    gate_open    AT %QX0.0 : BOOL;
    motor_run    AT %QX0.1 : BOOL;
  END_VAR

  IF stop_button OR jam_sensor THEN
    gate_open := FALSE;
    motor_run := FALSE;
  ELSIF start_button AND NOT jam_sensor THEN
    motor_run := TRUE;
  END_IF;

  IF motor_run THEN
    gate_open := FALSE;
  ELSE
    gate_open := TRUE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK tcyclic(INTERVAL := T#10ms, PRIORITY := 0);
    PROGRAM inst0 WITH tcyclic : gate_control;
  END_RESOURCE
END_CONFIGURATION
