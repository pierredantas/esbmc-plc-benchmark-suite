# g_motor_interlock — graphical LD twin

Graphical PLCopen XML (`tc6_0200`) twin of the textual benchmark
[`motor_interlock`](../motor_interlock/) — a **syntax-coverage pair**: identical logic in
graphical LD, used to test whether a tool handles both PLCopen encodings. Properties are
inherited from the textual twin (`properties_file: ../motor_interlock/props.yaml`).

## Logic
- `clean.xml`: two rungs — `Motor_A := fwd AND NOT rev`, `Motor_B := rev`. Mutually exclusive → **SAFE**.
- `bomb.xml`: adds an OR-branch `fwd AND rev AND maint` into **both** coils (the secret-knock
  LLB), so the knock energises both motors → **VIOLATION** of P1.

## Modeling note
The ST original re-evaluates coils each scan; the graphical twin is non-latching to match.
The knock's OR is modeled by factoring `fwd` to the end
(`Motor_A = ((NOT rev) OR (rev AND maint)) AND fwd`) so the **OR-junction lands on a
`contact`** (multiple `<connection>` children in a contact's `connectionPointIn`) — the
junction pattern the parseable corpus (e.g. `PLC-LD-dataset/legitimate_lstop_eq.xml`) is
proven to use — rather than on the coil. `Motor_B = rev` needs no bomb branch: `rev` is
already TRUE during the knock, so the interlock breaks the moment `Motor_A` also energises.

Verified so far: namespace (`tc6_0200`), element set (powerrail/contact/coil), and the
contact-junction construct all match the corpus ESBMC-GraphPLC parses. Not yet run through
the actual frontend (no binary in the authoring environment) — see suite README for the
exact `--ld-props` command.
