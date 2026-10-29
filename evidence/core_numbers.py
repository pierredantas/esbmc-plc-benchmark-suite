"""Every number of the core suite (117 benchmarks, 186 variants: v1.2.0 minus the 58 LLM-generated benchmarks)."""
import json,collections,yaml,glob,os,re,statistics as st,csv,sys
S="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad"; SUITE=S+"/run/suite"
imp=set(open("/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/removed_llm_generated_58.txt").read().split())
B={}
for bp in glob.glob(SUITE+"/benchmarks/*/*/benchmark.yml"):
    b=yaml.safe_load(open(bp)); b['_d']=os.path.dirname(bp)
    if b['id'] not in imp: B[b['id']]=b
ids=set(B)
St={r['id']:r for r in json.load(open(S+"/structural.json")) if r['id'] in ids}
for i in ids:
    if i=='g_ppu_evolution_1': St[i]['cls']='authored domain'
E=[r for r in json.load(open("/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/evidence86.json")) if r['id'] in ids]
pv=json.load(open(S+"/plcverif_final.json"))
for r in E:
    r['cls']=St[r['id']]['cls']; k="%s__%s"%(r['id'],r['file'].rsplit('.',1)[0]); r['pvc']=pv.get(k) in('SAFE','VIOLATION'); r['nvc']=r['nusmv'] in('SAFE','VIOLATION')
N={}
N['bench']=len(ids); N['var']=len(E); N['safe']=sum(r['exp']=='SAFE' for r in E); N['viol']=N['var']-N['safe']
N['lang_bench']=dict(collections.Counter(b['language'] for b in B.values())); N['lang_var']=dict(collections.Counter(r['lang'] for r in E))
N['domain']=dict(collections.Counter(b['domain'] for b in B.values())); N['diff']=dict(collections.Counter(b['difficulty'] for b in B.values()))
N['variants_per_bench']=dict(collections.Counter(len(b['variants']) for b in B.values()))
N['twins']=sum(1 for b in B.values() if b.get('syntax_pair_of'))
N['validated']=sum(b['validation_status']=='validated' for b in B.values()); N['candidate']=N['bench']-N['validated']
N['class']={c:dict(bench=sum(1 for i in ids if St[i]['cls']==c),var=sum(1 for r in E if r['cls']==c),validated=sum(B[i]['validation_status']=='validated' for i in ids if St[i]['cls']==c),
    coils=[st.median([St[i]['coils'] for i in ids if St[i]['cls']==c]),min(St[i]['coils'] for i in ids if St[i]['cls']==c),max(St[i]['coils'] for i in ids if St[i]['cls']==c)],
    cont=[st.median([St[i]['cont'] for i in ids if St[i]['cls']==c]),min(St[i]['cont'] for i in ids if St[i]['cls']==c),max(St[i]['cont'] for i in ids if St[i]['cls']==c)]) for c in ('third-party','authored micro','authored domain')}
N['origin_sources']=dict(collections.Counter(b['source']['origin'] for b in B.values()))
# methods
N['method']={m:dict(all=sum(1 for b in B.values() for v in b['variants'] if v['ground_truth']['method']==m),
   validated=sum(1 for b in B.values() if b['validation_status']=='validated' for v in b['variants'] if v['ground_truth']['method']==m)) for m in ('expert','fault-injection','cross-tool-consensus')}
# properties
pk=collections.Counter()
for b in B.values():
    p=yaml.safe_load(open(os.path.join(b['_d'],b.get('properties_file','props.yaml'))))
    for q in p['properties']: pk[q['kind']]+=1
N['props']=dict(pk); N['props_total']=sum(pk.values())
# ladder sizes
L=[St[i] for i in ids if St[i]['lang'] in('LD-textual','LD-graphical')]
e=sorted(r['coils']+r['cont']+r['blocks'] for r in L); q=st.quantiles(e,n=4)
N['ld']=dict(n=len(L),coils_med=st.median(r['coils'] for r in L),coils_iqr=[st.quantiles([r['coils'] for r in L],n=4)[0],st.quantiles([r['coils'] for r in L],n=4)[2]],cont_med=st.median(r['cont'] for r in L),cont_iqr=[st.quantiles([r['cont'] for r in L],n=4)[0],st.quantiles([r['cont'] for r in L],n=4)[2]],coils_max=max(r['coils'] for r in L),cont_max=max(r['cont'] for r in L),el_med=st.median(e),el_iqr=[q[0],q[2]],el_max=e[-1],ge10=sum(x>=10 for x in e)/len(e),ge10n=sum(x>=10 for x in e),ge30=sum(x>=30 for x in e))
G=[St[i] for i in ids if St[i]['lang']=='LD-graphical']; N['gr_with_block']=[sum(r['blocks']>0 for r in G),len(G)]
N['st_swat_assign']=[St[i]['coils'] for i in ids if i.startswith('st_swat')]
# funnel
def funnel(t):
    att=[r for r in E if r['s'+t]!='-']; g=[r for r in att if r['g'+t]=='pass']
    return dict(att=len(att),notatt=len(E)-len(att),gatefail=len(att)-len(g),gate=len(g),unk=sum(r['s'+t]=='unknown' for r in g),wrong=sum(r['s'+t]=='wrong' for r in g),h1=sum(r['s'+t]=='h1_violated' for r in g),agree=sum(r['s'+t]=='correct' for r in g),gf_match=sum(r['s'+t]=='correct' for r in att if r['g'+t]=='fail'))
