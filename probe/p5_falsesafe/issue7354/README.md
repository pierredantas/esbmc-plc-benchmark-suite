# Reproducer for esbmc/esbmc#7354

Three PLCopen files with identical interfaces and identical intent, differing only in
the body element. Each drives both outputs unconditionally, so the single property in
`props.yaml` is violated in every scan by construction.

```
esbmc <file>.ld --ld-props props.yaml --k-induction
```

| body | mode | master `d88a9fa4` | v8.4 `61172c6f` |
|---|---|---|---|
| `ld_both.ld` | `--k-induction` | FAILED | FAILED |
| `ld_both.ld` | `--incremental-bmc --unwind 10` | FAILED | FAILED |
| `st_both.ld` | `--k-induction` | **SUCCESSFUL** | **SUCCESSFUL** |
| `st_both.ld` | `--incremental-bmc --unwind 10` | UNKNOWN | UNKNOWN |
| `fbd_both.ld` | `--k-induction` | **SUCCESSFUL** | **SUCCESSFUL** |
| `fbd_both.ld` | `--incremental-bmc --unwind 10` | UNKNOWN | UNKNOWN |

The ladder body is refuted. The other two are proved, because the front end discarded
the body it could not read and verified the empty program that remained.

`--goto-functions-only` is the only way to see this today: `ld::scan_loop` contains
`ASSIGN A` and `ASSIGN B` for the ladder file and nothing at all for the other two.

Measured 2026-08-27, aarch64 macOS, both builds from source.
