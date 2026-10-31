# Batch 10: benchmarks ld_comb_mixed, ld_comb_or, ld_ctd_load, ld_ctu_saturate, ld_edge_counter, ld_ftrig_edge, ld_latch_basic, ld_rtrig_edge

## ld_comb_mixed

- Language: LD-textual
- File: comb_mixed.ld
- Properties:
- P1 (invariant): !Y || A || C

```text
// comb_mixed: series/parallel with a negated (XIO) contact
OTE(Y) := (XIC(A) * XIO(B)) + XIC(C) ;
```

## ld_comb_or

- Language: LD-textual
- File: comb_or.ld
- Properties:
- P1 (invariant): !Y || A || B

```text
// comb_or: parallel contacts (OR) -> coil
OTE(Y) := XIC(A) + XIC(B) ;
```

## ld_ctd_load

- Language: LD-textual
- File: ctd_load.ld
- Properties:
- P1 (invariant): !(Empty && Load)

```text
// ctd_load: count-down from preset; load restores the preset
CTD(CTD0_Q, 2, XIC(Pulse), XIC(Load)) ;
OTE(Empty) := XIC(CTD0_Q) ;
```

## ld_ctu_saturate

- Language: LD-textual
- File: ctu_saturate.ld
- Properties:
- P1 (invariant): !(Done && Reset)

```text
// ctu_saturate: count-up to preset then saturate; reset dominant
CTU(CTU0_Q, 2, XIC(Pulse), XIC(Reset)) ;
OTE(Done) := XIC(CTU0_Q) ;
```

## ld_edge_counter

- Language: LD-textual
- File: edge_counter.ld
- Properties:
- P1 (invariant): !(Full && Reset)

```text
// edge_counter: rising edges feed a counter; reset dominant
OTE(Rise) := XIC(Sig) * XIO(Sig_prev) ;
CTU(Cnt_Q, 3, XIC(Rise), XIC(Reset)) ;
OTE(Full) := XIC(Cnt_Q) ;
OTE(Sig_prev) := XIC(Sig) ;
```

## ld_ftrig_edge

- Language: LD-textual
- File: ftrig_edge.ld
- Properties:
- P1 (invariant): !OneShot || !Sig

```text
// ftrig_edge: falling-edge one-shot (F_TRIG lowering)
OTE(Fall) := XIO(Sig) * XIC(Sig_prev) ;
OTE(OneShot) := XIC(Fall) ;
OTE(Sig_prev) := XIC(Sig) ;
```

## ld_latch_basic

- Language: LD-textual
- File: latch_basic.ld
- Properties:
- P1 (invariant): !(Q && R)

```text
// latch_basic: set/reset latch; unlatch dominant within a scan
OTL(Q) := XIC(S) ;
OTU(Q) := XIC(R) ;
```

## ld_rtrig_edge

- Language: LD-textual
- File: rtrig_edge.ld
- Properties:
- P1 (invariant): !OneShot || Sig

```text
// rtrig_edge: rising-edge one-shot (R_TRIG lowering)
OTE(Rise) := XIC(Sig) * XIO(Sig_prev) ;
OTE(OneShot) := XIC(Rise) ;
OTE(Sig_prev) := XIC(Sig) ;
```
