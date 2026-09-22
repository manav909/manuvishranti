import json, sys, collections
from playwright.sync_api import sync_playwright
URL='file:///mnt/user-data/outputs/lanka-map3.html'
view=sys.argv[1] if len(sys.argv)>1 else 'phone'
W,H={'phone':(390,844),'tablet':(820,1180),'desktop':(1366,820)}[view]
role=sys.argv[2] if len(sys.argv)>2 else None
issues=[]; errs=[]; log=[]
def issue(kind,msg,where): issues.append({'kind':kind,'msg':msg,'where':where})
# what a player can see and press right now
VISIBLE_BTNS="""()=>{const out=[];document.querySelectorAll('button').forEach((b,i)=>{
  const r=b.getBoundingClientRect();const cs=getComputedStyle(b);
  if(r.width<2||r.height<2||cs.visibility==='hidden'||cs.display==='none')return;
  let hid=false;for(let n=b;n;n=n.parentElement){const s=getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden'){hid=true;break;}}
  if(hid)return;
  // is something else painted on top of its centre?
  const cx=r.left+r.width/2, cy=r.top+r.height/2; let covered=false, by='';
  // only a button its own scrolling box is showing can be covered by something else
  var shown=cx>0&&cy>0&&cx<innerWidth&&cy<innerHeight;
  for(let n=b.parentElement;n&&shown;n=n.parentElement){const s=getComputedStyle(n);
    if(/(auto|scroll|hidden)/.test(s.overflowY+s.overflowX)){const q=n.getBoundingClientRect();
      if(cy<q.top||cy>q.bottom||cx<q.left||cx>q.right)shown=false;}}
  if(shown){const t=document.elementFromPoint(cx,cy);if(t&&t!==b&&!b.contains(t)){covered=true;by=(t.className&&String(t.className))||t.tagName;}}
  out.push({i,t:(b.textContent||b.getAttribute('aria-label')||'').trim().slice(0,50),cls:String(b.className),x:Math.round(cx),y:Math.round(cy),inView:shown,covered,by:String(by).slice(0,30)});});return out;}"""
def screen_name(pg):
    return pg.evaluate("()=>{const h=document.querySelector('#story h1, #story h2');return (h?h.textContent:'').trim().slice(0,30)}")
def click_btn(pg, b):
    loc=pg.locator('button').nth(b['i'])
    try:
        pg.wait_for_timeout(450); loc.scroll_into_view_if_needed(timeout=4000); loc.click(timeout=5000)
        pg.wait_for_timeout(260); return True
    except Exception as e:
        diag=pg.evaluate('''i=>{const b=document.querySelectorAll('button')[i];if(!b)return 'gone';const r=b.getBoundingClientRect();
          const par=[];for(let a=b;a&&par.length<7;a=a.parentElement){const c=getComputedStyle(a);if(c.animationName!=='none'||c.transform!=='none'||c.position!=='static')par.push(String(a.id||a.className).slice(0,14)+':'+c.animationName+'/'+c.animationIterationCount+'/'+c.position+'/'+c.transform.slice(0,14));}
          const sc=[];for(let a=b.parentElement;a;a=a.parentElement){const c=getComputedStyle(a);if(/(auto|scroll)/.test(c.overflowY))sc.push(String(a.id||a.className).slice(0,14)+' h='+Math.round(a.clientHeight)+' sh='+Math.round(a.scrollHeight));}
          const st=document.getElementById('story');const q=st.getBoundingClientRect();
          return {r:[Math.round(r.top),Math.round(r.height)],story:[Math.round(q.top),Math.round(q.bottom)],top:st.scrollTop,par,sc};}''',b['i'])
        # does the page let a player scroll down to it, or does it snap back?
        pg.evaluate("()=>{const st=document.getElementById('story');st.scrollTop=st.scrollHeight;}")
        pg.wait_for_timeout(700)
        diag['after_scroll']=pg.evaluate("()=>{const st=document.getElementById('story');return [st.scrollTop,st.scrollHeight-st.clientHeight]}")
        diag['on_top']=pg.evaluate('''i=>{const b=document.querySelectorAll('button')[i];if(!b)return 'gone';const r=b.getBoundingClientRect();
          return [[.5,.5],[.1,.5],[.9,.5]].map(([fx,fy])=>{const x=r.left+r.width*fx,y=r.top+r.height*fy;const t=document.elementFromPoint(x,y);
            if(!t)return 'nothing at '+Math.round(x)+','+Math.round(y);if(t===b||b.contains(t))return 'self';
            const c=getComputedStyle(t);return (t.id||'')+'.'+String(t.className).slice(0,20)+' pos='+c.position+' z='+c.zIndex+' op='+c.opacity+' pe='+c.pointerEvents;});}''',b['i'])
        diag['box']=pg.evaluate('''i=>{const b=document.querySelectorAll('button')[i];const r=b.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height),innerWidth,innerHeight]}''',b['i'])
        # a player's finger does not care about automation rules: press where the button is painted
        if isinstance(diag,dict) and diag.get('on_top')==['self','self','self']:
            x,y,w,h=diag['box'][:4]
            before=pg.evaluate("()=>document.getElementById('story').innerText.length")
            pg.mouse.click(x+w/2,y+h/2); pg.wait_for_timeout(500)
            after=pg.evaluate("()=>document.getElementById('story').innerText.length")
            if after!=before:
                log.append(f"'{b['t'][:25]}' worked by a finger press (automation quirk only)"); return True
            issue('no-effect',f"'{b['t']}' is on top and in view, but pressing it does nothing",screen_name(pg)); return False
        issue('click-failed',f"'{b['t']}' ({b['cls']}) could not be pressed: {json.dumps(diag,ensure_ascii=False)[:500]}",screen_name(pg)); return False
