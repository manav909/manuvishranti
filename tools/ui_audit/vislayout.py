import sys, json
from playwright.sync_api import sync_playwright
VIEW={'phone':(390,844),'tablet':(820,1180),'desktop':(1200,860)}[sys.argv[1] if len(sys.argv)>1 else 'phone']
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
bad=[]; log=[]
def note(where,msg): bad.append({'where':where,'msg':msg})

MEASURE = """() => {
  const host=document.getElementById('bigshow');
  if(!host||host.hidden) return {none:true};
  const card=host.querySelector('.bcard');
  const out={bits:[],card:null,small:[],tiny:[],over:[],wide:[],touch:[]};
  const cr=card.getBoundingClientRect();
  out.card=[Math.round(cr.left),Math.round(cr.top),Math.round(cr.width),Math.round(cr.height)];
  const vis=[...card.querySelectorAll('button, canvas, p, b, span, h2, div.leafstrip, div.minimapbox')]
    .filter(e=>{const r=e.getBoundingClientRect();
      if(r.width<4||r.height<4) return false;
      const cs=getComputedStyle(e);
      if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<.1) return false;
      if(e.closest('.srlist')) return false;
      return true;});
  /* text too small, or buttons too small to press */
  vis.forEach(e=>{const cs=getComputedStyle(e),r=e.getBoundingClientRect();
    const fs=parseFloat(cs.fontSize)||0;
    const txt=(e.textContent||'').trim();
    if(txt && e.children.length===0 && fs<12.5) out.tiny.push([txt.slice(0,24),Math.round(fs)]);
    if(e.tagName==='BUTTON' && r.height<34) out.small.push([txt.slice(0,20),Math.round(r.height)]);
    if(r.right>cr.right+2||r.left<cr.left-2) out.bits.push(['बाहर निकला',txt.slice(0,20)]);
  });
  /* a line of reading must not run too wide for the eye */
  vis.forEach(e=>{
    if(e.children.length)return;
    const txt=(e.textContent||'').trim();
    if(txt.length<40)return;
    const cs=getComputedStyle(e),r=e.getBoundingClientRect();
    const fs=parseFloat(cs.fontSize)||16;
    const perLine=r.width/(fs*0.52);            /* roughly how many letters fit on one line */
    if(perLine>92) out.wide.push([txt.slice(0,24),Math.round(perLine)]);
  });
  /* the compartments must not touch each other */
  const boxes=[...card.querySelectorAll('.dcanvas, .minimapbox, .leafstrip, .dbar')]
    .filter(e=>{const r=e.getBoundingClientRect();return r.width>4&&r.height>4;});
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
    if(boxes[i].contains(boxes[j])||boxes[j].contains(boxes[i]))continue;
    const a2=boxes[i].getBoundingClientRect(),b2=boxes[j].getBoundingClientRect();
    const ox=Math.min(a2.right,b2.right)-Math.max(a2.left,b2.left);
    const oy=Math.min(a2.bottom,b2.bottom)-Math.max(a2.top,b2.top);
    if(ox>0&&oy>0) out.touch.push([boxes[i].className.slice(0,16),boxes[j].className.slice(0,16)]);
    else if(ox>-6&&oy>-6&&(ox>0||oy>0)) out.touch.push(['बहुत पास',boxes[i].className.slice(0,14)+' / '+boxes[j].className.slice(0,14)]);
  }
  /* two pieces of text sitting on top of each other */
  const leaves=vis.filter(e=>e.children.length===0&&(e.textContent||'').trim().length>2);
  for(let i=0;i<leaves.length;i++)for(let j=i+1;j<leaves.length;j++){
    const a=leaves[i].getBoundingClientRect(),b=leaves[j].getBoundingClientRect();
    if(leaves[i].contains(leaves[j])||leaves[j].contains(leaves[i]))continue;
    const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    const oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if(ox>6&&oy>6) out.over.push([(leaves[i].textContent||'').trim().slice(0,18),(leaves[j].textContent||'').trim().slice(0,18)]);
  }
  return out;
}"""

