# the whole journey, from the first screen to standing inside a place
import sys, json
from playwright.sync_api import sync_playwright
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
steps=[]; bad=[]
def wait_for(pg,js,tries=20,gap=500):
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
    title=lambda: pg.evaluate("()=>{const t=document.querySelector('#bigshow .btitle');return t?t.textContent:''}")
    # 1. भूमिका
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());persist();roleScreen();}")
    pg.wait_for_timeout(1200)
    # the pictures open only when asked, so ask
    pg.evaluate("()=>{const d=document.getElementById('drishyaBtn');if(d)d.click();}")
    if not wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"): bad.append('the roles never came')
    else: steps.append('भूमिकाएँ: '+title())
    pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const bs=[...document.querySelectorAll('#bigshow .srlist button')];if(bs.length>1)bs[1].click();}")
    # 2. रातें
    if not wait_for(pg,"()=>{const t=document.querySelector('#bigshow .btitle');return t&&t.textContent.indexOf('कहाँ से शुरू')>-1;}",tries=22):
        bad.append('picking a role did not lead to the nights')
    else: steps.append('रातें: '+title()+' | भूमिका '+pg.evaluate("()=>save.role"))
    pg.wait_for_timeout(1000)
    pg.evaluate("""()=>{const b=document.querySelector('#bigshow .srlist button');if(b){b.click();return;}
      const x=document.getElementById('bigshow');if(x&&!x.hidden){const c=x.querySelector('.bshut');if(c)c.click();}}""")
    pg.wait_for_timeout(1800)
    if not pg.evaluate("()=>!!run"):
        pg.evaluate("""()=>{const b=[...document.querySelectorAll('#story button')]
          .find(x=>/शुरू करो|पहली रात/.test(x.textContent||''));if(b)b.click();}""")
        pg.wait_for_timeout(1600)
    # 2b. the one button that opens the picture for where you stand
    pg.evaluate("()=>{const b=document.getElementById('bigshow');if(b&&!b.hidden){const c=b.querySelector('.bshut');if(c)c.click();}}")
    pg.wait_for_timeout(700)
    # 3. रात का परदा या सीधे दरवाज़े
    if not wait_for(pg,"()=>!!run",tries=20): bad.append('the night never began')
    else: steps.append('रात शुरू: '+pg.evaluate("()=>run?run.N.name:'-'"))
    # the night opens with its own card: let it come, close it, and only then ask for the doors
    pg.wait_for_timeout(2500)
    for i in range(6):
        if pg.evaluate("()=>{const b=document.getElementById('bigshow');return !b||b.hidden;}"): break
        pg.evaluate("()=>{const c=document.querySelector('#bigshow .bshut');if(c)c.click();}")
        pg.wait_for_timeout(900)
    pg.evaluate("()=>{const d=document.getElementById('drishyaBtn');if(d)d.click();}")
    wait_for(pg,"()=>!!document.querySelector('.dcanvas')&&/दरवाज़ा/.test((document.querySelector('#bigshow .btitle')||{}).textContent||'')",tries=16)
    if pg.evaluate("()=>!!document.querySelector('.dcanvas')"): steps.append('दरवाज़े: '+title())
    else: bad.append('the doors never came')
    # 4. भीतर
    pg.wait_for_timeout(1800)
    # the night opens with its own card: close whatever stands in front, then ask for the doors
    for i in range(8):
        if pg.evaluate("()=>{const t=document.querySelector('#bigshow .btitle');return !!(t&&/दरवाज़ा/.test(t.textContent));}"): break
        pg.evaluate("""()=>{const b=document.getElementById('bigshow');
          if(b&&!b.hidden){const c=b.querySelector('.bshut');if(c){c.click();return;}}
          const d=document.getElementById('drishyaBtn');if(d)d.click();}""")
        pg.wait_for_timeout(1300)
    wait_for(pg,"()=>!!document.querySelector('#bigshow .srlist button')",tries=14)
    pg.wait_for_timeout(1500)
    pressed=pg.evaluate("""()=>{const b=document.querySelector('#bigshow .srlist button');if(!b)return false;b.click();return b.textContent.slice(0,18);}""")
    if not pressed:
        bad.append('the doors offer no way to choose one; on screen: '+str(pg.evaluate(
          "()=>{const b=document.getElementById('bigshow');const t=document.querySelector('#bigshow .btitle');"
          "return {परदा:(b&&!b.hidden)?'खुला':'बंद',नाम:t?t.textContent:'-',सूची:document.querySelectorAll('#bigshow .srlist button').length};}")))
    pg.wait_for_timeout(1200)
    landed=wait_for(pg,"""()=>{const inside=!!document.querySelector('.leafstrip');
      const onpage=(typeof run!=='undefined'&&run&&run.hereId&&document.querySelectorAll('#story button.do.read').length>0);
      return inside||onpage;}""",tries=40,gap=400)
    if not landed: bad.append('walking through the door did not lead anywhere')
    else:
        inside=pg.evaluate("()=>!!document.querySelector('.leafstrip')")
        where=pg.evaluate("()=>run&&run.hereId?run.hereId:'-'")
        steps.append(('भीतर दृश्य में: ' if inside else 'जगह के पन्ने पर: ')+where)
    # nothing may be left covering the screen
    left=pg.evaluate("()=>document.querySelectorAll('.dveil').length")
    if left: bad.append('the doorway light is still covering the screen')
    stuck=pg.evaluate("""()=>{const b=document.getElementById('bigshow');
      if(!b||b.hidden)return false;
      return b.querySelectorAll('button').length===0;}""")
    if stuck: bad.append('a screen is open with nothing to press on it')
    ways=pg.evaluate("""()=>{const a=[...document.querySelectorAll('.lacts button')].map(b=>b.textContent);
      if(a.length)return a;
      return [...document.querySelectorAll('#story button')].filter(b=>b.getBoundingClientRect().width>2)
        .map(b=>b.textContent.replace(/\\s+/g,' ').slice(0,24)).slice(0,5);}""")
    if not ways: bad.append('after the door there is no way on at all')
    else: steps.append('आगे के रास्ते: '+', '.join(ways))
    br.close()
print(json.dumps({'steps':steps,'issues':bad,'errors':errs[:3]},ensure_ascii=False,indent=1))
