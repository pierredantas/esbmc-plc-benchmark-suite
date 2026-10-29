import csv,sys,statistics as st,os,collections
core={(r['id'],r['file'].split('.')[0]) for r in csv.DictReader(open('variants_302.csv')) if r['core_suite']=='yes'}
def mem(path):
    M=collections.defaultdict(list)
    for l in open(path):
        p=l.rstrip('\n').split('\t')
        if len(p)<2 or not p[1].isdigit(): continue
        a=p[0]; 
        i=a.find('/benchmarks/')
        if i<0: continue
        a=a[i+1:]
        parts=a.split('/'); stem=os.path.splitext(parts[-1])[0].replace('__xml',''); k=(parts[-2],stem)
        if k in core: M[k].append(int(p[1])/1048576)
    return M
for path in sys.argv[1:]:
    M=mem(path)
    mx=[max(v) for v in M.values()]
    print(os.path.basename(path),len(M),'median of per-variant max %.1f max %.1f'%(st.median(mx),max(mx)),'| entries/variant',len(next(iter(M.values()))))
