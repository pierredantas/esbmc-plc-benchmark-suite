Ladder has two spellings. Every program in the last six parts used the graphical one, a
graph of contacts and coils in PLCopen XML. The other is text, and this suite ships fifteen
programs written that way that no route here can verify.

## The notation

Here is the on-delay timer from [lesson 1.6](../timers/index.md), written textually:

{{code: benchmarks/hvac/ld_ton_single/ton_single.ld}}

`XIC` is examine-if-closed, a normally open contact. `OTE` is output-energise, a coil.
`TON` is the on-delay timer with its output, preset and enable. Three lines, and an
engineer reads the rung off them without a drawing.

The property is the one a timer deserves:

{{show: benchmarks/hvac/ld_ton_single/props.yaml}}

## What the tool does with it

```
$ esbmc benchmarks/hvac/ld_ton_single/ton_single.ld --ld-props ... --k-induction
ERROR: benchmarks/hvac/ld_ton_single/ton_single.ld: No document element found
ERROR: PARSING ERROR
```

Identical on both builds. ESBMC picks its ladder front end from the `.ld` extension and
then XML-parses the file, so a file of `XIC` and `OTE` lines produces the error an XML
parser gives an empty document.

This is the good failure. It refuses, loudly, at the front door, and nothing downstream
gets a chance to report `SAFE` about a program it never read. Compare
[lesson 6.1](../fbd-unread/index.md), where the same tool accepted a file, dropped its
body, and proved the empty remainder correct.

## The second route declines too

`record_all.py` decides what each route will attempt by extension:

```python
runnable = ((".xml",) if route == "ld" else (".xml", ".st", ".il"))
```

The textual DSL is in neither set. Beremiz reads PLCopen XML and MatIEC reads Structured
Text or Instruction List; neither speaks this notation, so the C route has nothing to
offer either. The skip is deliberate rather than an oversight, which is why these tasks
carry no run at all instead of a row of errors.

## Fifteen programs, no verdict

| | |
|---|---|
| LD-textual tasks in the catalog | 15 |
| with a recorded run on either route | 0 |
| with a graphical twin that does verify | 12 |

Twelve of the fifteen have a `g_` counterpart holding the same logic in PLCopen XML, and
those are verified. `ld_ton_single` has nothing; `g_ton_single` has a verdict from both
builds:

{{record: g_ton_single__program}}

So the suite can tell you the timer is correct. It cannot tell you the textual file
describes that timer, because nothing here reads the textual file. The two are related by
an author's intention and by nothing a tool checked.

Three have no twin at all: `ld_ton_chain2`, `ld_latch_basic` and `ld_edge_counter`. For
those the suite ships a program, a property and an expected verdict established by expert
review, and no machine has ever agreed or disagreed.

## Why keep them

A benchmark suite that only ships what its favourite tool can read is measuring the tool's
comfort rather than the standard's surface. Textual ladder is real: it is what the K-LD
executable-semantics work uses, and an engineer typing `XIC(Btn)` is writing ladder as
surely as one dragging a contact onto a rung.

Their presence is a standing question rather than a gap to apologise for. A tool that
claims IEC 61131-3 ladder coverage should say which spelling it means, and fifteen files
here make that question concrete instead of rhetorical.

## What would close it

Either end of the chain would do it. A front end that read the textual DSL would verify all fifteen directly, and a
converter into PLCopen XML would instead hand them to the route that already works, at the
cost of putting a translation of ours into the trusted base, which is the same trade
[the C route](../../the-tools-underneath.md) already makes for FBD and SFC.

Until one exists, these fifteen rows say `no run recorded`, and that is the honest entry.
