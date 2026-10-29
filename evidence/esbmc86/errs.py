import json,glob,csv,os,re,subprocess,shlex,sys,collections
S=sys.argv[1]; suite=S+'/run86/rep1/suite'; bn=S+'/esbmc86src/build/src/esbmc/esbmc'
core={(r['id'],r['file'].split('.')[0]) for r in csv.DictReader(open('/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/variants_302.csv')) if r['core_suite']=='yes'}
c=collections.Counter()
for f in sorted(glob.glob(suite+'/results/records/*.json')):
    b=os.path.basename(f)[:-5]
    if b.endswith('__viac'): continue
    k=tuple(b.split('__')[:2])
    if k not in core: continue
    r=json.load(open(f))['runs'].get('v8.6')
    if not r or r['verdict']!='error': continue
    lines=r['command'].split('\n'); last=shlex.split(lines[-1]); prog=last[1]
    if len(lines)>1: subprocess.run(lines[0],shell=True,cwd=suite,check=True)
    else: subprocess.run(['cp',prog[:-3]+'.xml',prog],cwd=suite,check=True)
    out=subprocess.run([bn]+last[1:],cwd=suite,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).stdout
    os.remove(os.path.join(suite,prog))
    m=[l for l in out.split('\n') if l.startswith('ERROR')]
    c[m[0] if m else '??']+=1; print(b,'|',m[:1])
print(c)
