import re,collections,json
s=open('/mnt/user-data/outputs/lanka-map3.html',encoding='utf8').read()
js=s.split('<script>')[1].split('</script>')[0]
items=[]
for m in re.finditer(r'"([^"\n]{30,})"',js):
    t=m.group(1)
    if not re.search(r'[\u0900-\u097F]{3}',t): continue
    back=js[max(0,m.start()-200):m.start()]
    if re.search(r'ref:\s*$',back): continue
    # owner: nearest  key:{  or "key":{  before
    own=re.findall(r'(?:^|[\s,{])"?([\w\-]{2,})"?:\s*\{',js[max(0,m.start()-6000):m.start()])
    fld=re.findall(r'([a-zA-Z_]+):\s*\[?\s*(?:"[^"\n]*",?\s*)*$',back)
    items.append({'own':own[-1] if own else '?','fld':fld[-1] if fld else '?','t':t})
W=[re.sub(r'[,।.:;!?]',' ',x['t']).split() for x in items]
N=7; seen=collections.defaultdict(set)
for ti,w in enumerate(W):
    for i in range(len(w)-N+1): seen[' '.join(w[i:i+N])].add(ti)
pairs=set()
for v in seen.values():
    v=sorted(v)
    for a in range(len(v)):
        for b in range(a+1,len(v)): pairs.add((v[a],v[b]))
def longest(A,B):
    best=0;end=0;prev=[0]*(len(B)+1)
    for i in range(1,len(A)+1):
        cur=[0]*(len(B)+1)
        for j in range(1,len(B)+1):
            if A[i-1]==B[j-1]:
                cur[j]=prev[j-1]+1
                if cur[j]>best:best=cur[j];end=i
        prev=cur
    return best,' '.join(A[end-best:end])
rows=sorted([(longest(W[a],W[b])+(a,b)) for a,b in pairs],reverse=True)
json.dump({'items':items,'rows':rows},open('/tmp/longlist.json','w'),ensure_ascii=False)
