import yaml,subprocess,json,sys
M="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad/indep"; E={'8.4':"/Users/user/esbmc-toolchain/bin/esbmc",'8.6':"/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/esbmc86src/build/src/esbmc/esbmc"}
res={}
for n in ('step_seq','cocktail','press_safety'):
    props=yaml.safe_load(open(f'{M}/props_{n}.yaml'))['properties']
    for p in props:
        yaml.safe_dump({'format_version':'0.1','properties':[p]},open(f'{M}/one.yaml','w'))
        row={}
        for v,b in E.items():
            try:
                r=subprocess.run([b,f'{M}/{n}_n.ld','--ld-props',f'{M}/one.yaml','--k-induction','--ld-scan-watchdog','--ld-scan-budget','8','--ld-sound-mode','--timeout','120s'],capture_output=True,text=True,timeout=140)
                o=r.stdout+r.stderr
                row['ladder '+v]='SAFE' if 'VERIFICATION SUCCESSFUL' in o else 'VIOLATION' if 'VERIFICATION FAILED' in o else 'unknown'
            except subprocess.TimeoutExpired: row['ladder '+v]='timeout'
        dest=f'{M}/viac3_{n}_{p["id"]}.json'
        try:
            subprocess.run([sys.executable,'runner/record_via_c.py',f'{M}/{n}_n.xml',f'{M}/one.yaml','true','--tool',f'v8.6={E["8.6"]}','--timeout','120','--scans','8','-o',dest],cwd="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/f6604d7d-0afd-466a-aa68-dc95e168034c/scratchpad/viac",capture_output=True,text=True,timeout=400)
            rec=json.load(open(dest))['runs']['v8.6']; row['C route 8.6']=rec['verdict']+(' (8 scans)' if rec['verdict']=='SAFE' and not rec.get('proof') else '')
        except Exception as e: row['C route 8.6']='error'
        res[f'{n}:{p["id"]}']=row; print(n,p['id'],row,flush=True)
json.dump(res,open(f'{M}/round3.json','w'),indent=1); print('FINISHED',flush=True)
