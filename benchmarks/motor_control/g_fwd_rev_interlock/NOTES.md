# Provenance NOTES

- Source: Lessons In Electric Circuits, Volume IV - Digital, Chapter 6 (Ladder Logic),
  by Tony R. Kuphaldt. https://www.ibiblio.org/kuphaldt/electricCircuits/
- License: Design Science License (confirmed against `Devel/dsl.html` on the source site;
  the index page's prose loosely calls this "the Creative Commons License", but the linked
  document is the Design Science License by Michael Stutz).
- Transcribed the cross-interlocked FWD/REV motor-starter rung into PLCopen XML: each
  direction's coil is wired through the other direction's normally-closed contact.

- **SAFE, corrected on 2026-10-18 from an earlier VIOLATION label.** The rungs run in program
  order, so the reverse rung reads `M1_FWD` after the forward rung has written it in the same scan;
  with the motor stopped and both start buttons pressed on one scan, the forward coil energizes and
  the reverse coil stays off. Both coils can therefore never be on together at a scan boundary. The old label came from a
  counterexample that only an earlier ESBMC LD front end produced, because it read every coil's
  previous-scan value (esbmc/esbmc#7352, fixed in #8036). k-induction proves P1 at k = 2 on the LD
  front end and on ESBMC over MATIEC's C of the same program. What a scan cycle does change is
  priority, not safety: when both starts arrive in one scan with the motor stopped, the rung drawn
  first wins, where a relay
  panel would settle on whichever contact closed first.
