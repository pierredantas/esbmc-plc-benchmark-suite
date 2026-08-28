Everything in this suite is built out of the two elements below. A contact asks a
question of a Boolean variable, and a coil writes the answer. Three contacts in a row
and one coil is enough of a program to state a property about, prove it, and read what
the verifier did with it.

## The rung

<svg class="diagram" viewBox="0 0 620 110" role="img" aria-label="Ladder rung: contacts A, B and C in series driving coil Y"><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 18 V92"/><path d="M592 18 V92"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 52 H110"/><path d="M126 52 H230"/><path d="M246 52 H350"/><path d="M366 52 H501"/><path d="M535 52 H592"/><path d="M110 40 V64"/><path d="M126 40 V64"/><path d="M230 40 V64"/><path d="M246 40 V64"/><path d="M350 40 V64"/><path d="M366 40 V64"/><path d="M508 38 Q494 52 508 66"/><path d="M528 38 Q542 52 528 66"/></g><g fill="currentColor" font-size="13" text-anchor="middle"><text x="118" y="32">A</text><text x="238" y="32">B</text><text x="358" y="32">C</text><text x="518" y="32">Y</text></g></svg>

Contacts in series conduct only when every one of them is closed, so the rung means
`Y := A AND B AND C`. Nothing is remembered between scans. Whatever the inputs are
when the scan starts, `Y` is decided before it ends.

{{files: benchmarks/manufacturing/g_comb_and/program.xml | benchmarks/manufacturing/g_comb_and/props.yaml}}

{{code: benchmarks/manufacturing/g_comb_and/program.xml}}

Four elements and a rail on each side. Notice that each contact names the element it
receives power from, in `<connectionPointIn>`, rather than sitting at a position on a
line. The drawing above is a rendering of that graph, not the program itself.

## The property

{{show: benchmarks/manufacturing/g_comb_and/props.yaml}}

Read `!Y || (A && B && C)` as an implication: if `Y` is energized then all three
contacts were closed. It says nothing about the reverse, which is deliberate. A
property is a claim you are prepared to defend, not a restatement of the code, and
restating the code proves nothing except that the tool can read it.

!!! warning "The extension decides the front end"
    ESBMC picks its LD front end from the file name, and the benchmark ships as
    `program.xml`. Copy it before you run:
    ```bash
    cp program.xml program.ld
    ```

## The run

{{record: comb_and}}

Both builds prove it, and both name the inductive step at k = 2. For a rung with no
memory that is what you expect: the base case covers the first scan, one inductive
step covers every scan after it, and there is nothing else for the proof to chase.

## Read the encoding

This is the first place worth slowing down, because the two tabs above disagree about
how to write the same rung.

One reasonable compilation is the assignment you would have written yourself:

```
ASSIGN Y=1 && A && B && C;
```

master threads power through the rung one contact at a time. `pf3` records whether the
rail reached the far side of contact A, `pf4` whether it got past B, `pf5` whether it
got past C, and only then is `Y` assigned:

```
IF !(1 && A)          THEN GOTO 3
ASSIGN pf3=1;
IF !(1 && pf3 && B)   THEN GOTO 5
ASSIGN pf4=1;
...
ASSIGN Y=1 && pf5;
```

On this rung the two are the same function. The accumulators exist because a real
ladder has branches, and a branch needs somewhere to put a partial result. Lesson 1.4
is where that difference stops being cosmetic and starts changing the verdict.

## The same rung in the other languages

The rung above is ladder, and ladder is one of five notations the standard defines. The
same three-input conjunction can be written in any of them, and the suite ships all four
spellings of this one program so a tool's coverage can be measured rather than assumed.

=== "Structured text"

    ```pascal
    Y := A AND B AND C;
    ```

=== "Instruction list"

    ```
          LD    A
          AND   B
          AND   C
          ST    Y
    ```

=== "Function block diagram"

    Three inVariables into one variadic AND block, its output wired to an outVariable.
    Beremiz renders that graph back to text as `_TMP_AND4_OUT := AND(A, B, C);`.

{{files: benchmarks/manufacturing/st_comb_and/comb_and.st | benchmarks/manufacturing/il_comb_and/comb_and.il | benchmarks/manufacturing/fbd_comb_and/program.xml | benchmarks/manufacturing/ld_comb_and/comb_and.ld}}

ESBMC's LD front end reads none of them. It registers one extension, `ld`, and one body
type, so a structured text file is `failed to figure out type of file` and an FBD body
inside a `.ld` file is discarded without a diagnostic. That is not a gap you can close by
writing the property differently.

## Real verdicts for all four, through C

There is a second route to the same solver, described in full on
[How ESBMC-PLC works](../../how-esbmc-plc-works.md). Beremiz renders any PLCopen body as
structured text, MatIEC compiles structured text or instruction list to C, and ESBMC has
read C for years. Every rendering below was verified that way, on this machine, against
the property this lesson already uses.

### Structured text

{{record: comb_and_st_viac}}

### Instruction list

{{record: comb_and_il_viac}}

### Function block diagram

{{record: comb_and_fbd_viac}}

### Ladder, for comparison

{{record: comb_and_ld_viac}}

Four notations, one program, four proofs, all closing by the forward condition at k = 4.
The ladder column is the interesting one: it is the same file the panel further up this
page verified through the LD front end, and it now has a second verdict reached without
that front end at all. Two independent routes agreeing is worth more than one route
insisting.

Read the generated harness in any of those panels. The property is not carried over from
the YAML file: it is written out over the C variables MatIEC emitted, which is the price
of this route and the reason it answers *is this program correct* rather than *does the
ladder front end read it correctly*.

One notation is missing from the four. The K-LD textual rung, `OTE(Y) := XIC(A) * XIC(B)
* XIC(C);`, is in the download table and no tool here reads it: ESBMC XML-parses the file
and fails, and Beremiz only reads PLCopen. It was validated with nuXmv, which is why the
suite keeps more than one tool in view.

## Try it

Change the property and predict the answer before you run it.

- `!Y || A` claims that `Y` implies `A` alone. Weaker than the original, so it still
  holds.
- `Y || !A` claims the reverse, that `A` alone is enough to energize `Y`. Run it and
  ESBMC hands you a scan where `A` is closed, one of the others is not, and `Y` stays
  low.

The second is the useful habit. Write the property you expect to fail, and check that
the tool fails it for the reason you expected, because a verifier that says SUCCESSFUL
to everything is telling you nothing.
