# Provenance NOTES

- Source: Lessons In Electric Circuits, Volume IV - Digital, Chapter 6 (fail-safe design),
  by Tony R. Kuphaldt. https://www.ibiblio.org/kuphaldt/electricCircuits/
- License: Design Science License (confirmed against `Devel/dsl.html` on the source site;
  the index page's prose loosely calls this "the Creative Commons License", but the linked
  document is the Design Science License by Michael Stutz).
- Transcribed the fail-safe seal-in rung: Stop and thermal-overload inputs are wired as
  normally-closed, so the motor coil drops out on loss of continuity (wire break, relay
  trip) rather than requiring an active signal to stop.

- **P1 could not be stated as `!THERMAL_OVERLOAD_NC -> !MOTOR_RUN`.** ESBMC's
  `--ld-props` parser rejects `->` outright: `ERROR: property 'P1': undeclared variable
  '!THERMAL_OVERLOAD_NC -> !MOTOR_RUN'`, treating the whole expression as one token
  rather than parsing an implication. This is distinct from the IEC-keyword-spelling
  trap in esbmc#7371 (`NOT`/`AND` vs `!`/`&&`); here the operator itself is missing
  from the grammar regardless of spelling, and no other property in this suite uses
  `->`, so the gap had gone unexercised. Rewritten via De Morgan's law to
  `THERMAL_OVERLOAD_NC || !MOTOR_RUN`, logically equivalent to the original
  implication, which parses and proves SAFE at k=2. Recorded at
  `results/records/g_failsafe_motor_latch__failsafe_motor_latch.json`.
