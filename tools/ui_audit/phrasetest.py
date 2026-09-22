# long runs of words repeated between two different texts of the game; the ceilings only come down
import re,sys,collections
s=open('/mnt/user-data/outputs/lanka-map3.html',encoding='utf8').read()
js=s.split('<script>')[1].split('</script>')[0]
js=re.sub(r'ref:"[^"]*"','',js)
texts=[m.group(1) for m in re.finditer(r'"([^"\n]{30,})"',js) if re.search(r'[\u0900-\u097F]{3}',m.group(1))]
W=[re.sub(r'[,।.:;!?]',' ',t).split() for t in texts]
N=7; seen=collections.defaultdict(set)
for ti,w in enumerate(W):
    for i in range(len(w)-N+1): seen[' '.join(w[i:i+N])].add(ti)
pairs=set()
for v in seen.values():
    v=sorted(v)
    for a in range(len(v)):
        for b in range(a+1,len(v)): pairs.add((v[a],v[b]))
def longest(A,B):
    best=0;prev=[0]*(len(B)+1)
    for i in range(1,len(A)+1):
        cur=[0]*(len(B)+1)
        for j in range(1,len(B)+1):
            if A[i-1]==B[j-1]:
                cur[j]=prev[j-1]+1; best=max(best,cur[j])
        prev=cur
    return best
L=[longest(W[a],W[b]) for a,b in pairs]
c20=sum(1 for x in L if x>=20); c12=sum(1 for x in L if 12<=x<20)
CEIL20,CEIL12=int(sys.argv[1]) if len(sys.argv)>1 else 0, int(sys.argv[2]) if len(sys.argv)>2 else 144
bad=[]
if c20>CEIL20: bad.append(f'{c20} repeats of 20+ words (ceiling {CEIL20})')
if c12>CEIL12: bad.append(f'{c12} repeats of 12 to 19 words (ceiling {CEIL12})')
print(('FAILS: '+'; '.join(bad)) if bad else f'phrase repeats checked: {c20} long, {c12} medium, {len(pairs)} short pairs')
