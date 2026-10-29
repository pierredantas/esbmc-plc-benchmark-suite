import json,glob,csv,os,re,subprocess,shlex,sys,collections
S=sys.argv[1]; suite=S+'/run86/rep1/suite'
bins={'v8.4':'/Users/user/esbmc-toolchain/bin/esbmc','v8.6':S+'/esbmc86src/build/src/esbmc/esbmc'}
core={(r['id'],r['file'].split('.')[0]) for r in csv.DictReader(open('/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/variants_302.csv')) if r['core_suite']=='yes'}
res={v:collections.Counter() for v in bins}; rows=[]
for f in sorted(glob.glob(suite+'/results/records/*.json')):
    b=os.path.basename(f)[:-5]
    if b.endswith('__viac'): continue
    k=tuple(b.split('__')[:2])
    if k not in core: continue
    runs=json.load(open(f))['runs']
    for ver,bn in bins.items():
        r=runs.get(ver)
        if not r or r['verdict']!='VIOLATION' or (r.get('encoding') or {}).get('gate')!='pass': continue
        lines=r['command'].split('\n'); last=shlex.split(lines[-1]); prog=last[1]
        if len(lines)>1: subprocess.run(lines[0],shell=True,cwd=suite,check=True)
        else:
            src=prog[:-3]+'.xml'; subprocess.run(['cp',src,prog],cwd=suite,check=True)
        out=subprocess.run([bn]+last[1:],cwd=suite,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).stdout
        ks=re.findall(r'Checking base case, k = (\d+)',out); d=int(ks[-1]) if ks else None
        os.remove(os.path.join(suite,prog))
        res[ver][d]+=1; rows.append((ver,b,d))
for v,c in res.items(): print(v,sum(c.values()),sorted(c.items(),key=str))
json.dump(rows,open(S+'/run86/depths.json','w'))
