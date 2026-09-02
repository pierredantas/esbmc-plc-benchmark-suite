# Provenance NOTES

- Source: Lessons In Electric Circuits, Volume IV - Digital, Chapter 6 (Ladder Logic),
  by Tony R. Kuphaldt. https://www.ibiblio.org/kuphaldt/electricCircuits/
- License: Design Science License (confirmed against `Devel/dsl.html` on the source site;
  the index page's prose loosely calls this "the Creative Commons License", but the linked
  document is the Design Science License by Michael Stutz).
- Transcribed the cross-interlocked FWD/REV motor-starter rung into PLCopen XML: each
  direction's coil is wired through the other direction's normally-closed contact.

- **Recorded as VIOLATION, not the SAFE the textbook diagram implies.** The interlock
  contact reads the *other* coil's state from the previous scan (`M2_REV__prev`,
  `M1_FWD__prev`), because a coil cannot gate on its own not-yet-computed value within
  the same scan. On the first scan both are 0/false, so pressing START_FWD and
  START_REV at the same instant energizes both M1_FWD and M2_REV together before either
  interlock contact has a true previous-scan value to block on. ESBMC finds this with
  `START_FWD=1, START_REV=1, STOP=0` on scan 1. A relay-based implementation of this
  diagram does not have this race (contacts and coils are simultaneous, not scanned),
  so the defect is specific to translating the rung into a scan-cycle PLC without an
  explicit same-scan mutual exclusion. Recorded at
  `results/records/g_fwd_rev_interlock__fwd_rev_interlock.json`.
