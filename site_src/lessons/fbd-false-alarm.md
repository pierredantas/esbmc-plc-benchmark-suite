A verifier that misses a defect has failed once, and one that condemns a correct program
has failed twice over: the engineer loses an afternoon to a program that was never broken,
and the next red result gets rather less attention than it deserves.

Both come from the same defect here.

## Two out of three

A pressure vessel with three switches on it. One switch reading high could be a fault, so tripping
on one is how a plant learns to bypass its own protection, while waiting for all three means
a genuine overpressure with a single dead switch never trips the vessel at all. The industry answer
is a vote: any two agreeing trip the reactor.

<svg class="diagram" viewBox="0 0 600 220" role="img" aria-label="Function block diagram: three AND blocks pair ps1 with ps2, ps2 with ps3 and ps1 with ps3, and their outputs feed one OR block driving trip"><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="20" y="20" width="70" height="24" rx="2"/><rect x="20" y="98" width="70" height="24" rx="2"/><rect x="20" y="176" width="70" height="24" rx="2"/><rect x="180" y="26" width="66" height="52" rx="2"/><rect x="180" y="104" width="66" height="52" rx="2"/><rect x="180" y="158" width="66" height="52" rx="2"/><rect x="330" y="70" width="66" height="96" rx="2"/><rect x="450" y="106" width="80" height="24" rx="2"/></g><g stroke="currentColor" fill="none" stroke-width="1.4"><path d="M90 32 H150 V40 H180"/><path d="M90 110 H150 V64 H180"/><path d="M90 110 H160 V118 H180"/><path d="M90 188 H150 V142 H180"/><path d="M90 32 H130 V172 H180"/><path d="M90 188 H140 V196 H180"/><path d="M246 52 H290 V92 H330"/><path d="M246 130 H300 V118 H330"/><path d="M246 184 H310 V144 H330"/><path d="M396 118 H450"/></g><g fill="currentColor" font-size="12.5" text-anchor="middle"><text x="55" y="36">ps1</text><text x="55" y="114">ps2</text><text x="55" y="192">ps3</text><text x="213" y="57">AND</text><text x="213" y="135">AND</text><text x="213" y="189">AND</text><text x="363" y="123">OR</text><text x="490" y="123">trip</text></g></svg>

Three AND blocks, one per pair, into an OR.

{{show: benchmarks/chemical_batch/fbd_reactor_2oo3/props.yaml}}

Two properties, and they pull against each other on purpose. P1 says any two agreeing must
trip. P2 says nothing less than two may trip. A vote is exactly the logic that satisfies
both, which is why the pair is worth writing down.

## The defect

{{files: benchmarks/chemical_batch/fbd_reactor_2oo3/clean.xml | benchmarks/chemical_batch/fbd_reactor_2oo3/bomb.xml | benchmarks/chemical_batch/fbd_reactor_2oo3/props.yaml}}

The bombed file drops the `ps1 AND ps3` leg. Two of three pairs still vote, so the vessel
trips whenever the middle switch agrees with either neighbour, and the plant behaves
normally through commissioning. Only the outer pair is deaf: `ps1=1, ps2=0, ps3=1` leaves
`trip` low with two switches calling for it.

## The correct program, refuted

{{record: fbd_reactor_2oo3__clean}}

`VIOLATION`, on both builds, with `status: wrong`.

That is the clean file, which implements the vote correctly and satisfies both properties,
and the ladder front end refutes it anyway. The counterexample even looks plausible:

```
ps1 = 0
ps2 = 1
ps3 = 1
```

Two switches high, no trip, P1 broken. Except the program does trip on that input, and the
scan body says why it appeared not to:

```
1: IF !1 THEN GOTO 2
   ASSIGN ps1=NONDET(_Bool);
   ASSIGN ps2=NONDET(_Bool);
   ASSIGN ps3=NONDET(_Bool);
   GOTO 1
2:
```

Three inputs and nothing else. `trip` is never assigned, so it holds its initial value of
false forever and a property demanding that it rise is broken by construction, which is why
the gate says `fail` and names `trip` as the one variable no statement in the body drives.

## The C route

{{record: fbd_reactor_2oo3__clean__viac}}

`SAFE`, found by the forward condition at k = 9. The vote is correct and provably so.

## Both answers were wrong for one reason

Its bombed twin is refuted on the ladder route too, and that row reads `correct`.

That is the part worth sitting with. The same front end returns `VIOLATION` for the working
reactor and `VIOLATION` for the broken one, because it read neither program. One of those
rows counts as a pass in any table that compares verdict against expectation, and it was
right by accident.

| | ladder route | via-C | truth |
|---|---|---|---|
| clean | `VIOLATION`, gate fails | `SAFE` | correct program, falsely condemned |
| bomb | `VIOLATION`, gate fails | `VIOLATION` | broken program, right for the wrong reason |

An accuracy score over those four cells reports fifty percent and tells you nothing. The
gate column reports four failures out of four, and tells you everything: no verdict here
rests on the program in the file.

That is the argument for recording the encoding next to the verdict rather than the verdict
alone. [Lesson 1.4](../seal-in/index.md) made it on a ladder where the two builds disagreed.
This one makes it where the tool agrees with itself, twice, and is wrong both times.
