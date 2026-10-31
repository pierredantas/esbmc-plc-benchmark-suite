"""Prove the ST, IL, and FBD re-encodings equal their textual-ladder sources over one scan from any prior state (R2.4).

Each program is compiled to C (Beremiz for FBD, then MATIEC), and ESBMC checks that its output equals the source's
expression for every input and prior output. A control asserts the negated reference and must be refuted.

    equiv_proof.py SUITE ESBMC VIAC_SUITE
"""
import json, pathlib, subprocess, sys, tempfile

suite, esbmc, viac = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
sys.path.insert(0, str(viac / "runner"))
import record_via_c as rvc  # noqa: E402

CASES = {  # id: (file, input names, output, reference over C variables a (inputs) and prev (prior output))
    "st_seal_in": ("seal_in.st", ["START", "STOP"], "RUN", "(START || prev) && !STOP"),
    "il_seal_in": ("seal_in.il", ["START", "STOP"], "RUN", "(START || prev) && !STOP"),
    "fbd_seal_in": ("program.xml", ["START", "STOP"], "RUN", "(START || prev) && !STOP"),
    "st_comb_and": ("comb_and.st", ["A", "B", "C"], "Y", "A && B && C"),
    "il_comb_and": ("comb_and.il", ["A", "B", "C"], "Y", "A && B && C"),
    "fbd_comb_and": ("program.xml", ["A", "B", "C"], "Y", "A && B && C"),
}
results = {}
for bid, (fname, ins, out, ref) in CASES.items():
    d = next((suite / "benchmarks").glob(f"*/{bid}"))
    prog = d / fname
    work = pathlib.Path(tempfile.mkdtemp())
    try:
        harness_file, outdir, _ = rvc.build(prog, d / "props.yaml", work, 1)
    except Exception as e:
        results[bid] = f"build failed: {str(e)[:80]}"; print(bid, results[bid]); continue
    header = (outdir / "POUS.h").read_text()
    struct = rvc.entry_struct(prog, header)
    pou = struct[: -len("_data__")]
    decl = "".join(f"  _Bool {n.lower()} = nondet_bool();\n  __SET_VAR(d., {n}, , {n.lower()});\n" for n in ins)
    expr = ref
    for n in ins:
        expr = expr.replace(n, n.lower())
    verdicts = {}
    for label, claim in (("equal", f"__GET_VAR(d.{out},) == ({expr})"), ("control", f"__GET_VAR(d.{out},) != ({expr})")):
        c = (f'#include "iec_std_lib.h"\n#include "POUS.h"\n#include "POUS.c"\n_Bool nondet_bool(void);\n'
             f"int main(void) {{\n  {struct} d = {{0}};\n  {pou}_init__(&d, 0);\n"
             f"  _Bool prev = nondet_bool();\n  __SET_VAR(d., {out}, , prev);\n{decl}"
             f"  {pou}_body__(&d);\n  __ESBMC_assert({claim.replace('prev', 'prev')}, \"{label}\");\n  return 0;\n}}\n")
        (outdir / f"eq_{label}.c").write_text(c)
        r = subprocess.run([esbmc, str(outdir / f"eq_{label}.c"), "-I", str(rvc.TOOLS / "matiec" / "lib" / "C"),
                            "-I", str(outdir), "--unwind", "4", "--timeout", "60s"],
                           capture_output=True, text=True)
        o = r.stdout + r.stderr
        verdicts[label] = "SAFE" if "VERIFICATION SUCCESSFUL" in o else "VIOLATION" if "VERIFICATION FAILED" in o else "other"
    results[bid] = verdicts
    print(bid, verdicts, flush=True)
json.dump(results, open(pathlib.Path(__file__).with_name("equiv_results.json"), "w"), indent=1)
