# missions of all three sizes, boons, the little games, the questions, badges, and saving
import json
from playwright.sync_api import sync_playwright
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
ok=[];bad=[]
def wait_for(pg,js,tries=16,gap=400):
    for i in range(tries):
        if pg.evaluate(js): return True
        pg.wait_for_timeout(gap)
    return False
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':390,'height':844})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(1300)
    pg.evaluate("""()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());
      save.role='jigyasu';save.rolePicked=true;roleTint();start('khoj');}""")
    pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
    pg.wait_for_timeout(600)

    # 1. the three sizes of mission exist and know their goals
    m=pg.evaluate("""()=>{const n=muhimNow();const out={};
      ['ghadi','raat','safar'].forEach(k=>{const id=n[k];out[k]=id?{n:MUHIM[id].n,goal:MUHIM[id].goal,have:mcount(id)}:null;});
      return out;}""")
    for k in ['ghadi','raat','safar']:
        if not m.get(k): bad.append('no %s mission is running'%k)
        else: ok.append('मुहिम %s: %s %d/%d'%(k,m[k]['n'],m[k]['have'],m[k]['goal']))

    # 2. a mission counts up as the player plays
    before=pg.evaluate("()=>{const n=muhimNow();return n.ghadi?mcount(n.ghadi):0;}")
    pg.evaluate("()=>{visit(ghadiSpots()[0]);}")
    pg.wait_for_timeout(1400)
    after=pg.evaluate("()=>{const n=muhimNow();return n.ghadi?mcount(n.ghadi):0;}")
    if after<=before: bad.append('the watch mission does not count what the player does')
    else: ok.append('मुहिम गिनती बढ़ी: %d से %d'%(before,after))

    # 3. the boons actually change the game
    v1=pg.evaluate("()=>visitsHere()")
    pg.evaluate("()=>{save.muhim=save.muhim||{done:{},boon:{}};save.muhim.boon.extra=1;persist();}")
    v2=pg.evaluate("()=>visitsHere()")
    if v2<=v1: bad.append('the extra visit boon gives nothing')
    else: ok.append('हक़ काम करता है: जगहें %d से %d'%(v1,v2))
    pg.evaluate("()=>{save.muhim.boon.diya=1;save.diyaUsed=null;persist();}")
    if not pg.evaluate("()=>typeof diyaLeft==='function'&&diyaLeft()"): bad.append('the lamp boon is not available after it is won')
    else: ok.append('दीया वाला हक़: जलाने लायक')

    # 4. the little games
    games=pg.evaluate("""()=>['khelChalang','khelChhat','khelChhaya','khelDiya'].filter(k=>typeof window[k]==='function'||typeof eval(k)==='function');""")
    if len(games)<4: bad.append('only %d of the four little games are there'%len(games))
    else: ok.append('छोटे खेल: चारों मौजूद')
    pg.evaluate("()=>{try{khelDiya();}catch(e){window.__gerr=String(e);}}")
    pg.wait_for_timeout(1500)
    if pg.evaluate("()=>!!window.__gerr"): bad.append('a little game fails to open: '+str(pg.evaluate("()=>window.__gerr")))
    else: ok.append('दीयों वाला खेल: खुलता है')
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
    pg.wait_for_timeout(700)

    # 5. the five questions: the box it builds, and an answer given
    pg.evaluate("()=>{try{nightQuiz(run.N,5);}catch(e){window.__q=String(e);}}")
    pg.wait_for_timeout(1400)
    q=pg.evaluate("()=>{const x=document.getElementById('nq');return x?{t:x.innerText.slice(0,60),n:x.querySelectorAll('button').length}:null;}")
    if not q or q['n']<2: bad.append('the five questions build nothing to answer')
    else:
        ok.append('पाँच सवाल: %d जवाब सामने'%q['n'])
        pg.evaluate("()=>{const x=document.getElementById('nq');const b=x&&x.querySelector('button');if(b)b.click();}")
        pg.wait_for_timeout(900)
        said=pg.evaluate("()=>{const x=document.getElementById('nq');return x?x.innerText.slice(0,40):''}")
        if 'सही' not in said and 'ठीक' not in said: bad.append('answering a question says nothing back')
        else: ok.append('जवाब देने पर: '+said.split('\n')[0][:36])

    # 5b. the task that lasts a real day
    d=pg.evaluate("()=>{const M=dinMuhim();return {n:M.n,goal:M.goal,have:dinCount(),mani:M.mani};}")
    if not d or not d['n']: bad.append('there is no task for the day')
    else: ok.append('आज की मुहिम: %s %d/%d, +%d मणि'%(d['n'],d['have'],d['goal'],d['mani']))
    mani=pg.evaluate("()=>purse()")
    pg.evaluate("()=>{const M=dinMuhim();for(let i=0;i<M.goal+1;i++)dinTick(M.count);}")
    pg.wait_for_timeout(1200)
    if not pg.evaluate("()=>!!(save.din&&save.din.done)"): bad.append('the day task never finishes')
    elif pg.evaluate("()=>purse()")<=mani: bad.append('the day task pays nothing')
    else: ok.append('आज की मुहिम पूरी: मणि %d से %d'%(mani,pg.evaluate("()=>purse()")))
    seven=pg.evaluate("""()=>{const s=new Set();
      for(let k=0;k<7;k++){const d=new Date(Date.now()+k*86400000);
        const key=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
        const t=Math.floor(Date.parse(key+'T00:00:00')/86400000);
        s.add(((t%DIN.length)+DIN.length)%DIN.length);}
      return s.size;}""")
    if seven<7: bad.append('the day task repeats inside a week (%d different in seven days)'%seven)
    else: ok.append('सात दिन, सात अलग मुहिमें')
    # the run of days: it grows one a day, and a missed day breaks it
    r=pg.evaluate("""()=>{const day=n=>{const d=new Date(Date.now()+n*86400000);
        return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
      const out={};out.one=save.din.run;
      save.din.day=day(-1);persist();dinState();let M=dinMuhim();for(let i=0;i<M.goal;i++)dinTick(M.count);
      out.two=save.din.run;
      save.din.day=day(-3);save.din.done=false;persist();dinState();
      out.broken=save.din.run;out.best=save.din.best;return out;}""")
    if r['two']!=r['one']+1: bad.append('the run of days does not grow by one a day')
    elif r['broken']!=0: bad.append('a missed day does not break the run')
    elif r['best']<r['two']: bad.append('the longest run is not remembered')
    else: ok.append('लगातार दिन: %d, फिर %d, छूटने पर 0, सबसे लंबा %d'%(r['one'],r['two'],r['best']))
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
    pg.wait_for_timeout(700)

    # 6. badges and titles counted
    b=pg.evaluate("()=>({badges:Object.keys(ACH).length,titles:(typeof PADVI!=='undefined')?Object.keys(PADVI).length:0,mani:purse()})")
    ok.append('बैज %d, पदवियाँ %d, मणि %d'%(b['badges'],b['titles'],b['mani']))

    # 7. what is saved comes back
    pg.evaluate("()=>{save.cards['sita_raat']=1;persist();}")
    pg.reload(); pg.wait_for_timeout(1600)
    kept=pg.evaluate("()=>!!(save.cards&&save.cards['sita_raat'])")
    if not kept: bad.append('what was found is lost when the page is opened again')
    else: ok.append('सहेजना: पन्ना दोबारा खोलने पर बात बची रही')
    br.close()
print(json.dumps({'ok':ok,'issues':bad,'errors':errs[:4]},ensure_ascii=False,indent=1))
