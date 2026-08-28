Nobody writes a two-hand control from contacts twice. Certified safety libraries ship it
as a block, you drop the block in, wire the two palm buttons, and the anti-tie-down logic
is somebody else's tested code. That is the shape safety logic actually arrives in.

So here is lesson 7.2's press again, with the identical Type II body moved into a
function block. Same machine, same properties, same expected answers. The ladder twin
verifies, and has since 7.2.

## The block

```
     LH ---[      ]
            TwoHandII  ]--- Stroke
     RH ---[      ]
```

```
BothOff := NOT LH AND NOT RH;
Armed := (Armed OR BothOff) AND NOT Stroke;
Stroke := (Stroke OR Armed) AND LH AND RH;
```

`BothOff` and `Armed` are the block's own locals, which is what makes the instance
stateful and the anti-tie-down work.

{{files: benchmarks/manufacturing/g_two_hand_fb/program.xml | benchmarks/manufacturing/g_two_hand_fb/type_i.xml | benchmarks/manufacturing/g_two_hand_fb/props.yaml}}

## Both builds fail the gate

{{record: g_two_hand_fb__program}}

`SAFE` on both, and the gate fails on both, with `Stroke` never driven. Here is the
whole scan body, from either build:

```
ASSIGN LH=NONDET(_Bool);
ASSIGN RH=NONDET(_Bool);
ASSIGN LH=NONDET(_Bool);
ASSIGN RH=NONDET(_Bool);
```

The block is not in it. Two proofs about a press with no logic in it at all.

## And the correct variant is condemned

Put the Type I body in the block instead, `Stroke := LH AND RH`, which is the program
lesson 7.2 proves safe. This time the gate passes.

{{predict: g_two_hand_fb__type_i | The block body is now the plain conjunction, and its ladder twin satisfies the property. What happens here?}}

Both builds refute a property that holds. The encoding says why:

```
ASSIGN THC0__LH=NONDET(_Bool);
ASSIGN THC0__RH=NONDET(_Bool);
ASSIGN THC0__Stroke=THC0__LH;
ASSIGN Stroke=THC0__Stroke;
```

Two separate defects, in one four-line block.

The block's inputs are havocked rather than bound. `THC0__LH` is a fresh unconstrained
value, not the program's `LH`, so the wiring from the call site is gone. Then the body
itself loses an operand: `Stroke := LH AND RH` arrives as `Stroke := LH`. We checked the
direction, and it keeps the first operand rather than a particular name: `B AND A`
becomes `B`, and `A OR B` becomes `A`. Arithmetic survives, so this looks specific to
boolean operators.

## What this does not mean

It would be easy to read that as "function blocks do not work", and it is narrower than
that. The eight `g_tank_*` benchmarks in Part 5 are function-block programs, they pass
their gates, and their verdicts are right, because their bombs are constant assignments
sitting inside the block bodies rather than functions of the block inputs, which means
an unbound parameter never changes the answer they give. Going back and reading their recorded encoding, the same
`NONDET` on every formal parameter is sitting there and has been all along.

That is the uncomfortable part. This is not a new regression: it is behavior the corpus
has been carrying since the tank programs were imported, invisible the whole time because
nothing in it had ever asked a question whose answer depended on what a block does with
the arguments handed to it. Two rungs of ISO 13851 logic asked. The answer came back
about a different program.

The discriminator from 7.2 still runs here, for completeness, and inherits the same
problem.

{{record: twohand_fb_tiedown_ii}}

{{record: twohand_fb_tiedown_i}}

## Where this leaves the part

{{stat: benchmarks.discriminator|Words}} machines in this part carry a discriminator that separates a correct
program from a plausible wrong one. This one cannot, because the checker is not reading the program.
That makes it the odd lesson out here and a natural neighbour of Part 6, where the same
thing happens to function block diagrams and sequential function charts.

The suite ships it anyway, marked `candidate` rather than `validated`, with the ladder
twin as its ground truth. A gap you can point at is worth more than a benchmark quietly
dropped for answering wrong.
