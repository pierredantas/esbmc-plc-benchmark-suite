# Ladder to structured text

Drop a PLCopen LD program here and read it back as IEC 61131-3 structured text. The
file never leaves your browser: the conversion runs locally, in JavaScript, the same
algorithm as [`runner/ld_to_st.py`](https://github.com/pierredantas/esbmc-plc-benchmark-suite/blob/main/runner/ld_to_st.py),
which is what generates the "Structured text, derived" panel on every benchmark page in
this suite. This is a reading aid, not a second ground truth: ESBMC verifies the ladder
program itself, never a rendering of it.

Works on any file with a `<pou><body><LD>` inside, not only files from this suite.

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
