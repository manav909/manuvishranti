import json, sys
from playwright.sync_api import sync_playwright
URL='file:///mnt/user-data/outputs/lanka-map3.html'
view=sys.argv[1] if len(sys.argv)>1 else 'phone'
which=sys.argv[2].split(',') if len(sys.argv)>2 else None
W,H={'phone':(390,844),'tablet':(820,1180),'desktop':(1366,820)}[view]
SCREENS={
 'roles':  "()=>{roleScreen();}",
 'front':  "()=>{front();}",
 'night':  "()=>{start('khoj');}",
 'moment': "()=>{start('khoj');run.busy=false;visit(mainList(run.w)[0]);}",
 'offer':  "()=>{start('khoj');run.busy=false;visit(mainList(run.w)[0]);run.busy=false;run.ghadi=1;run.used=0;offer();}",
 'dawn':   "()=>{start('khoj');run.w=run.N.watches.length;run.busy=false;turn();}",
 'pothi':  "()=>{start('khoj');showPanel('pothi');}",
 'card':   "()=>{start('khoj');openCard();}",
 'help':   "()=>{start('khoj');helpPanel();}",
}
SETUP="""()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());save.role='jigyasu';save.rolePicked=true;
 save.nights.khoj=1;save.done.khoj=1;roleTint();}"""
# a fingerprint of what the player sees, to tell whether a press did anything
SIG="""()=>{const v=[...document.querySelectorAll('#story,#pothi,#pcard,#deep,#dio,#mini,#bar,#stage')].map(e=>{const r=e.getBoundingClientRect();
 return (e.id||'')+':'+getComputedStyle(e).display+':'+e.className+':'+Math.round(r.height)+':'+(e.innerText||'').length+':'+(e.scrollTop||0);}).join('|');
 const m=document.querySelector('#stage svg');return v+'|'+(m?m.getAttribute('viewBox'):'')+'|'+document.activeElement.tagName;}"""
LIST="""()=>[...document.querySelectorAll('button')].map((b,i)=>{const r=b.getBoundingClientRect();const cs=getComputedStyle(b);
 let hid=r.width<2||r.height<2;for(let n=b;n&&!hid;n=n.parentElement){const s=getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden')hid=true;}
 return {i,t:(b.textContent||b.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,40),id:b.id,cls:String(b.className).slice(0,30),hid,dis:b.disabled};}).filter(b=>!b.hid&&!b.dis)"""
issues=[]; tested=0; covered=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx=br.new_context(viewport={'width':W,'height':H})
    pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)[:160]))
    pg.goto(URL); pg.wait_for_timeout(700)
    for name,go in SCREENS.items():
        if which and name not in which: continue
        pg.evaluate(SETUP); pg.evaluate(go); pg.wait_for_timeout(350)
        btns=pg.evaluate(LIST)
        for b in btns[:40]:
            pg.evaluate(SETUP); pg.evaluate(go); pg.wait_for_timeout(250)
            cur=pg.evaluate(LIST)
            tgt=next((x for x in cur if x['t']==b['t'] and x['cls']==b['cls']),None)
            if not tgt: continue
            before=pg.evaluate(SIG); e0=len(errs)
            try:
                L=pg.locator('button').nth(tgt['i'])
                top=pg.evaluate('''i=>{const b=document.querySelectorAll('button')[i];b.scrollIntoView({block:'center'});
                  const r=b.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
                  return !t?'none':(t===b||b.contains(t))?'self':((t.id||'')+'.'+String(t.className).slice(0,24));}''',tgt['i'])
                pg.wait_for_timeout(150)
                if top!='self':
                    covered.append({'screen':name,'btn':b['t'],'under':top}); continue
                L.click(timeout=2500,force=True)
            except Exception as ex:
                issues.append({'screen':name,'kind':'unpressable','btn':b['t'],'cls':b['cls'],'msg':str(ex)[:120]}); continue
            pg.wait_for_timeout(450); tested+=1
            after=pg.evaluate(SIG)
            if len(errs)>e0: issues.append({'screen':name,'kind':'error','btn':b['t'],'cls':b['cls'],'msg':errs[-1]})
            elif after==before:
                already=' on' in (' '+b['cls']+' ')
                issues.append({'screen':name,'kind':'already-on' if already else 'nothing-happens','btn':b['t'],'cls':b['cls']})
    br.close()
print(json.dumps({'view':view,'tested':tested,'covered':covered,'issues':issues},ensure_ascii=False,indent=1))
