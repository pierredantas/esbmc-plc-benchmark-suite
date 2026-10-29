"""Size of independently written public ladder programs vs the suite's ladder programs.
Inputs: ESBMC_PLC/ws_thirdparty/results/programs.json (GitHub mining of 2026-10-19, ACM study) and
structural.json (this folder). Elements = contacts + coils + blocks."""
import json, statistics as st, sys
programs, structural = sys.argv[1], sys.argv[2]
P = json.load(open(programs))
ld = [p for p in P if p.get("bodies", {}).get("LD", 0) > 0]
DS = lambda r: any(k in r.lower() for k in ("defuser", "lld_security", "lld-security", "plc-ld", "plc_ld", "clone"))
projects = [p for p in ld if not any(DS(r) for r in p["repos"])]
el = lambda p: p["contacts"] + p["coils"] + p["blocks"]
e = sorted(el(p) for p in projects)
q = st.quantiles(e, n=4)
print("public projects", len(projects), "median", st.median(e), "IQR", q[0], q[2], "max", e[-1])
print(">=10:", sum(x >= 10 for x in e) / len(e), ">=30:", sum(x >= 30 for x in e) / len(e), "with block:", sum(p["blocks"] > 0 for p in projects) / len(projects))
S = [r for r in json.load(open(structural)) if r["lang"] in ("LD-textual", "LD-graphical")]
s = sorted(r["coils"] + r["cont"] + r["blocks"] for r in S)
print("suite LD", len(s), "median", st.median(s), "IQR", st.quantiles(s, n=4)[0], st.quantiles(s, n=4)[2], "max", s[-1], ">=10:", sum(x >= 10 for x in s) / len(s), ">=30:", sum(x >= 30 for x in s))
