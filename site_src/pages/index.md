# A benchmark suite you can read

PLC programs, the safety properties they have to satisfy, and recorded runs of a model
checker against them. Every artifact on this site is a file you can download, open in
a text editor, change, and verify again.

- **[Lessons](lessons/index.md)** take one ladder program at a time and show what the verifier
  did with it, counterexample included.
- **[Benchmarks](benchmarks/index.md)** is the catalog: 50 tasks over ten industrial domains,
  each with its files, its expected verdict, and the method that established it.
- **[Reproducing](reproducing.md)** is how to run any of it on your own machine.

## Recorded, not live

Nothing runs when you load a page. Every verdict, scan body, and counterexample here
came out of a command that is printed beside it, from an ESBMC build named by its
commit hash. Copy the command and you get the same output. Disbelieve the page and you
can check it.

That trade gives up interactivity and buys what a benchmark actually needs: results
that do not move under the reader.

## The verdict is not the result

A verifier that quietly drops a program body reports success, because an empty program
satisfies every safety property ever written. So each recorded run carries three things
next to the verdict: the exact command, the scan body the front end produced, and an
ingestion gate that fails when the property's variables were never assigned inside the
scan loop.

[Lesson 2](lessons/seal-in/index.md) is the case that motivates the whole arrangement. Two
builds return the same verdict on the same file, and only one of them verified the
circuit that file describes.