def wait_for(pg,js,tries=20,gap=500):
    for i in range(tries):
        if pg.evaluate(js): return True
        pg.wait_for_timeout(gap)
    return False

with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':VIEW[0],'height':VIEW[1]})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(1200)

    screens=[]
    def settled(pg):
        # the card lands with a small bounce: measure only once it has come to rest
        return pg.evaluate("""()=>{const c=document.querySelector('#bigshow .bcard');
          if(!c)return false;const t=getComputedStyle(c).transform;
          return t==='none'||t==='matrix(1, 0, 0, 1, 0, 0)';}""")

    def grab(name):
        pg.wait_for_timeout(900)
        for i in range(12):
            if settled(pg): break
            pg.wait_for_timeout(250)
        m=pg.evaluate(MEASURE)
        if m.get('none'): note(name,'this screen did not open'); return
        for t in m['tiny']: note(name,'too small to read: "%s" at %dpx'%(t[0],t[1]))
        for s2 in m['small']: note(name,'button too small to press: "%s" %dpx tall'%(s2[0],s2[1]))
        for b in m['bits']: note(name,'%s: "%s"'%(b[0],b[1]))
        for o in m['over']: note(name,'these two sit on top of each other: "%s" / "%s"'%(o[0],o[1]))
        for w in m['wide']: note(name,'a line runs too wide to read: "%s" about %d letters a line'%(w[0],w[1]))
        for t2 in m['touch']: note(name,'these two compartments touch: %s / %s'%(t2[0],t2[1]))
        log.append(name+': ok')
    def clear():
        pg.evaluate("()=>{const x=document.getElementById('bigshow');if(x){x.hidden=true;x.innerHTML='';}}")
        pg.wait_for_timeout(400)

    # भूमिकाएँ
    # the pictures open only when asked for, so ask each time
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());persist();roleScreen();}")
    pg.wait_for_timeout(1000); pg.evaluate("()=>{bhumikaDikhao();}")
    wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"); grab('भूमिकाएँ'); clear()
    # रातें
    pg.evaluate("""()=>{Object.assign(save,blankSave());save.role='yatri';save.rolePicked=true;roleTint();
      save.nights={khoj:1};persist();front();}""")
    pg.wait_for_timeout(900); pg.evaluate("()=>{raateinDikhao();}")
    wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"); grab('रातें'); clear()
    # दरवाज़े
    pg.evaluate("()=>{start('khoj');}")
    wait_for(pg,"()=>!!document.querySelector('#bigshow .bshut')")
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
    pg.wait_for_timeout(900); pg.evaluate("()=>{darwazeDikhao(ghadiSpots());}")
    wait_for(pg,"()=>!!document.querySelector('.dcanvas')"); grab('दरवाज़े'); clear()
    # भीतर
    pg.evaluate("()=>{visit(ghadiSpots()[0]);}")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const w=autoDrishya;autoDrishya=true;andarDikhao(run.hereId);autoDrishya=w;}")
    wait_for(pg,"()=>!!document.querySelector('.leafstrip')"); grab('भीतर'); clear()
    if VIEW[0]<600 and len(sys.argv)<3:   # the last two only on a phone: the big scenes are slow to build here
      # पोथियाँ
      pg.evaluate("()=>{if(run.hereOthers&&run.hereOthers.length)pothiDikhao(run.hereId,run.w,run.hereOthers,run.hereKey);}")
      wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"); grab('पोथियाँ'); clear()
      pg.evaluate("()=>{const bk=[...story.querySelectorAll('.basket')].pop();if(bk)thaalDikhao(bk);}")
      wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"); grab('थाल'); clear()
    br.close()

print(json.dumps({'issues':bad,'ok':log,'view':sys.argv[1] if len(sys.argv)>1 else 'phone'},ensure_ascii=False,indent=1))
