# Independent tier

Three programs that someone outside the author group wrote, taken from public GitHub projects, with ten properties that the suite authors wrote
for them. They sit outside `benchmarks/` and are not part of the 117 benchmarks and 186 variants that the paper counts. The paper reports them as
a replication (Supplementary Note S4, Table S4.1).

| Directory | Source (file, repository commit, blob) | License | Elements | Properties |
|---|---|---|---|---|
| `ind_press_safety` | omarfaruq-ai/Real-Time-Systems, `Exercise 5/Project Files/plc.xml`, e0e0ca3, c8a8ccb | GPL-2.0 | 77 | P1 to P4 |
| `ind_cocktail_dispenser` | solarfiretech/Pallas, `Examples/OpenPLCEditor/Pallas/src/build/OpenPLC Runtime v4/src/plc.xml`, ead8f71, b95361a | Apache-2.0 | 29 | P1 to P4 (C1 to C4 in the paper) |
| `ind_step_sequencer` | jjv432/SeniorDesign, `OpenPLCFolders/Lab2b/plc.xml`, 519ab1e, cf7b0ff | MIT | 17 | P1, P2 (S1, S2 in the paper) |

The license of each program is the license of the project it came from, recorded in `source.license`. The CC BY 4.0 license of the suite covers only the
properties, descriptors, and results that we added.

## How the programs were prepared

`program.xml` is the original file after `normalize_io.py`, which drops the I/O addresses and declares every variable that no coil writes as an input, so that
all routes treat it as free. Nothing else changes.

## Expected verdicts

Each program has one variant. Its verdict is VIOLATION when any property is violated. The verdicts rest on agreement between ESBMC 8.6 (ladder front end) and PLCverif
on every property, not on construction, and the programs are candidates: no second ESBMC route finishes on the programs with timers. `results.json` lists, for each
property, the answers of ESBMC 8.4, ESBMC 8.6, the C route through MATIEC, and PLCverif. The properties are ours and the programs are not, so the tier tests whether
the findings on our own programs recur on code that we did not write. It is not an estimate of how often they do.

## Checks

`python3 runner/validate.py` and `python3 runner/schema_check.py` cover this directory.
