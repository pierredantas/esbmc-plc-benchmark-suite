"""BMC depth of every conclusive violation answer on the Linux machine (run on the instance).
Mirrors the Apple-silicon pass: rerun each gate-passing VIOLATION once, read the last
"Checking base case, k = N" line. Usage: python3 depth_linux.py"""
import collections, glob, json, os, re, shlex, subprocess

HOME = os.path.expanduser("~/r12")
SUITE = HOME + "/rep1/suite"
BINS = {"v8.4": HOME + "/esbmc-84/build/src/esbmc/esbmc", "v8.6": HOME + "/esbmc-86/build/src/esbmc/esbmc"}

res = {v: collections.Counter() for v in BINS}
rows = []
for f in sorted(glob.glob(SUITE + "/results/records/*.json")):
    name = os.path.basename(f)[:-5]
    if name.endswith("__viac"):
        continue
    runs = json.load(open(f))["runs"]
    for ver, binary in BINS.items():
        r = runs.get(ver)
        if not r or r["verdict"] != "VIOLATION" or (r.get("encoding") or {}).get("gate") != "pass":
            continue
        lines = r["command"].split("\n")
        args = shlex.split(lines[-1])[1:]
        prog = args[0]
        if len(lines) > 1:
            subprocess.run(lines[0], shell=True, cwd=SUITE, check=True)
        else:
            subprocess.run(["cp", prog[:-3] + ".xml", prog], cwd=SUITE, check=True)
        out = subprocess.run([binary] + args, cwd=SUITE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True).stdout
        ks = re.findall(r"Checking base case, k = (\d+)", out)
        depth = int(ks[-1]) if ks else None
        os.remove(os.path.join(SUITE, prog))
        res[ver][depth] += 1
        rows.append((ver, name, depth))

for ver, c in res.items():
    print(ver, sum(c.values()), sorted(c.items(), key=str))
json.dump(rows, open(os.path.expanduser("~/depths_linux.json"), "w"))
