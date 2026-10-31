import subprocess,json,sys,time,pathlib,re
M="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad"; suite=pathlib.Path(M)/"viac"
out={}
for N in (255,1023,4095,16383,32767):
    d=next((suite/"benchmarks").glob("*/counter_scalability"))
    prog=d/f"bomb_N{N:05d}.st"
    for v in ("84","86"):
        rss=pathlib.Path(M)/"scale"/f"rss{v}.log"; rss.write_text("")
        t0=time.perf_counter()
        r=subprocess.run([sys.executable,"runner/record_via_c.py",str(prog.relative_to(suite)),str((d/"props.yaml").relative_to(suite)),"false","--tool",f"v8.{v[1]}={M}/scale/esbmc{v}.sh","--timeout","120","--scans",str(N+2),"-o",f"{M}/scale/cs_{N}_{v}.json"],cwd=suite,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        wall=time.perf_counter()-t0
        try:
            rec=json.load(open(f"{M}/scale/cs_{N}_{v}.json"))["runs"][f"v8.{v[1]}"]; verdict=(rec["verdict"],rec["status"],rec["cpu_time_s"])
        except Exception as e: verdict=("error",str(e)[:60],None)
        m=[int(x) for x in rss.read_text().split()]
        out[f"{N}_{v}"]=dict(result=verdict,wall=round(wall,1),rss_mib=round(max(m)/1048576,1) if m else None)
        print(N,v,out[f"{N}_{v}"],flush=True)
json.dump(out,open(f"{M}/scale/counter.json","w"),indent=1)
print("FINISHED",flush=True)
