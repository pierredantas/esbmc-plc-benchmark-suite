# A benchmark suite you can read

PLC programs, the safety properties they have to satisfy, and recorded runs of a model
checker against them. Every artifact here is a file you can download, open in a text
editor, change, and verify again.

The suite exists to test verification tools, so what it says about the one tool used
throughout is deliberately unflattering in places. That is the job.

## Start here

**[Lessons](lessons/index.md)** are the way in. {{stat: lessons.count|Words}} of them, in {{stat: lessons.parts|words}} parts, each
built on one program and the runs recorded against it.

| part | what it covers |
|---|---|
| [Foundations](lessons/one-rung/index.md) | contacts, branches, rung order, timers and counters, on ladders small enough to read line by line |
| [Machines and their hazards](lessons/conveyor/index.md) | twelve industrial plants, and a bypass hidden in each |
| [Logic-level bombs](lessons/what-is-an-llb/index.md) | triggers, fuses, denial of control, and recovering the trigger from a counterexample |
| [Code from the plant](lessons/real-export/index.md) | programs neither of us wrote, and what they cost |

**[Benchmarks](benchmarks/index.md)** is the catalog: {{stat: benchmarks.tasks}} tasks across {{stat: benchmarks.domains|words}} industrial
domains and five IEC languages, each with its files, its expected verdict, and the method
that established it.

**[The five languages](languages.md)** writes one circuit six ways, and
**[The properties we prove](properties.md)** is the other half of every benchmark: the four
kinds of question the suite asks, and what each becomes by the time the solver sees it.
**[How ESBMC-PLC works](how-esbmc-plc-works.md)** follows a program from XML to a verdict,
and **[Reproducing](reproducing.md)** is how to run any of it yourself.

## Recorded, not live

Nothing runs when you load a page. Every verdict, scan body and counterexample on this
site came out of a command printed beside it, run against an ESBMC build named by its
commit hash, so copying that command back into a shell gives you the same output. Disbelieve
the page and you can check it.

That trade gives up interactivity and buys what a benchmark needs: results that do not
move under the reader.

## The verdict is not the result

A verifier that quietly drops a program body reports success, because an empty program
satisfies every safety property ever written. So each recorded run carries three things
next to its verdict: the exact command, the scan body the front end produced, and an
ingestion gate that fails when the property's variables were never assigned inside the
scan loop.

Of the {{stat: runs.ladder}} runs that reach the ladder front end, **{{stat: gate.fail}} fail
that gate**, and they fail it in two different ways. {{stat: gate.fail.error|Words}} are files
ESBMC now refuses outright, naming the construct it cannot read. That diagnostic is new: until
[esbmc#7354](https://github.com/esbmc/esbmc/issues/7354) was fixed, the same files were
silently emptied and then proved correct.

The remaining {{stat: gate.fail.silent|words}} are what the gate is for. Both are confident
verdicts, one `SAFE` and one `VIOLATION`, and neither is an answer about the program in the
file. A violation raised inside an empty scan loop is worth no more than a proof found there.

[Lesson 1.4](lessons/seal-in/index.md) is the case that motivates the arrangement. Two
builds return the same verdict on the same file, and only one of them verified the circuit
that file describes.

## What it found

Four defects, each filed upstream with a reproducer:

| issue | defect |
|---|---|
| [esbmc#7354](https://github.com/esbmc/esbmc/issues/7354) | the ladder front end discards `ST`, `FBD` and `SFC` bodies, then reports `SUCCESSFUL` on the empty program that remains |
| [esbmc#7352](https://github.com/esbmc/esbmc/issues/7352) | scan order comes from hash iteration order when the right power rail is unwired |
| [esbmc#7353](https://github.com/esbmc/esbmc/issues/7353) | graphical `CTD` counters are never reloaded, because the load pin is not read |
| [beremiz#83](https://github.com/beremiz/beremiz/issues/83) | `FactorizePaths` raises `TypeError` on Python 3 for unequal-length parallel branches |

Three of the four are soundness bugs, which is to say the tool answers `SAFE` for a
program that plainly breaks its property, and that is the one kind of wrong answer a
verifier is never allowed to give.

None of the four came from reading the tool's source. Each surfaced because a benchmark
carried an expected verdict established without that tool, and the run disagreed with it.
That is the entire argument for building a catalog this way, and it is why the expected
verdicts here are derived from the standard and from a second toolchain rather than from
the checker under test.

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
