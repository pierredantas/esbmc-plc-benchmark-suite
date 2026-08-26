# Minimal ESBMC ladder example

One ladder program, one property, one verification. Two variants: one that proves,
one that produces a counterexample.

```
ESBMC=/path/to/esbmc ./run.sh
```

## The ladder (`interlock.ld`)

A **reversing starter**: one motor, two contactors. `KM_CW` closes to run it clockwise,
`KM_CCW` counter-clockwise (ACW in British schematics). Closing both at once shorts two
supply phases straight through the reversing contacts, so this interlock is wiring
protection rather than a process preference.

```
Rung 1:  fwd ---| |----|/|--- ( KM_CW )      KM_CW  := fwd AND NOT rev
                       rev
Rung 2:  rev ---| |------------( KM_CCW )     KM_CCW := rev
```

**The file extension must be `.ld`, but the content is PLCopen XML.** ESBMC-PLC v8.4
keys the LD front-end off the extension and then XML-parses the file. A `.xml` name is
rejected; a textual-LD DSL or a raw `.st` file is also rejected.

## The property (`props.yaml`)

```yaml
properties:
  - id: P1
    kind: mutual_exclusion
    variables: [KM_CW, KM_CCW]
    justification: "Forward and reverse contactors must never be energised together."
```

## Proving the correct version

```
$ esbmc interlock.ld --ld-props props.yaml --k-induction
VERIFICATION SUCCESSFUL
Solution found by the inductive step (k = 2)
```

`--k-induction` is the mode for an expected-SAFE program: it proves the property for
every scan, not just up to a bound.

## Falsifying the broken version

`interlock_bug.ld` is the same file with the `|/| rev` contact deleted from rung 1, so
`KM_CW := fwd` and nothing stops both contactors closing.

```
$ esbmc interlock_bug.ld --ld-props props.yaml --incremental-bmc --unwind 20
State 1   fwd = 1
State 2   rev = 1
State 3   KM_CCW = 1
State 4   KM_CW = 1
Violated property:
  P1
  !(KM_CW && KM_CCW)
VERIFICATION FAILED
Bug found (k = 1)
```

`--incremental-bmc` is the mode for an expected-VIOLATION program: it searches for a
counterexample and prints the input assignment that reaches the bad state.

## Property kinds that work in v8.4

| Kind | Required fields | Notes |
|---|---|---|
| `mutual_exclusion` | `variables` | |
| `invariant` | `expression` | Compound formulas work: `!(KM_CW && KM_CCW)`. Must use **C** operators, not `AND`/`NOT` |
| `reachability` | `expression`, `justification` | |
| `absence` | `subtype`, `expression` | |

Non-termination is checked separately with `--ld-scan-watchdog --ld-scan-budget N`,
with no property file.
