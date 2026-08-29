# Reproducer for esbmc/esbmc#7389

Three PLCopen files, each an `<LD>` program body holding one standard operator block.
They differ only in where the block sits relative to the rung.

- `rung_path.ld` — a `GT` block whose output drives the coil `alarm`. Property `!alarm`
  is false by construction, since `level > limit` is reachable.
- `data_path.ld` — a `DIV` block reading two `inVariable`s and writing the `outVariable`
  `scaled`, alongside an unrelated contact/coil rung. Property is boolean and true.
- `data_path_en.ld` — identical, except `EN` is wired from the contact so the block sits
  on the rung. Included to rule out a malformed-input explanation.

```
esbmc <file>.ld --ld-props <props>.yaml --k-induction
```

| file | props | master `0064c4ac` | v8.4 `61172c6f` |
|---|---|---|---|
| `rung_path.ld` | `rung_props.yaml` | `UnsupportedConstruct(GT, tier=2)` | **SUCCESSFUL** |
| `data_path.ld` | `props.yaml` | **SUCCESSFUL** | **SUCCESSFUL** |
| `data_path_en.ld` | `props.yaml` | **SUCCESSFUL** | **SUCCESSFUL** |

Master refuses the block that drives a coil and says so. v8.4 discards it in silence and
proves a property that is false by construction: its scan loop havocs `level` and `limit`,
reads neither, and never assigns `alarm`, so `ASSERT !alarm` holds vacuously.

Neither build handles the data path. In both, `scaled` is assigned once, to 0, ahead of
the loop and never inside it, while `raw` and `divisor` are havocked and read by nothing.
The division is absent from the model. Wiring `EN` changes nothing: the scan bodies of
`data_path.ld` and `data_path_en.ld` are byte-identical, so the block is dropped for what
it is rather than for how it is connected.

`--goto-functions-only` is the only way to see any of this; the verdict line alone cannot
distinguish a proof from an empty model.

Measured 2026-08-29, aarch64 macOS, both builds from source.
