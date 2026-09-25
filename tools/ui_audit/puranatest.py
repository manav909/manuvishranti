# the game as it was built: map, places, tellings, detours, quiz, notebook, letter, night's end
import json
from playwright.sync_api import sync_playwright
THREE=open('/tmp/three/node_modules/three/build/three.min.js','rb').read()
bad=[];ok=[]
def note(m): bad.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=br.new_page(viewport={'width':390,'height':844})
    pg.route('**/three.min.js',lambda r:r.fulfill(status=200,body=THREE,headers={'content-type':'application/javascript'}))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(1300)
    pg.evaluate("""()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());
      save.role='jigyasu';save.rolePicked=true;roleTint();start('khoj');}""")
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const b=document.querySelector('#bigshow .bshut');if(b)b.click();}")
    pg.wait_for_timeout(700)

    # 1. the map
    m=pg.evaluate("""()=>{const s=document.querySelector('#mapPane svg')||document.querySelector('svg');
      if(!s)return null;const r=s.getBoundingClientRect();
      return {h:Math.round(r.height),pins:document.querySelectorAll('.pin,.mpin,[class*=pin]').length};}""")
    if not m or m['h']<80: note('the map is not drawn')
    else: ok.append('नक्शा: %dpx ऊँचा, %d निशान'%(m['h'],m['pins']))

    # 2. the places offered, and walking into one
    cards=pg.evaluate("()=>[...document.querySelectorAll('#story .card-pick')].filter(b=>b.getBoundingClientRect().width>2).length")
    if cards<1: note('no place is offered to walk into')
    else: ok.append('जगहें: %d कार्ड'%cards)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('#story .card-pick')].filter(x=>x.getBoundingClientRect().width>2)[0];if(b)b.click();}")
    pg.wait_for_timeout(1600)
    tells=pg.evaluate("()=>[...document.querySelectorAll('#story button.do.read')].length")
    if tells<1: note('inside a place no telling is offered')
    else: ok.append('उस पल की कथाएँ: %d'%tells)

    # 3. reading a telling
    pg.evaluate("()=>{const b=[...document.querySelectorAll('#story button.do.read')][0];if(b)b.click();}")
    pg.wait_for_timeout(1400)
    if pg.evaluate("()=>panel")!='reader': note('a telling does not open the reading page')
    else:
        srcs=pg.evaluate("()=>[...document.querySelectorAll('#reader .rtabs button')].length")
        ok.append('पढ़ने का पन्ना: %d ग्रंथ'%srcs)
    pg.evaluate("()=>{const b=document.querySelector('#reader .rback');if(b)b.click();}")
    pg.wait_for_timeout(900)

    # 4. a detour
    pg.evaluate("()=>{run.w=2;run.ghadi=0;run.used=0;run.pickedHere=[];offer();}")
    pg.wait_for_timeout(900)
    pg.evaluate("()=>{visit('vatika');}")
    pg.wait_for_timeout(1500)
    tc=pg.evaluate("()=>document.querySelectorAll('.tourcall').length")
    if tc<1: note('no detour is offered where one should be')
    else:
        pg.evaluate("()=>{document.querySelector('.tourcall').click();}")
        pg.wait_for_timeout(1500)
        if pg.evaluate("()=>panel")!='chakkar': note('the detour does not run')
        else: ok.append('चक्कर: चलता है')
        pg.evaluate("()=>{showPanel('story');}")
        pg.wait_for_timeout(600)

    # 5. the notebook and the letter
    pg.evaluate("()=>{showPanel('pothi');fill();}")
    pg.wait_for_timeout(900)
    tabs=pg.evaluate("()=>[...document.querySelectorAll('#pothi .tab, .rtabs button, .tabsbar button')].length")
    if pg.evaluate("()=>panel")!='pothi': note('the notebook does not open')
    else: ok.append('खोजी की पोथी: खुलती है (%d खाने)'%tabs)
    pg.evaluate("()=>{showPanel('story');try{openCard();}catch(e){}}")
    pg.wait_for_timeout(900)
    if not pg.evaluate("()=>{const c=document.getElementById('pcard');return !!(c&&!c.hidden);}"): note('the letter does not open')
    else: ok.append('खोजी का पत्र: खुलता है')
    pg.evaluate("()=>{try{closeCard();}catch(e){}}")
    pg.wait_for_timeout(500)

    # 5b. the strips that ride above the reading
    st=pg.evaluate("""()=>{const r=document.getElementById('raahbar'),m=document.getElementById('muhimbar');
      const rr=r&&!r.hidden?r.getBoundingClientRect():null, s2=document.getElementById('story').getBoundingClientRect();
      return {raah:r&&!r.hidden?[...r.querySelectorAll('.raah b')].map(x=>x.textContent):null,
        over:rr?(rr.bottom>s2.top+2):false,
        trail:document.querySelectorAll('.trail .tchip').length,
        mini:!!document.querySelector('#minimap, .mini svg, .mini canvas')};}""")
    if not st['raah']: note('the road bar is missing over the reading')
    else: ok.append('राह पट्टी: '+', '.join(st['raah']))
    if st['over']: note('the road bar sits on top of the reading')
    if st['trail']<1: note('the trail of places is empty')
    else: ok.append('पगडंडी: %d चिप'%st['trail'])
    if not st['mini']: note('the corner map is gone')
    else: ok.append('कोने का नक्शा: है')

    # 5c. the five questions of the night
    q=pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>/पाँच सवाल/.test(x.textContent||''));
      if(!b)return null;b.click();return true;}""")
    pg.wait_for_timeout(1200)
    if q:
        opts=pg.evaluate("()=>document.querySelectorAll('.qopt, .quizopt, #quiz button').length")
        if opts<2: note('the questions open but offer nothing to answer')
        else: ok.append('पाँच सवाल: %d जवाब सामने'%opts)
        pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(x=>/बंद|लौटो/.test(x.textContent||''));if(b)b.click();}")
        pg.wait_for_timeout(600)

    # 6. the night runs to its end
    for i in range(24):
        st=pg.evaluate("""()=>{const b=document.getElementById('bigshow');if(b&&!b.hidden){b.hidden=true;b.innerHTML='';}
          if(!run)return 'ख़त्म';
          const sp=ghadiSpots().filter(x=>!run.pickedHere.includes(x));
          if(sp.length&&visitsHere()-run.used>0){visit(sp[0]);return 'जगह';}
          endWatch();return 'घड़ी';}""")
        pg.wait_for_timeout(450)
        if pg.evaluate("()=>document.getElementById('story').innerText.indexOf('भोर हो गई')>-1"): break
    if pg.evaluate("()=>document.getElementById('story').innerText.indexOf('भोर हो गई')<0"): note('the night never reaches its dawn')
    else: ok.append('रात पूरी: भोर तक पहुँची')
    br.close()
print(json.dumps({'ok':ok,'issues':bad,'errors':errs[:3]},ensure_ascii=False,indent=1))
