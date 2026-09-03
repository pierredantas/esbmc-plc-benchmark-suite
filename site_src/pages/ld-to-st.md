# Ladder to structured text

Drop a PLCopen LD program here and read it back as IEC 61131-3 structured text. The
file never leaves your browser: the conversion runs locally, in JavaScript, the same
algorithm as [`runner/ld_to_st.py`](https://github.com/pierredantas/esbmc-plc-benchmark-suite/blob/main/runner/ld_to_st.py),
which is what generates the "Structured text, derived" panel on every benchmark page in
this suite. This is a reading aid, not a second ground truth: ESBMC verifies the ladder
program itself, never a rendering of it.

Works on any file with a `<pou><body><LD>` inside, not only files from this suite.

## How the translation works

PLCopen XML does not store a rung as a line of contacts; it stores a graph. Every
element carries a `localId` and a `connectionPointIn` naming the `refLocalId`(s) it is
wired from. The translator starts at each coil and walks that graph backward toward the
power rail: one incoming reference is a series link (AND), two or more on the same
`connectionPointIn` are parallel branches (OR). The walk is memoized per `localId`, so a
contact feeding two coils is still evaluated once.

<svg class="diagram" viewBox="0 0 700 465" role="img" aria-label="Three views of the same rung: the ladder drawing with contacts A and B in parallel feeding negated contact C into coil Y; the PLCopen graph of localId nodes wired by connectionPointIn and refLocalId that ld_to_st.py actually walks; and the structured text the backward walk from the coil produces"><g fill="currentColor" font-size="12.5" font-weight="600"><text x="8" y="20">1. The rung, as drawn</text><text x="8" y="175">2. The PLCopen graph, as stored (and as ld_to_st.py walks it)</text><text x="8" y="345">3. The walk from the coil back to the rail</text></g><g stroke="currentColor" fill="none" stroke-width="2.4"><path d="M28 40 V128"/><path d="M592 40 V128"/></g><g stroke="currentColor" fill="none" stroke-width="1.6"><path d="M28 62 H110"/><path d="M126 62 H320"/><path d="M28 106 H110"/><path d="M126 106 H210"/><path d="M210 106 H320"/><path d="M320 62 V106"/><path d="M320 84 H366"/><path d="M382 84 H501"/><path d="M535 84 H592"/><path d="M110 50 V74"/><path d="M126 50 V74"/><path d="M110 94 V118"/><path d="M126 94 V118"/><path d="M366 72 V96"/><path d="M382 72 V96"/><path d="M362 98 L386 70"/><path d="M508 70 Q494 84 508 98"/><path d="M528 70 Q542 84 528 98"/></g><circle cx="320" cy="62" r="3.5" fill="currentColor"/><circle cx="320" cy="106" r="3.5" fill="currentColor"/><g fill="currentColor" font-size="13" text-anchor="middle"><text x="118" y="42">A</text><text x="118" y="130">B</text><text x="374" y="42">C</text><text x="518" y="42">Y</text></g><g stroke="currentColor" fill="none" stroke-width="1.4"><rect x="30" y="196" width="100" height="42" rx="3"/><rect x="30" y="268" width="100" height="42" rx="3"/><rect x="290" y="232" width="150" height="42" rx="3"/><rect x="560" y="232" width="110" height="42" rx="3"/></g><g fill="currentColor" font-size="12" text-anchor="middle"><text x="80" y="213">contact id=3</text><text x="80" y="229">var: A</text><text x="80" y="285">contact id=4</text><text x="80" y="301">var: B</text><text x="365" y="249">contact id=5, negated</text><text x="365" y="265">var: C</text><text x="615" y="249">coil id=6</text><text x="615" y="265">var: Y</text></g><g stroke="currentColor" fill="none" stroke-width="1.3" marker-end="url(#arrow)"><path d="M130 210 L290 244"/><path d="M130 282 L290 261"/><path d="M440 253 L560 253"/></g><g fill="currentColor" font-size="11" text-anchor="middle" font-style="italic"><text x="200" y="190">connectionPointIn</text><text x="200" y="325">refLocalId=3, 4</text><text x="500" y="244">refLocalId=5</text></g><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs><g font-family="var(--md-code-font)" font-size="12.5" fill="currentColor"><text x="30" y="366">coil 6 reads contact 5's connectionPointIn: one ref, so AND.</text><text x="30" y="386">contact 5 reads refLocalId 3 and 4: two refs, so OR.</text><text x="30" y="406">the walk bottoms out at the rails: 3 and 4 both read TRUE.</text></g><path d="M28 420 H672" stroke="currentColor" stroke-width="1" opacity="0.35"/><g font-family="var(--md-code-font)" font-size="15" fill="currentColor" font-weight="600"><text x="30" y="450">Y := (A OR B) AND NOT C;</text></g></svg>

Every function block call is collected the same way, before the coil assignments: a
block's inputs are walked first, so a call statement always precedes any expression that
reads `<instance>.<formal>` from it. When two rungs write the same coil, scan order
decides which write survives, and the rendered ST marks that target rather than hiding
the collision.

<div id="ld2st-app">
  <div id="ld2st-drop" tabindex="0" role="button"
       aria-label="Drop a PLCopen XML file here, or click to choose one">
    <p><strong>Drop a PLCopen XML file here</strong>, or click to choose one.</p>
    <p class="ld2st-hint">Nothing is uploaded. Parsing happens on this page.</p>
    <input id="ld2st-file" type="file" accept=".xml,.ld" hidden />
  </div>
  <p id="ld2st-name" class="ld2st-hint"></p>
  <div id="ld2st-error" class="ld2st-error" hidden></div>
  <div id="ld2st-result" hidden>
    <div class="ld2st-toolbar">
      <button id="ld2st-copy" type="button">Copy</button>
    </div>
    <pre><code id="ld2st-output" class="language-text"></code></pre>
  </div>
</div>

<script src="../scripts/ld-to-st.js"></script>
<script>
(function () {
  const drop = document.getElementById("ld2st-drop");
  const fileInput = document.getElementById("ld2st-file");
  const nameEl = document.getElementById("ld2st-name");
  const errorEl = document.getElementById("ld2st-error");
  const resultEl = document.getElementById("ld2st-result");
  const outputEl = document.getElementById("ld2st-output");
  const copyBtn = document.getElementById("ld2st-copy");

  function showError(message) {
    errorEl.textContent = message;
    errorEl.hidden = false;
    resultEl.hidden = true;
  }

  function showResult(text) {
    errorEl.hidden = true;
    outputEl.textContent = text || "(* no LD body in this file *)";
    resultEl.hidden = false;
  }

  function handleFile(file) {
    if (!file) return;
    nameEl.textContent = file.name;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        showResult(window.LdToSt.translate(reader.result));
      } catch (e) {
        showError(e.message);
      }
    };
    reader.onerror = () => showError("Could not read the file.");
    reader.readAsText(file);
  }

  drop.addEventListener("click", () => fileInput.click());
  drop.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileInput.click(); }
  });
  fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

  ["dragenter", "dragover"].forEach((evt) =>
    drop.addEventListener(evt, (e) => { e.preventDefault(); drop.classList.add("ld2st-over"); }));
  ["dragleave", "drop"].forEach((evt) =>
    drop.addEventListener(evt, (e) => { e.preventDefault(); drop.classList.remove("ld2st-over"); }));
  drop.addEventListener("drop", (e) => handleFile(e.dataTransfer.files[0]));

  function flashCopyLabel(label) {
    const original = copyBtn.textContent;
    copyBtn.textContent = label;
    setTimeout(() => { copyBtn.textContent = original; }, 1200);
  }

  copyBtn.addEventListener("click", () => {
    if (!navigator.clipboard) { flashCopyLabel("Copy not available"); return; }
    navigator.clipboard.writeText(outputEl.textContent)
      .then(() => flashCopyLabel("Copied"))
      .catch(() => flashCopyLabel("Copy failed"));
  });
})();
</script>

## Reading it from the command line instead

The same conversion, as a script:

```text
python3 runner/ld_to_st.py path/to/program.xml
```

Both the page above and the script read a `<pou>` element anywhere in the document
(not only under `<types><pous>`, since one vendor export nests it under a proprietary
extension instead), handle the `tc6_0200` and `tc6_0201` PLCopen namespaces, and fall
back to a `(* ... *)` comment rather than guessing when a `refLocalId` cannot be
resolved or a rung has more than one writer to the same coil.