PRIORITY=[('कथा आगे चलती है',None),(None,'card-pick'),('वक़्त आगे',None),('आगे',None),('do go',None)]
def pick_forward(btns):
    def has(b,t=None,c=None): return (t is None or t in b['t']) and (c is None or c in b['cls'])
    for t,c in [('कथा आगे चलती है',None),(None,'card-pick'),('वक़्त आगे',None)]:
        for b in btns:
            if has(b,t,c): return b
    for b in btns:
        if 'do go' in b['cls'] or 'go' in b['cls'].split(): return b
    return None
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx=br.new_context(viewport={'width':W,'height':H},has_touch=(view=='phone'))
    pg=ctx.new_page()
    pg.on('pageerror',lambda e: errs.append(str(e)[:200]))
    pg.goto(URL); pg.wait_for_timeout(700)
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}"); pg.reload(); pg.wait_for_timeout(700)
    # 1. the very first screen must offer a way in
    btns=pg.evaluate(VISIBLE_BTNS)
    if not btns: issue('dead-end','the first screen has no button at all','शुरुआत')
    # 2. pick a role the way a player would: tap its card, then the button that confirms it
    cards=[b for b in btns if 'rolecard' in b['cls'] or 'role' in b['cls']]
    target=None
    if role:
        target=next((b for b in btns if role in b['t']),None)
    target=target or (cards[0] if cards else None)
    if not target: issue('dead-end','no role card to press on the first screen','भूमिका चुनना')
    else:
        click_btn(pg,target)
        btns=pg.evaluate(VISIBLE_BTNS)
        go=next((b for b in btns if 'चलो' in b['t'] or 'चुनो' in b['t'] or 'do go' in b['cls']),None)
        if not go: issue('dead-end','a role page with no way to pick it','भूमिका का पन्ना')
        else:
            if go['covered']: issue('covered',f"'{go['t']}' is under {go['by']}",'भूमिका का पन्ना')
            click_btn(pg,go)
    # 3. play the first night, only by pressing what is on screen
    btns=pg.evaluate(VISIBLE_BTNS)
    night=next((b for b in btns if 'रात' in b['t'] and 'do go' in b['cls']),None) or next((b for b in btns if 'do go' in b['cls']),None)
    if not night: issue('dead-end','the nights screen has nothing to start','रातें')
    else: click_btn(pg,night)
    steps=0; seen_dawn=False; last=''; nightlog={}
    while steps<60:
        steps+=1
        btns=pg.evaluate(VISIBLE_BTNS)
        for b in btns:
            if b['inView'] and b['covered'] and b['by'] not in ('',):
                issue('covered',f"'{b['t'][:30]}' ({b['cls'][:20]}) sits under {b['by']}",screen_name(pg))
        st=pg.evaluate("()=>{try{return run?{n:run.N.id||'',w:run.w,W:run.N.watches.length}:{n:'',w:0,W:0}}catch(e){return {n:'',w:0,W:0}}}")
        nightlog.setdefault(st['n'],{'max_w':0,'W':st['W'],'presses':0})
        nightlog[st['n']]['max_w']=max(nightlog[st['n']]['max_w'],st['w']); nightlog[st['n']]['presses']+=1
        if st['W'] and st['w']>=st['W']: seen_dawn=True
        if len([k for k in nightlog if k])>1: seen_dawn=True
        fw=pick_forward(btns)
        if not fw:
            if not seen_dawn: issue('dead-end','nothing to press forward, and the night is not over',screen_name(pg))
            break
        # the forward button must be reachable without hunting: in view, or in the sticky bar
        if not fw['inView']:
            sticky=pg.evaluate("i=>{const b=document.querySelectorAll('button')[i];return !!(b&&b.closest('.actbar'))}",fw['i'])
            if not sticky: log.append(f"forward '{fw['t'][:25]}' is below the fold")
        key=fw['t']+fw['cls']
        before=pg.evaluate("()=>document.getElementById('story').innerText.length")
        click_btn(pg,fw)
        after=pg.evaluate("()=>document.getElementById('story').innerText.length")
        if after==before and key==last: issue('no-effect',f"pressing '{fw['t'][:30]}' changes nothing",screen_name(pg))
        last=key
        if 'वक़्त आगे' in fw['t'] or 'दूसरी घड़ी' in fw['t']: pass
        if pg.evaluate("()=>!run"): break
    if not seen_dawn: issue('never-ends','the night did not reach its morning in 60 presses',screen_name(pg))
    # 4. the side panels open and close by their own buttons
    for label in ['पोथी','पत्र']:
        btns=pg.evaluate(VISIBLE_BTNS)
        b=next((x for x in btns if label in x['t']),None)
        if not b: issue('missing',f"no '{label}' button on screen",'सुबह')
        else:
            click_btn(pg,b)
            btns2=pg.evaluate(VISIBLE_BTNS)
            ids=pg.evaluate("()=>[...document.querySelectorAll('button')].map(b=>b.id)")
            close=next((x for x in btns2 if ids[x['i']] in ('pcardShut','scrollShut','deepShut')),None) or next((x for x in btns2 if x['t']=='कथा' or 'वापस' in x['t']),None)
            if not close: issue('trap',f"'{label}' opens but offers no visible way back",label)
            else: click_btn(pg,close)
    br.close()
print(json.dumps({'view':view,'role':role,'steps':steps,'nights':nightlog,'issues':issues,'errors':errs,'log':log[:8]},ensure_ascii=False,indent=1))
