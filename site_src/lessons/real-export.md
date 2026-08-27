Sixty-eight benchmarks are in this catalog and sixty-seven of them were written by people
building a benchmark suite. This lesson is about the one that was not.

`g_ppu_evolution_1` came out of a real engineering tool:

```xml
<fileHeader companyName="Beckhoff Automation GmbH"
            productName="TwinCAT PLC Control" productVersion="3.5.10.30"
            creationDateTime="2019-09-26T16:12:41.2429215" />
```

It is from the PPU pick-and-place corpus, exported in 2019, and the program inside it is
about as small as a ladder gets: two contacts in series driving a coil.

{{show: benchmarks/manufacturing/g_ppu_evolution_1/props.yaml}}

{{files: benchmarks/manufacturing/g_ppu_evolution_1/evolution_1.xml | benchmarks/manufacturing/g_ppu_evolution_1/props.yaml}}

{{record: g_ppu_evolution_1__evolution_1}}

Proved on both builds. Nothing about the verdict is interesting. Everything about the
file is.

## It was the only one that validated

When this suite was first checked against PLCopen's own TC6 schema, the result was one
pass out of fifty-five programs. **This is the one.** Every hand-authored file failed, and
the errors were consistent enough to fix in a single pass: a `coordinateInfo` that
declared only `<ld>` where the schema wants `fbd`, `ld` and `sfc`, an SFC action missing
its `relPosition`, a step whose outgoing connection point lacked the required
`formalParameter`.

None of that was carelessness exactly. It was a set of assumptions about what a PLCopen
file looks like, held by people who had never read one that a tool produced. One real
export settled every question at once.

## And nothing in it is where you would look

Open the file and go to where the standard keeps programs:

```xml
<types>
  <dataTypes />
  <pous />
</types>
<instances>
  <configurations />
</instances>
```

Both empty. The program is not missing; it is somewhere else:

```
/project/addData/data/resource/addData/data/pou     name="Main"
```

Four levels down, inside vendor extension blocks under
`http://www.3s-software.com/plcopenxml/`. The resource and its task are in there too, and
the ladder body contains a `<vendorElement>` of its own. The file also opens with a
byte-order mark, which is legal and which a naive parser will choke on.

This is what `addData` is for. The schema provides it precisely so a vendor can carry
what the standard does not model, and TwinCAT uses it for the entire application. The
file is conformant. It is simply not organized the way a reader of the schema would
predict.

## Why ESBMC reads it anyway

Because its selector does not walk down from the root:

```cpp
root.select_nodes("//pou/body/LD | //pou/actions/action/body/LD")
```

`//pou` matches a POU at any depth. Had the front end looked in `types/pous`, where the
standard puts programs and where every one of our hand-written files puts them, it would
have found nothing here and reported an empty scan loop, which by now you know reports
`SAFE`.

A one-character difference in an xpath is the reason this benchmark works.

## The interval, and a correction to lesson 1.6

Here is the task this export declares:

```xml
<task name="PlcTask" interval="PT0S" priority="20" />
```

`PT0S` is an ISO 8601 duration. [Lesson 1.6](../timers/index.md) tells the story of this
suite writing `interval="PT0.01S"`, ESBMC failing to parse it, falling back to a one
millisecond tick, and every timer preset being ten times longer than intended. I framed
that as our mistake, on the strength of the TC6 schema annotating the attribute as
*"a constant duration as defined in the IEC"*.

The one real export in the catalog writes ISO 8601. So the picture is worse than a
mistake in our files:

| writes | reads |
|---|---|
| TwinCAT export: `PT0S` | ESBMC: needs `T#`, silently defaults to 1 ms otherwise |
| this suite, now: `T#10ms` | MatIEC: needs `T#`, rejects `PT0.01S` outright |
| TC6 annotation | says IEC duration |

Every timer preset in a real TwinCAT export is misread by ESBMC, silently, in exactly the
way lesson 1.6 describes. Switching our files to `T#` made them work and made them less
like the files they are supposed to represent. Both facts are true and the second one is
easy to forget.

## What this file is worth

More than its verdict, which is a two-contact conjunction nobody needed a solver for.

It is the control. Every assumption this suite makes about PLCopen is checkable against
it, and each time I have checked, the assumption was wrong in a way that mattered: where
the POU lives, what encoding the file uses, which duration notation a vendor writes,
whether `types/pous` is populated at all.

If you are assembling a benchmark suite in a format you do not control, get one genuine
export before you write the second file. Ours arrived late enough that fifty-four
programs had to be corrected, and it is still the only thing standing between this
catalog and a format that exists only in its own head.
