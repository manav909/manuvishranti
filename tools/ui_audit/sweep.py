# every role through every night: does it run to dawn without a stumble
import json,sys
from playwright.sync_api import sync_playwright
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
ROLES=['jigyasu','yatri','kathapremi','balak','yoddha','shastri','sadhak','raja']
NIGHTS=sys.argv[1].split(',') if len(sys.argv)>1 else ['khoj']
rows=[];bad=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':390,'height':844})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(1200)
    for r in ROLES:
        for n in NIGHTS:
            before=len(errs)
            pg.evaluate("""a=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());
              save.role=a[0];save.rolePicked=true;roleTint();
              save.nights={khoj:1,aag:1,khabar:1,vilanka:1,vidya:1};
              save.katha={vilanka:1,shakti:1,vidya:1};persist();start(a[1]);}""",[r,n])
            pg.wait_for_timeout(500)
            seen=0;dawn=False
            for i in range(40):
                st=pg.evaluate("""()=>{const b=document.getElementById('bigshow');if(b&&!b.hidden){b.hidden=true;b.innerHTML='';}
                  if(!run)return 'ख़त्म';
                  const sp=ghadiSpots().filter(x=>!run.pickedHere.includes(x));
                  if(sp.length&&visitsHere()-run.used>0){visit(sp[0]);return 'जगह';}
                  endWatch();return 'घड़ी';}""")
                pg.wait_for_timeout(180)
                if st=='जगह': seen+=1
                if pg.evaluate("()=>document.getElementById('story').innerText.indexOf('भोर हो गई')>-1 || document.getElementById('story').innerText.indexOf('दिन ढल गया')>-1 || document.getElementById('story').innerText.indexOf('ख़बर पहुँच गई')>-1 || document.getElementById('story').innerText.indexOf('रात पूरी')>-1"):
                    dawn=True;break
            mani=pg.evaluate("()=>purse()")
            cards=pg.evaluate("()=>Object.keys(save.cards||{}).length")
            rows.append({'role':r,'night':n,'places':seen,'dawn':dawn,'mani':mani,'cards':cards})
            if not dawn: bad.append('%s could not finish the night %s'%(r,n))
            if len(errs)>before: bad.append('%s in %s hit a browser error: %s'%(r,n,errs[before]))
    br.close()
print(json.dumps({'rows':rows,'issues':bad,'errors':errs[:4]},ensure_ascii=False,indent=1))
