# Are these programs runnable outside ESBMC?

ESBMC parses PLCopen XML with pugixml, which is forgiving. That tells you nothing about
whether another vendor's tool would accept the same file. This note records what an
independent IEC 61131-3 toolchain does with the programs in this suite, and how to
repeat the experiment.

Three questions, in increasing strength:

1. Is the file well-formed XML?
2. Does it validate against the PLCopen TC6 schema?
3. Does it compile to code that runs?

## 1 and 2: well-formedness and schema

`runner/schema_check.py` answers both. See *Reproducing* on the portal.

As of 2026-08-26: 42 of 58 programs validate. The 16 that do not are the `g_tank_*`
benchmarks, which carry no PLCopen namespace at all and which an importer will not
recognise as PLCopen documents.

## 3: compile and run

The chain is PLCopen XML → Structured Text → C → native binary, using two projects that
are independent of ESBMC and of each other.

| stage | tool | notes |
|---|---|---|
| XML → ST | [Beremiz](https://github.com/beremiz/beremiz) `PLCGenerator` | GUI-free once `wx` is stubbed |
| ST → C | [MatIEC](https://github.com/beremiz/matiec) `iec2c` | needs autoconf, automake, bison 3, flex |
| C → binary | any C compiler | link against `matiec/lib/C` |

### Worked example

`benchmarks/manufacturing/g_comb_and/program.xml` is three contacts in series driving a
coil. Beremiz generates:

```pascal
PROGRAM g_comb_and
  VAR_INPUT  A : BOOL; B : BOOL; C : BOOL; END_VAR
  VAR_OUTPUT Y : BOOL; END_VAR
  Y := C AND B AND A;
END_PROGRAM
```

`iec2c` turns the body into:

```c
__SET_VAR(data__->,Y,,((__GET_VAR(data__->C,) && __GET_VAR(data__->B,)) && __GET_VAR(data__->A,)));
```

Compiled and driven over all eight input combinations, the binary prints the truth table
of a three-input AND, with `Y` high only for `A=B=C=1`. The ladder runs.

## Two interoperability defects found on the way

**The task interval was written in the wrong notation, and that was our defect.** These
programs used to declare `interval="PT0.01S"`, the ISO 8601 spelling. The TC6 schema types
the attribute as a string and annotates it *"Either a constant duration as defined in the
IEC or variable name"*, which means `T#10ms`. Beremiz passed the ISO form through
unchanged, correctly, and `iec2c` rejected it:

```
error: invalid task initialization in task declaration.
```

Worse, ESBMC did not reject it. Its front end reads the interval with a parser that
requires the IEC `#` form, found none, and fell back to a one millisecond tick, so every
timer preset in the suite was ten times longer than intended with no diagnostic. All 43
programs were corrected to `T#10ms` on 2026-08-26, after which the round trip below runs
with no hand patching.

**Namespace version.** Programs here declare `tc6_0200` while the published schema
targets `tc6_0201`. The element vocabulary is the same, so validation and generation both
work once the namespace is rewritten, which `schema_check.py` does in memory.

## Coverage

The round trip above was carried out end to end for one program. Running the whole corpus
through Beremiz's generator with a minimal controller stub produced ST for 21 of 43
programs; several of the remaining failures are the stub's fault rather than the files'
(FBD bodies need a block-type lookup the stub does not provide). Extending that stub and
recording a per-program result is open work.
