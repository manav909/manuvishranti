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
    if not wait_for(pg,"()=>!!document.querySelector('#bigshow .dcanvas')"): bad.append('the roles never came')
    else: steps.append('भूमिकाएँ: '+title())
    pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const bs=[...document.querySelectorAll('#bigshow .srlist button')];if(bs.length>1)bs[1].click();}")
    # 2. रातें
    if not wait_for(pg,"()=>{const t=document.querySelector('#bigshow .btitle');return t&&t.textContent.indexOf('कहाँ से शुरू')>-1;}",tries=22):
        bad.append('picking a role did not lead to the nights')
    else: steps.append('रातें: '+title()+' | भूमिका '+pg.evaluate("()=>save.role"))
    pg.wait_for_timeout(1000)
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .srlist button');if(b)b.click();}")
    # 3. रात का परदा या सीधे दरवाज़े
    if not wait_for(pg,"()=>!!run",tries=20): bad.append('the night never began')
    else: steps.append('रात शुरू: '+pg.evaluate("()=>run?run.N.name:'-'"))
    for i in range(6):
        if pg.evaluate("()=>!!document.querySelector('.dcanvas')&&/दरवाज़ा/.test((document.querySelector('#bigshow .btitle')||{}).textContent||'')"): break
        pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
        pg.wait_for_timeout(900)
    if pg.evaluate("()=>!!document.querySelector('.dcanvas')"): steps.append('दरवाज़े: '+title())
    else: bad.append('the doors never came')
    # 4. भीतर
    pg.wait_for_timeout(1000)
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .srlist button');if(b)b.click();}")
    if not wait_for(pg,"()=>!!document.querySelector('.leafstrip')",tries=26): bad.append('walking through the door did not lead inside')
    else: steps.append('भीतर: '+title()+' | '+pg.evaluate("()=>{const s=document.querySelector('.lsrc');return s?s.textContent:'-'}"))
    # 5. भीतर से आगे
    ways=pg.evaluate("()=>[...document.querySelectorAll('.lacts button')].map(b=>b.textContent)")
    if not ways: bad.append('inside the place there is no way on')
    else: steps.append('भीतर के रास्ते: '+', '.join(ways))
    br.close()
print(json.dumps({'steps':steps,'issues':bad,'errors':errs[:3]},ensure_ascii=False,indent=1))
