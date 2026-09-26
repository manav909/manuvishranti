import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re
head=open('gi-head.html').read(); foot=open('gi-foot.html').read(); data=open('lkdata.json').read()
style=re.search(r'<style>(.*?)</style>',head,re.S).group(1)
body=re.search(r'(<div id="gi".*?</div>\n)<script>',head,re.S).group(1)
script=re.search(r'<script>(.*?)</script>',foot,re.S).group(1)
def R(a,b,t):
    assert a in t,a[:70]; return t.replace(a,b)
style=R('#gi{position:fixed;inset:0;z-index:2147483000;overflow-y:auto;overflow-x:hidden;background:#07131B;','#gi{position:relative;overflow-x:hidden;background:#07131B;',style)
style='html,body{margin:0;background:#07131B}\nhtml{scroll-behavior:smooth}\n'+style
style=R('#gi button{font:inherit;color:inherit;cursor:pointer}','#gi button{font:inherit;color:inherit;cursor:pointer}\n#gi .gi-start{text-decoration:none;cursor:pointer}',style)
body=R(' role="dialog" aria-modal="true" aria-labelledby="giTitle"','',body)
body=body.replace('<button class="gi-start" type="button" data-go>','<a class="gi-start" href="/lanka_ki_khoj/" data-go>').replace('<span class="gi-lbl">खेल शुरू करो</span></button>','<span class="gi-lbl">खेल शुरू करो</span></a>')
body=R('<div class="gi-body" id="giBody"></div>','<main class="gi-body" id="giBody"></main>',body)
script=R("  function G(name,fb){try{var v=eval(name);return v==null?fb:v}catch(e){return fb}}","  var D="+data+";\n  function G(name,fb){var v=D[name];return v==null?fb:v}",script)
script=R("  try{if(typeof save!=='undefined'&&save.calm)reduce=true}catch(e){}\n","  var SV=null;try{SV=JSON.parse(localStorage.getItem('lanka_map_v3')||'null')}catch(e){}\n  try{if(SV&&SV.calm)reduce=true}catch(e){}\n",script)
script=R("  var SV=G('save',null);\n","",script)
script=R("PL=G('PLACES',{});","PLA=G('PL',[]);",script)
script=R("function pts(){return Object.keys(PL).map(function(k){return [PL[k].la,PL[k].lo]}).filter(function(p){return p[0]&&p[1]})}","function pts(){return PLA.filter(function(p){return p[0]&&p[1]})}",script)
script=R("var nPl=Object.keys(PL).length||96;","var nPl=PLA.length||96;",script)
script=R('<button class="gi-start" type="button" data-go><span class="gi-tri" aria-hidden="true"></span><span class="gi-lbl">\'+($(\'.gi-lbl\').textContent)+\'</span></button>','<a class="gi-start" href="/lanka_ki_khoj/" data-go><span class="gi-tri" aria-hidden="true"></span><span class="gi-lbl">\'+($(\'.gi-lbl\').textContent)+\'</span></a>',script)
script=R("{root:gi,threshold:.2}","{threshold:.2}",script);script=R("{root:gi,threshold:.25}","{threshold:.25}",script)
a=script.index('  function start(){');b=script.index("  $$('[data-go]')")
script=script[:a]+"""  function start(e){
    if(e)e.preventDefault();if(gi.classList.contains('gone'))return;SFX.go();gi.classList.add('gone');
    setTimeout(function(){location.href='/lanka_ki_khoj/'},reduce?0:700);
  }
"""+script[b:]
script=R("(e.target===document.body||e.target===gi)","(e.target===document.body||e.target===document.documentElement)",script)
script=R("  gi.focus&&gi.setAttribute('tabindex','-1');\n","  window.addEventListener('pageshow',function(ev){if(ev.persisted)gi.classList.remove('gone')});\n",script)
m=re.search(r"\bPL\b(?!\")",script.replace("\"PL\"",""));0 and print("PLCHK",m and script.replace("\"PL\"","")[m.start()-80:m.end()+40])
assert 'eval(' not in script
tpl=open('lkpage.tpl').read()
page=tpl.replace('/*STYLE*/',style).replace('<!--BODY-->',body).replace('/*SCRIPT*/',script)
open('../../game/LankaKiKhoj/index.html','w').write(page)
print(len(page),len(re.findall('[–—]',page)))