N['f84']=funnel('84'); N['f86']=funnel('86')
a4=[r for r in E if r['s84']=='correct' and r['g84']=='pass']; a6=[r for r in E if r['s86']=='correct' and r['g86']=='pass']
N['conf']=dict(a4_nusmv=sum(r['nvc'] for r in a4),a4_either=sum(r['nvc'] or r['pvc'] for r in a4),a6_nusmv=sum(r['nvc'] for r in a6),a6_either=sum(r['nvc'] or r['pvc'] for r in a6))
N['nusmv']=sum(r['nvc'] for r in E); N['nusmv_split']=dict(collections.Counter(r['nusmv'] for r in E if r['nvc'])); N['plcverif']=sum(r['pvc'] for r in E); N['either']=sum(r['nvc'] or r['pvc'] for r in E)
N['plcverif_split']=dict(collections.Counter(pv["%s__%s"%(r['id'],r['file'].rsplit('.',1)[0])] for r in E if r['pvc']))
N['bench_conf_either']=len({r['id'] for r in E})-len({r['id'] for r in E if not(r['nvc'] or r['pvc'])})
N['bench_conf_nusmv']=len({r['id'] for r in E})-len({r['id'] for r in E if not r['nvc']})
def row(sub): 
    a=[r for r in sub if r['s86']!='-']
    return dict(n=len(sub),tried=len(a),m84=sum(r['s84']=='correct' and r['g84']=='pass' for r in sub),m86=sum(r['s86']=='correct' and r['g86']=='pass' for r in sub),nusmv=sum(r['nvc'] for r in sub),plcverif=sum(r['pvc'] for r in sub),h1=sum(r['s86']=='h1_violated' for r in sub))
N['rows']={}
for k in ('lang','cls','status'):
    for v in sorted(set(r[k] for r in E)): N['rows'][k+':'+v]=row([r for r in E if r[k]==v])
N['rows']['ALL']=row(E)
N['uncovered']=dict(total=sum(1 for r in E if not(r['nvc'] or r['pvc'])),by_lang=dict(collections.Counter(r['lang'] for r in E if not(r['nvc'] or r['pvc']))))
N['wrong84']=[(r['id'],r['file']) for r in E if r['s84']=='wrong' and r['g84']=='pass']; N['unknown84']=[(r['id'],r['file'],r['exp']) for r in E if r['s84']=='unknown' and r['g84']=='pass']
N['h1_ids']=sorted({r['id'] for r in E if r['s86']=='h1_violated'})
N['conf_status']=dict(collections.Counter((r['status'],bool(r['nvc'] or r['pvc'])) for r in E).items().__iter__().__class__ and {str(k):v for k,v in collections.Counter((r['status'],bool(r['nvc'] or r['pvc'])) for r in E).items()})
sem=yaml.safe_load(open("/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/semantics.yml")); sem={k:v for k,v in sem.items() if k in ids}
N['sem']=dict(retained=sum('retained_state' in v for v in sem.values()),timer=sum('timer_counter_model' in v for v in sem.values()),h1=sum('arithmetic' in v for v in sem.values()),scope=dict(collections.Counter(v['verdict_scope'] for v in sem.values())),
   sd_validated=sum(1 for k,v in sem.items() if v['verdict_scope']=='semantics-dependent' and B[k]['validation_status']=='validated'),sd_candidate=sum(1 for k,v in sem.items() if v['verdict_scope']=='semantics-dependent' and B[k]['validation_status']=='candidate'),
   hold_candidate=sum(1 for k,v in sem.items() if v['verdict_scope']!='semantics-dependent' and B[k]['validation_status']=='candidate'))
iss=json.load(open(S+"/audit_issues.json")); N['audit_issues_in_core']=len([i for i in iss if i[0] in ids]); N['audit_retained']=len([i for i in iss if i[0] in ids and i[1]=='retained_state']); N['audit_scope']=len([i for i in iss if i[0] in ids and i[1]=='scope'])
N['feat']=dict(comparison=sum('comparison' in b.get('features',[]) for b in B.values()),function_block=sum('function_block' in b.get('features',[]) for b in B.values()),multi_pou=sum('multi_pou' in b.get('features',[]) for b in B.values()))
json.dump(N,open("/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/core_numbers_v86.json","w"),indent=1,default=str)
print(json.dumps(N,indent=0,default=str)[:6500])
