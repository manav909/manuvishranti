import json,sys
from playwright.sync_api import sync_playwright
pairs=json.loads(sys.argv[1]); out=sys.argv[2] if len(sys.argv)>2 else '/tmp/three/g'
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':820,'height':1000})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.on('console',lambda m:errs.append('console:'+m.text[:160]) if m.type=='error' and 'fonts' not in m.text and '403' not in m.text else None)
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(900)
    print('three loaded:',pg.evaluate("()=>!!window.THREE"),'| webgl:',pg.evaluate("()=>s3ok()"))
    for n,(k,i,r) in enumerate(pairs):
        pg.evaluate("([k,i,r])=>{Object.assign(save,blankSave());save.role=r;save.rolePicked=true;roleTint();start('khoj');startTour(k);tour.i=i;drawTour();}",[k,i,r])
        pg.wait_for_timeout(2600)
        is3d=pg.evaluate("()=>!!document.querySelector('#chakkar .tart.is3d canvas')")
        pg.locator('#chakkar .tart').first.screenshot(path=f'{out}{n}.png')
        print(n,k,i,r,'3d' if is3d else 'PIXEL FALLBACK')
    print('errors',errs[:6])
    br.close()