# ---------- the same intro, living inside the home page's Lanka world ----------
import json,math
D=json.loads(data)
hstyle=style.replace('html,body{margin:0;background:#07131B}\nhtml{scroll-behavior:smooth}\n','')
hstyle+='\n#gi .gi-top{display:none}\n#gi .gi-float{z-index:30}\n.w-lk{background:#07131B}\n.lk-end{background:#07131B;color:#CFE0E6;padding:0 0 70px}\n.lk-end .w-end{margin-top:0;border-top-color:rgba(243,234,211,.15)}\n.lk-direct{color:#FFCA7A;text-decoration:none;font:400 19px/1 var(--deva)}\n.w-lk .allw{color:#CFE0E6}\n'
hbody=body.replace('<h1 class="gi-title" id="giTitle">','<h2 class="gi-title" id="giTitle">').replace('लंका की खोज</h1>','लंका की खोज</h2>')
hstyle=hstyle.replace('h1.gi-title','.gi-title')
hscript=script
hscript=R("document.addEventListener('keydown',function k(e){if(!document.body.contains(gi)){document.removeEventListener('keydown',k);return}",
          "document.addEventListener('keydown',function k(e){if(!gi.offsetParent)return;",hscript)
hscript=hscript.strip()
assert hscript.startswith('(function(){') and hscript.endswith('})();'),hscript[:30]
hscript='window.LKI=function(){'+hscript[len('(function(){'):-len('})();')]+'''
  return {replay:function(){gi.classList.remove('play','shake','gone');hlay();
      if(reduce){t0=performance.now()-9000;gi.classList.add('play');hframe(performance.now());return}
      marks={};trail=[];embers=[];void gi.offsetWidth;t0=performance.now();gi.classList.add('play');if(!raf)raf=requestAnimationFrame(hframe)},
    sound:function(on){son=!!on;if(!ac())return;if(on&&AC.state==='suspended')AC.resume();MG.gain.setTargetAtTime(on?.6:0,AC.currentTime,.2)}};
};'''

# the card: the real coastline at night, a comet on its way, the city awake
W,H=300,380;box=(10.6,77.0,5.7,82.4);k=math.cos(math.radians(8))
s_=max(W/((box[3]-box[1])*k),H/(box[0]-box[2]));cx=(box[1]+box[3])/2;cy=(box[0]+box[2])/2
P=lambda la,lo:(W/2+(lo-cx)*k*s_,H/2+(cy-la)*s_)
def smooth(pts):
    q=[P(a,b) for a,b in pts];n=len(q);m=lambda a,b:((a[0]+b[0])/2,(a[1]+b[1])/2);s0=m(q[-1],q[0]);d='M%.1f %.1f'%s0
    for i in range(n):
        nx=m(q[i],q[(i+1)%n]);d+=' Q%.1f %.1f %.1f %.1f'%(q[i][0],q[i][1],nx[0],nx[1])
    return d+'Z'
city=D['CITY'];cl=(sum(c[0] for c in city)/len(city),sum(c[1] for c in city)/len(city))
a=P(8.38,77.53);b=P(*cl);c=((a[0]+b[0])/2,min(a[1],b[1])-120)
arc='M%.1f %.1f Q%.1f %.1f %.1f %.1f'%(a[0],a[1],c[0],c[1],b[0],b[1])
lights=''
import random;random.seed(7)
for la,lo in D['PL']:
    x,y=P(la,lo)
    if 0<x<W and 0<y<H:
        lights+='<circle cx="%.1f" cy="%.1f" r="1.8" class="lkc-l" style="animation-delay:%.2fs"/>'%(x,y,random.random()*3)
