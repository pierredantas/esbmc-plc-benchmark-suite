import yaml,glob,os,re,json,sys,collections
sys.path.insert(0,"/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad"); sys.path.insert(0,"/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad/run/suite/tools")
import xml2smv as X
from ld_text_to_xml import translate as t2x
SUITE="/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad/run/suite"
sem=yaml.safe_load(open("/Users/user/Claude/4_Papers/ESBMC-Benchmark-Suite (Springer - Scientific Reports)/revision-evidence/semantics.yml"))
BLK=re.compile(r'typeName="(TON|TOF|TP|CTU|CTD|CTUD|R_TRIG|F_TRIG|SR|RS)"|:\s*(TON|TOF|TP|CTU|CTD|CTUD|R_TRIG|F_TRIG|SR|RS)\s*;|\b(TON|TOF|TP|CTU|CTD|CTUD|R_TRIG|F_TRIG)\s*\(|\b(OTL|OTU)\s*\(')
TIM=re.compile(r'\b(TON|TOF|TP|CTU|CTD|CTUD)\b')
KW={"IF","THEN","ELSE","ELSIF","END_IF","AND","OR","NOT","XOR","TRUE","FALSE","CASE","OF","END_CASE","WHILE","DO","END_WHILE","FOR","TO","BY","END_FOR","MOD","XIC","XIO","OTE","OTL","OTU","LD","ST","LDN","ANDN","ORN","S","R"}
def idents(t): return [x for x in re.findall(r"[A-Za-z_]\w*",t) if x.upper() not in KW and not re.fullmatch(r"T\d+|\d+",x)]
def first_read_before_write(text):
    text=re.sub(r"\(\*.*?\*\)|//[^\n]*","",text,flags=re.S)
    stmts=[]   # (reads, writes) in textual order
    for line in re.split(r";|\n",text):
        line=line.strip()
        if not line: continue
        m=re.match(r"OT[ELU]\((\w+)\)\s*:=\s*(.*)",line)
        if m: stmts.append((idents(m.group(2)),[m.group(1)])); continue
        m=re.match(r"(?:IF\s+(.*?)\s+THEN\s+)?([A-Za-z_]\w*)\s*:=\s*(.*)",line)
        if m: stmts.append((idents((m.group(1) or "")+" "+m.group(3)),[m.group(2)])); continue
        m=re.match(r"(?:ELS)?IF\s+(.*?)\s+THEN",line)
        if m: stmts.append((idents(m.group(1)),[]))
    assigned={w for _,ws in stmts for w in ws}; written=set(); ret=set()
    for reads,ws in stmts:
        for r in reads:
            if r in assigned and r not in written: ret.add(r)
        written|=set(ws)
    return ret
h1rec={}
for f in glob.glob(SUITE+"/results/records/*.json"):
    d=json.load(open(f)); r=d['runs']['v8.5']; h=(r.get('h1') or {}).get('verdict')
    bid=os.path.basename(f).split('__')[0]; h1rec.setdefault(bid,set()).add(h)
issues=[];cnt=collections.Counter()
for bp in sorted(glob.glob(SUITE+"/benchmarks/*/*/benchmark.yml")):
    b=yaml.safe_load(open(bp)); d=os.path.dirname(bp); bid=b['id']; e=sem[bid]; lang=b['language']
    texts=[]
    for v in b['variants']:
        t=open(os.path.join(d,v['file']),errors='ignore').read(); texts.append((v['file'],t))
    allt='\n'.join(t for _,t in texts)
    has_fb=bool(BLK.search(allt))
    has_tc=bool(TIM.search(re.sub(r'<!--.*?-->|//[^\n]*|\(\*.*?\*\)','',allt,flags=re.S)))
    # retained state by read-before-write (independent of translator)
    rbw=False
    for f,t in texts:
        if f.endswith('.xml'):
            try: rbw|=bool(X.translate(os.path.join(d,f))[2])
            except Exception: pass
        else: rbw|=bool(first_read_before_write(t))
    retained = has_fb or rbw
    tc_entry='timer_counter_model' in e; ret_entry='retained_state' in e; h1_entry='arithmetic' in e
    if tc_entry!=has_tc: issues.append((bid,'timer_counter',tc_entry,'vs',has_tc))
    if ret_entry!=retained: issues.append((bid,'retained_state',ret_entry,'vs',retained))
    hv=h1rec.get(bid,set())
    if 'unknown' in hv and not h1_entry: issues.append((bid,'H1 undecided by run',hv))
    if 'overflow' in hv and not h1_entry: issues.append((bid,'H1 overflow not recorded',hv))
    if h1_entry and 'overflow' not in hv: issues.append((bid,'H1 recorded without overflow run',hv))
    exp_scope='semantics-dependent' if (tc_entry or h1_entry or has_fb) else 'holds under the stated scan order'
    if e['verdict_scope']!=exp_scope: issues.append((bid,'scope',e['verdict_scope'],'vs',exp_scope))
    exp_so='sequential rung order within one scan' if lang.startswith('LD') else ('sequential statement order' if lang in('ST','IL') else 'tool-defined')
    if e['scan_order']!=exp_so: issues.append((bid,'scan_order',e['scan_order'],exp_so))
    cnt['checked']+=1
print(cnt,len(issues))
cat=collections.Counter(i[1] for i in issues); print(cat)
for i in issues: print(i)
json.dump(issues,open("/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad/audit_issues.json","w"))
