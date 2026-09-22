# every stop, every scene: it must draw in 3D, draw something, raise no error, and keep the player on screen
import json,sys
from playwright.sync_api import sync_playwright
lo,hi=int(sys.argv[1]),int(sys.argv[2])
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
roles=["jigyasu","yatri","kathapremi","balak","yoddha","shastri","sadhak","raja"]
bad=[];done=0
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':640,'height':900})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:160]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(700)
    stops=pg.evaluate("()=>{const o=[];Object.keys(DETOUR).forEach(k=>DETOUR[k].stops.forEach((s,i)=>o.push([k,i])));return o;}")
    for n,(k,i) in enumerate(stops[lo:hi]):
        r=roles[(lo+n)%8]; e0=len(errs)
        pg.evaluate("([k,i,r])=>{document.getElementById('app').classList.add('calm');Object.assign(save,blankSave());save.role=r;save.rolePicked=true;roleTint();if(!run)start('khoj');startTour(k);tour.i=i;drawTour();}",[k,i,r])
        pg.wait_for_timeout(450)
        info=pg.evaluate("""()=>{const a=document.querySelector('#chakkar .tart');const c=a&&a.querySelector('canvas.s3');const cur=S3NOW();
          if(!c||!a.classList.contains('is3d'))return {d3:false};
          return {d3:true,me:cur&&cur.me};}""")
        if info.get('d3'):
            import io
            from PIL import Image, ImageStat
            png=pg.locator('#chakkar .tart').first.screenshot()
            im=Image.open(io.BytesIO(png)).convert('L').resize((64,36))
            ex=im.getextrema(); info['range']=ex[1]-ex[0]; info['std']=ImageStat.Stat(im).stddev[0]
        where=f'{k} #{i+1} ({r})'
        if not info.get('d3'): bad.append(where+': no 3D scene')
        else:
            if info['range']<40 or info['std']<6: bad.append(where+f": the frame is nearly blank (range {info['range']}, spread {info['std']:.1f})")
            me=info.get('me')
            if not me: bad.append(where+': the player was not placed')
            elif abs(me['x'])>0.97 or abs(me['y'])>0.97: bad.append(where+f": the player is off screen {me}")
        if len(errs)>e0: bad.append(where+': '+errs[-1])
        done+=1
    br.close()
print(json.dumps({'checked':done,'bad':bad},ensure_ascii=False))
