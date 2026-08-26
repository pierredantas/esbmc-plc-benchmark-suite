# A benchmark suite you can read

PLC programs, the safety properties they have to satisfy, and recorded runs of a model
checker against them. Every artifact here is a file you can download, open in a text
editor, change, and verify again.

The suite exists to test verification tools, so what it says about the one tool used
throughout is deliberately unflattering in places. That is the job.

## Start here

**[Lessons](lessons/index.md)** are the way in. Twenty-three of them, in four parts, each
built on one program and the runs recorded against it.

| part | what it covers |
|---|---|
| [Foundations](lessons/one-rung/index.md) | contacts, branches, rung order, timers and counters, on ladders small enough to read line by line |
| [Machines and their hazards](lessons/conveyor/index.md) | twelve industrial plants, and a bypass hidden in each |
| [Logic-level bombs](lessons/what-is-an-llb/index.md) | triggers, fuses, denial of control, and recovering the trigger from a counterexample |
| [Code from the plant](lessons/real-export/index.md) | programs neither of us wrote, and what they cost |

**[Benchmarks](benchmarks/index.md)** is the catalog: 68 tasks across ten industrial
domains and five IEC languages, each with its files, its expected verdict, and the method
that established it.

**[The five languages](languages.md)** writes one circuit six ways, and
**[How ESBMC-PLC works](how-esbmc-plc-works.md)** follows a program from XML to a verdict.
**[Reproducing](reproducing.md)** is how to run any of it yourself.

## Recorded, not live

Nothing runs when you load a page. Every verdict, scan body and counterexample came out of
a command printed beside it, from an ESBMC build named by its commit. Copy the command and
you get the same output. Disbelieve the page and you can check it.

That trade gives up interactivity and buys what a benchmark needs: results that do not
move under the reader.

## The verdict is not the result

A verifier that quietly drops a program body reports success, because an empty program
satisfies every safety property ever written. So each recorded run carries three things
next to its verdict: the exact command, the scan body the front end produced, and an
ingestion gate that fails when the property's variables were never assigned inside the
scan loop.

**Twenty-six of the 210 recorded runs here fail that gate.** Every one of them reports
`SAFE`, and every one of them is worthless.

[Lesson 1.4](lessons/seal-in/index.md) is the case that motivates the arrangement: two
builds return the same verdict on the same file, and only one of them verified the circuit
that file describes.

## What it is for

If you are evaluating a tool, the catalog gives you tasks whose expected verdicts were
established without that tool, which is the only way a disagreement means anything.
[Lesson 1.5](lessons/edges-and-scan-order/index.md) is what that looks like in practice:
the benchmark is right, the standard agrees with it, and the tool is wrong.

If you are writing control logic, the lessons are about properties rather than programs.
[Lesson 3.6](lessons/what-a-property-says/index.md) collects what the failures on this site
had in common, and none of them was a solver getting an answer wrong.

## Citing it

The archived release **v1.0.1** holds 50 benchmarks over 83 program variants and is what
the accompanying paper reports. This site tracks the working tree, which has grown since.
[Citing](citing.md) has the DOIs and the BibTeX.
