# Reproducing

You need one ESBMC binary and Python 3.8 or later. No other services, no accounts.

## Get ESBMC

Releases are at [github.com/esbmc/esbmc](https://github.com/esbmc/esbmc/releases). The
LD front end used throughout these lessons landed in 8.4. If you are on Apple silicon,
the upstream release has no Darwin build and the source build hits six separate
blockers; [Building ESBMC on macOS](build-macos.md) documents each one and the fix.

## Run a lesson

```bash
git clone https://github.com/pierredantas/esbmc-plc-benchmark-suite
cd esbmc-plc-benchmark-suite
ESBMC=/path/to/esbmc ./demo/run.sh      # lesson 1
ESBMC=/path/to/esbmc ./demo2/run.sh     # lesson 2
```

## Re-record a run

The panels on this site are rendered from `results/records/*.json`, which
`runner/record.py` writes:

```bash
python3 runner/record.py demo/interlock_bug.ld demo/props.yaml false \
  --tool v8.4=/path/to/esbmc-8.4/esbmc \
  --tool master=/path/to/esbmc-master/esbmc \
  -o results/records/interlock_viol.json
```

The third positional argument is the expected verdict, `true` for SAFE and `false` for
VIOLATION, and it picks the mode: k-induction for a program you expect to prove,
incremental BMC for one you expect to falsify. Override that with
`--mode kinduction` when you need a SUCCESSFUL to mean a proof rather than a bounded
silence, as lesson 2 does. Termination tasks take `--watchdog-only` and no property
file.

`record.py` exits 1 when any build's ingestion gate fails, so it drops into CI as it
stands.

## Rebuild this site

```bash
pip install -r site_src/requirements.txt
python3 site_src/build.py
mkdocs serve
```

`site_src/build.py` regenerates `portal/` from `site_src/`, `benchmarks/`, and
`results/records/`. That directory is not tracked, so edit the sources and never the
generated pages. Building the site needs no verifier at all, since the runs are already
recorded.
