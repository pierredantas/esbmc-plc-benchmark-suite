import json,glob,csv,os,sys,statistics as st
core={(r['id'],r['file'].split('.')[0]) for r in csv.DictReader(open('variants_302.csv')) if r['core_suite']=='yes'}
def times(dirs,ver):
    T={}
    for d in dirs:
        for f in glob.glob(d+'/results/records/*.json'):
            b=os.path.basename(f)[:-5]
            if b.endswith('__viac'): continue
            k=tuple(b.split('__')[:2])
            if k not in core: continue
            r=json.load(open(f))['runs'].get(ver)
            if r: T.setdefault(k,[]).append(r['cpu_time_s'])
    return T
q=lambda a,p:sorted(a)[int(round(p*(len(a)-1)))]
def report(T):
    med=[st.median(v) for v in T.values()]; allr=[x for v in T.values() for x in v]
    print(len(T),'per-variant median -> median %.3f p95 %.3f max %.3f'%(st.median(med),q(med,.95),max(med)))
    print('  all runs -> median %.3f p95 %.3f max %.3f'%(st.median(allr),q(allr,.95),max(allr)))
    print('  spread median %.3f max %.3f'%(st.median([max(v)-min(v) for v in T.values()]),max(max(v)-min(v) for v in T.values())))
if __name__=='__main__':
    P,S=sys.argv[1],sys.argv[2]
    print('old 8.4'); report(times([P+'/suite']+[P+'/rep%d/suite'%i for i in (2,3,4,5)],'v8.4'))
    print('old 8.5'); report(times([P+'/suite']+[P+'/rep%d/suite'%i for i in (2,3,4,5)],'v8.5'))
    dirs=[S+'/run86/rep%d/suite'%i for i in range(1,6)]
    print('new 8.4'); report(times(dirs,'v8.4'))
    print('new 8.6'); report(times(dirs,'v8.6'))