waves=''.join('<path d="M-20 %d q15 -4 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0" fill="none" stroke="#9DC2D4" stroke-opacity=".12"/>'%y for y in range(40,380,46))
card='''<a class="portal p-lk" href="#lanka-ki-khoj" data-w="lk" lang="hi"><span class="p-art"><svg viewBox="0 0 300 380" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
          <defs><linearGradient id="lkcSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1D2A3A"/><stop offset=".5" stop-color="#0B2530"/><stop offset="1" stop-color="#07131B"/></linearGradient>
          <radialGradient id="lkcGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFB24A" stop-opacity=".45"/><stop offset="1" stop-color="#FFB24A" stop-opacity="0"/></radialGradient></defs>
          <rect width="300" height="380" fill="url(#lkcSea)"/>'''+waves+'''
          <path d="'''+smooth(D['COAST_IN'])+'''" fill="#4A4636" stroke="#8F7C50" stroke-width="1.4"/>
          <path d="'''+smooth(D['COAST_LK'])+'''" fill="#4A4636" stroke="#8F7C50" stroke-width="1.4"/>
          <circle cx="%.1f" cy="%.1f" r="60" fill="url(#lkcGlow)" class="lkc-city"/>'''%b+lights+'''
          <path d="'''+arc+'''" fill="none" stroke="#FFCA7A" stroke-opacity=".35" stroke-width="1.4" stroke-dasharray="2 5"/>
          <g class="lkc-comet"><circle r="14" fill="#FFB24A" opacity=".3"/><circle r="4.5" fill="#FFF4DA"/><animateMotion dur="3.4s" repeatCount="indefinite" path="'''+arc+'''" keyPoints="0;1;1" keyTimes="0;.62;1" calcMode="spline" keySplines=".45 0 .55 1;0 0 1 1"/></g>
          </svg></span>
        <span class="p-txt"><span class="p-tag">खेल · हिंदी में</span><span class="p-title">लंका की खोज</span><span class="p-go">अंदर चलिए →</span></span></a>'''
cardcss='''.p-lk{--g:255,170,80;background:#07131B}
.p-lk .p-title{font:400 clamp(28px,2.8vw,38px)/1.1 var(--devdisp);color:#FFF4DA;text-shadow:0 0 14px rgba(255,160,60,.6),0 0 40px rgba(201,73,47,.55),0 3px 0 #6B2A14}
.p-lk .p-tag{color:#FFCA7A!important}
.p-lk svg{position:absolute;inset:0;width:100%;height:100%}
.lkc-l{fill:#FFE3A1;animation:lkcTw 2.6s ease-in-out infinite}
@keyframes lkcTw{50%{opacity:.25}}
.lkc-city{animation:lkcCity 3.4s ease-in-out infinite}
@keyframes lkcCity{0%,58%{opacity:.4}66%{opacity:1}100%{opacity:.4}}
.lkc-comet{filter:drop-shadow(0 0 6px #FFB24A)}
.p-lk .p-tag,.p-jn .p-tag,.p-nn .p-tag{font-family:var(--deva);letter-spacing:.02em;font-size:14px}
@media (prefers-reduced-motion:reduce){.lkc-l,.lkc-city{animation:none}.lkc-comet{display:none}}
'''
hp='../../index.html';h=open(hp).read()
def slot(h,a,b,new):
    i=h.index(a)+len(a);j=h.index(b,i);return h[:i]+'\n'+new+'\n'+h[j:]
h=slot(h,'/* lk-card css */','/* lk-card css end */',cardcss)
h=slot(h,'/* lk-world css */','/* lk-world css end */',hstyle)
h=slot(h,'<!-- lk-card -->','<!-- lk-card end -->',card)
h=slot(h,'<!-- lk-world -->','<!-- lk-world end -->',hbody)
h=slot(h,'<!-- lk-world script -->','<!-- lk-world script end -->','<script>\n'+hscript+'\n</script>')
open(hp,'w').write(h)
open('/tmp/lki.js','w').write(hscript)
print('home',len(h),len(re.findall('[–—]',h)))
