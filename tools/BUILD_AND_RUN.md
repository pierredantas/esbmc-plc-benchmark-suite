# Building ESBMC-PLC v8.4 and running the suite (reproducible recipe)

The public ESBMC release binaries are built WITHOUT the LD front-end. To run this suite you
need a source build with `-DENABLE_LD_FRONTEND=On`. Recipe (linux/amd64, verified 2026-07):

## 1. Build the binary (in a container)
```
git clone --depth 1 --branch v8.4 https://github.com/esbmc/esbmc.git esbmc-src
docker run --rm --platform linux/amd64 -v "$PWD/esbmc-src":/src-ro:ro -v "$PWD/out":/out \
  -v "$PWD/tools/build_esbmc_v84.sh":/build.sh:ro ubuntu:22.04 bash /build.sh
# -> out/esbmc-linux-amd64 (+ out/libz3.so). ~15 min. Key cmake flags:
#    -DDOWNLOAD_DEPENDENCIES=On -DENABLE_LD_FRONTEND=On -DENABLE_Z3=On (rest of frontends Off)
```

## 2. Build the run image (boost + python3-yaml + binary)
```
cd out && cp ../tools/Dockerfile.run . && docker build --platform linux/amd64 -f Dockerfile.run -t esbmc-plc:run .
```

## 3. Run the suite
```
docker run --rm --platform linux/amd64 -v "<suite>":"<suite>" -w "<suite>" esbmc-plc:run \
  bash -lc "ESBMC=/usr/local/bin/esbmc python3 runner/run_v84.py"
# -> results/summary_v84_full.tsv
```

## v8.4 interface notes (IMPORTANT)
- Input must be **PLCopen XML** with a `.ld` extension (content ST/XML; the frontend XML-parses it).
  Standalone textual-LD DSL and raw `.st` are NOT accepted ("failed to figure out type" / "No document element").
- `--ld-props <file>`: YAML properties. `invariant.expression` takes a compound formula,
  written with **C operators**: `!`, `&&`, `||` and parentheses. IEC spelling is not parsed;
  `NOT (A AND B)` is read as one variable name and fails with
  `undeclared variable 'NOT (A AND B)'`. Kinds: invariant, mutual_exclusion, reachability,
  absence. NO `termination`.
- Non-termination is caught by `--ld-scan-watchdog --ld-scan-budget N` (no property file needed).
- `runner/run_v84.py` adapts the suite's schema to these rules at run time.
