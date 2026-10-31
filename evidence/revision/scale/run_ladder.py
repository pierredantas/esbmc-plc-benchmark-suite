import subprocess,json,sys,time,pathlib,statistics as st
M="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad"; suite=pathlib.Path(M)/"viac"
sys.path.insert(0,str(suite/"tools"))
from ld_text_to_xml import translate
out={}
for n in (10,100,500,1000,2000,4000):
    text="\n".join(f"OTE(R{i}) := (XIC(S{i}) + XIC(R{i})) * XIO(T{i}) ;" for i in range(n))
    d=pathlib.Path(M)/"scale"/f"lad{n}"; d.mkdir(exist_ok=True)
    (d/"p.ld").write_text(translate("p",text))
    props="format_version: \"0.1\"\nproperties:\n"+"".join(f"  - id: P{i}\n    kind: invariant\n    expression: \"!R{i} || !T{i}\"\n    justification: scale\n" for i in range(n))
    (d/"props.yaml").write_text(props)
    for v in ("84","86"):
        runs=[]
        for rep in range(3):
            rss=pathlib.Path(M)/"scale"/f"rss{v}.log"; rss.write_text("")
            t0=time.perf_counter()
            r=subprocess.run([f"{M}/scale/esbmc{v}.sh",str(d/"p.ld"),"--ld-props",str(d/"props.yaml"),"--k-induction","--ld-scan-watchdog","--ld-scan-budget","8","--ld-sound-mode","--timeout","120s"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            wall=time.perf_counter()-t0
            m=[int(x) for x in rss.read_text().split()]
            verdict="SAFE" if "VERIFICATION SUCCESSFUL" in r.stdout else ("VIOLATION" if "VERIFICATION FAILED" in r.stdout else "other")
            runs.append(dict(wall=round(wall,2),rss_mib=round(max(m)/1048576,1) if m else None,verdict=verdict))
            if wall>100: break
        out[f"{n}_{v}"]=runs
        print(n,v,runs,flush=True)
json.dump(out,open(f"{M}/scale/ladder.json","w"),indent=1)
print("FINISHED",flush=True)
