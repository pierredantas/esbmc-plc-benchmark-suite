# The tools underneath

Nothing on this site is the work of one program. A verdict on a ladder diagram passes
through an XML parser, a translator or two, a symbolic execution engine and an SMT solver
before it reaches a page, and each of those is somebody else's project with its own
authors, license and bugs.

This page names them. It matters for a benchmark suite, because the set of things you are
trusting when you read `VERIFICATION SUCCESSFUL` is exactly the set of things listed here,
and that set is not the same on both routes.

## What is pinned

| tool | version used here | role |
|---|---|---|
| [ESBMC](https://github.com/esbmc/esbmc) | `61172c6f` (v8.4, 2026-07-06) and `d88a9fa4` (master, 2026-08-25) | the checker under test |
| [Clang / LLVM](https://llvm.org) | 18.1.8, arm64 | parses C for ESBMC's C front end |
| [Z3](https://github.com/Z3Prover/z3) | 4.13.3 | decides the formulas ESBMC builds |
| [MatIEC](https://github.com/beremiz/matiec) | `7949c0bd` (2026-05-03) | compiles ST and IL to C |
| [Beremiz](https://github.com/beremiz/beremiz) | `aeb89e80` (2026-08-18) | renders any PLCopen body as ST |
| [pugixml](https://pugixml.org) | v1.14, fetched at build time | parses PLCopen XML inside the LD front end |
| `xmllint` | libxml2, system | validates programs against the PLCopen TC6 schema |

Both ESBMC builds here were configured with Z3 alone. Bitwuzla, Boolector, CVC4 and CVC5
are all `Off` in the CMake cache, so every verdict on this site is Z3's.

## ESBMC

ESBMC is a bounded model checker. Give it a program and a property, and it unrolls the
program's control flow to some depth, encodes the result as a formula that is satisfiable
exactly when the property can be broken, and hands that formula to a solver. A satisfying
assignment is a counterexample: concrete inputs, step by step, that reach the bad state.

It has front ends for several languages, and the two that matter here are separate
programs that happen to live in one binary:

```
src/ld-frontend/       parses PLCopen XML, builds LD IR, emits GOTO
src/clang-c-frontend/  parses C with libclang, emits GOTO
```

They meet at GOTO, the intermediate form everything downstream consumes.
[How ESBMC-PLC works](how-esbmc-plc-works.md) follows a program through the left one.

## Clang does not read your ladder

This is the point people get wrong most often, so it is worth stating plainly. Clang is a
C and C++ compiler front end, part of the LLVM project, and ESBMC uses it to turn C source
into an AST it can lower to GOTO. That is all it does here.

It has nothing to do with the ladder route. `src/ld-frontend/` contains no reference to
clang at all, and its XML reading is done by pugixml, which the front end declares as its
own dependency in `src/ld-frontend/CMakeLists.txt`:

```cpp
#include <pugixml.hpp>
#include <unordered_map>
```

That second include is not incidental. Iterating an `unordered_map` to decide the order
rungs execute in is [esbmc#7352](https://github.com/esbmc/esbmc/issues/7352), and it is a
good illustration of why knowing which library sits under a front end is worth the five
minutes it takes to look.

Clang earns its place on the second route, where a program has already become C by the
time ESBMC sees it. There, Clang's reading of that C is part of what you trust.

## MatIEC

MatIEC is a compiler for IEC 61131-3, written by Mario de Sousa at the University of
Porto, with later contributions from Laurent Bessard and Edouard Tisserant. The source
headers date it to 2003 and name its reference: the *FINAL DRAFT - IEC 61131-3, 2nd Ed.
(2001-12-10)*. It is GPLv3.

The binary used here is `iec2c`, which takes Structured Text or Instruction List and emits
ANSI C:

```
iec2c -I <matiec>/lib -T <outdir> program.st
```

MatIEC is doing the semantic work on that route. When a `TON` timer in the generated C
behaves the way the standard says a `TON` behaves, that is MatIEC's reading of the
standard, not ESBMC's. Two of its habits shape the harness the suite wraps around its
output: it uppercases identifiers, and it gives a located variable a pointer rather than a
value, so anything reading `%IX0.0` back out has to dereference it.

MatIEC also declines a `VAR` block that mixes located and plain declarations, which is
why `record_via_c.py` splits them before handing the file over.

## Beremiz

Beremiz is an IDE for machine automation, and its README describes it as "an integrated
development environment for machine automation. It is Free Software, conforming to
IEC-61131 among other standards." The licensing is split by component: GPLv2 for the IDE,
LGPLv2.1 for the Python runtime, GPLv3 for the C++ runtime.

MatIEC handles text. Nothing in it reads a graphical body, so a ladder, function block
diagram or sequential function chart needs a translation into text before `iec2c` can be
useful, and Beremiz's `PLCGenerator` is what performs it. Given a PLCopen project it walks
the graph and writes equivalent ST.

The suite drives that generator headlessly, without the IDE:

```python
import types
_wx = types.ModuleType("wx")
_wx.GetTranslation = lambda s: s
sys.modules.setdefault("wx", _wx)

from plcopen.plcopen import LoadProject
from PLCGenerator import GenerateCurrentProgram
```

Beremiz imports `wx` for its translation catalog, but the generator itself needs no GUI,
so a stub module with one function on it is enough. Block types come from Beremiz's own
`StdBlckDct` rather than a table written here, which means `AND`, `TON` and the rest
resolve exactly as they do inside the IDE.

Filing [beremiz#83](https://github.com/beremiz/beremiz/issues/83) came out of this work:
`FactorizePaths` sorts a list of unequal-length branches and raises `TypeError` on
Python 3, because Python 3 will not order a `list` against an `int`.

## Z3

Z3 is the SMT solver, developed at Microsoft Research and released under the MIT license.
It answers one question, over and over: is this formula satisfiable? Everything above it
exists to phrase a question about a conveyor or a reactor in terms Z3 can answer.

Because Z3 is the only solver enabled in these builds, a solver-specific bug would show up
in every recorded run at once, with nothing to contradict it. That is a real limitation of
the current setup rather than a hypothetical one, and the honest mitigation is that the
defects found so far all sit in front ends, where a second route disagrees with the first.

## The PLCopen schema

A benchmark that no tool will import is not a benchmark. Every program here is validated
against PLCopen's TC6 XSD with `xmllint`:

```
xmllint --noout --schema tc6_xml_v201.xsd program.ld
```

The schema is not vendored into this repository, because redistributing it is PLCopen's
call rather than ours. `runner/schema_check.py` fetches it once into `~/.cache/plcopen`
and reuses it, and the copy it fetches lives in Beremiz's repository. So Beremiz appears
twice in the trusted base: once as a translator, and once as the source of the schema the
catalog is checked against.

## Two routes, two trusted bases

The reason for naming all of this is that the two verification routes do not depend on the
same things, and that difference is what makes their agreement worth something.

| | ladder route | via-C route |
|---|---|---|
| reads the program | ESBMC `ld-frontend`, pugixml | Beremiz, then MatIEC, then Clang |
| states the property | `--ld-props` YAML | assertion in a C harness |
| decides | Z3 | Z3 |

A defect in the ladder front end cannot produce the same wrong answer on both, because the
second route never runs that code. That is the entire value of carrying a program the long
way around, and it is how the suite establishes an expected verdict without asking the
tool under test what the answer should be.

`fbd_fan_damper` is what that looks like when it pays off. Its bomb is written in FBD, so
the ladder front end drops the body and the scan loop assigns nothing but three nondet
inputs; the ingestion gate fails on `fan`, and both builds return `unknown`. The via-C
route reads the same file through Beremiz, compiles it with MatIEC, and returns
`VIOLATION` with a counterexample. One route could not see the program, and the other
refuted it.

Of the 223 recorded runs, 166 take the ladder route and 57 take the via-C route, covering
LD, ST, IL and FBD sources. The procedure and its per-stage results are in
[docs/INTEROP.md](https://github.com/pierredantas/esbmc-plc-benchmark-suite/blob/main/docs/INTEROP.md).
