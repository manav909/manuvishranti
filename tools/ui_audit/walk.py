# a whole play, photographed screen by screen, the way a player sees it
import json,sys
from playwright.sync_api import sync_playwright
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
shots=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':390,'height':844})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(900)
    def shot(n):
        pg.wait_for_timeout(500); pg.screenshot(path=f"/tmp/ui/w_{n}.png",animations="disabled",timeout=15000); shots.append(n)
    shot('01_start')
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());roleScreen();}"); shot('02_roles')
    pg.evaluate("()=>{save.role='jigyasu';save.rolePicked=true;roleTint();front();}"); shot('03_nights')
    pg.evaluate("()=>start('khoj')"); shot('04_night')
    for i in range(3):
        pg.evaluate("""()=>{const bs=[...document.querySelectorAll('#story button')].filter(b=>b.getBoundingClientRect().width>2&&/do go|card-pick/.test(b.className));
          if(bs.length)bs[0].click();}"""); pg.wait_for_timeout(500)
    shot('05_moment')
    pg.evaluate("()=>{const b=[...document.querySelectorAll('#story button')].find(x=>/tourcall|chakkar/.test(x.className));if(b)b.click();else startTour('vr_vatika',null);}")
    pg.wait_for_timeout(1800); shot('06_detour')
    pg.evaluate("()=>{const b=document.querySelector('.tbar .tnext2');if(b)b.click();}"); pg.wait_for_timeout(1600); shot('07_detour2')
    pg.evaluate("()=>{const b=document.querySelector('.tbar .tback');if(b)b.click();}"); shot('08_back')
    pg.evaluate("()=>{showPanel('pothi');fill();}"); shot('09_pothi')
    pg.evaluate("()=>{showPanel('story');openCard();}"); shot('10_card')
    pg.evaluate("()=>{closeCard();run.w=run.N.watches.length;run.busy=false;turn();}"); pg.wait_for_timeout(700); shot('11_dawn')
    print(json.dumps({'shots':shots,'errors':errs[:4]},ensure_ascii=False))
    br.close()
