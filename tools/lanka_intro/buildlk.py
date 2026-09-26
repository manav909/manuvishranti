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
m=re.search(r"\bPL\b(?!\")",script.replace("\"PL\"",""));print("PLCHK",m and script.replace("\"PL\"","")[m.start()-80:m.end()+40])
assert 'eval(' not in script
tpl=open('lkpage.tpl').read()
page=tpl.replace('/*STYLE*/',style).replace('<!--BODY-->',body).replace('/*SCRIPT*/',script)
open('/home/claude/manuvishranti/game/LankaKiKhoj/index.html','w').write(page)
open('lkpage.js','w').write(script)
print(len(page),len(re.findall('[–—]',page)))
