import sys,pathlib,json,yaml
sys.path.insert(0,"/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/plcverif_st")
sys.path.insert(0,"/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad/viac/runner")
import plcverif_st as pv, record_via_c as rvc
M=pathlib.Path("/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad/indep"); R=pathlib.Path("/Users/user/Claude/5_ESBMC-PLC Toolkit/ESBMC_PLC/results")
java="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad/jdk/jdk-27.0.1.0.2+1/Contents/Home/bin/java"; cli="/Users/user/Claude/tools/plcverif-cli"; nusmv="/Users/user/Claude/tools/nusmv-src/NuSMV-2.7.1/build/NuSMV"
builtin=str(R/"plcverif-timers-2026-10-23"/"builtin.scl"); blocks=str(R/"plcverif-counters-2026-10-23"/"iec_blocks.scl")
out={}
for n in ('step_seq','cocktail','press_safety'):
    d=M/f"pv_{n}"; d.mkdir(exist_ok=True)
    st=rvc.to_st(M/f"{n}_n.xml",d)
    props=yaml.safe_load(open(M/f"props_{n}.yaml"))["properties"]
    for p in props:
        try:
            scl,entry,uses=pv.convert(st,[p])
        except ValueError as e:
            out[f"{n}:{p['id']}"]="skipped: "+str(e); print(n,p['id'],out[f"{n}:{p['id']}"],flush=True); continue
        f=d/f"{p['id']}.scl"; f.write_text(scl)
        files=[str(f)]+([builtin] if uses&{"TON","TOF","TP"} else [])+([blocks] if uses&{"CTU","CTD","R_TRIG","F_TRIG"} else [])
        res,dt,txt=pv.run_plcverif(java,cli,nusmv,files,entry,f"{n}_{p['id']}",str(d/"out"))
        v={"SATISFIED":"SAFE","VIOLATED":"VIOLATION"}.get(res[0] if res else "","unknown")
        out[f"{n}:{p['id']}"]=v; print(n,p['id'],v,res,dt,flush=True)
json.dump(out,open(M/"plcverif_indep.json","w"),indent=1); print("FINISHED",flush=True)
