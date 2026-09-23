# only the place you are at may stay open; everything already read folds away
import json,sys
from playwright.sync_api import sync_playwright
bad=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:140]))
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(700)
    pg.evaluate("()=>{Object.assign(save,blankSave());save.role='jigyasu';save.rolePicked=true;roleTint();start('khoj');}")
    seen=0
    for i in range(20):
        ok=pg.evaluate("""()=>{const bs=[...document.querySelectorAll('#story button')].filter(b=>b.getBoundingClientRect().width>2&&/do go|card-pick/.test(b.className));
          if(!bs.length)return false;bs[0].click();return true;}""")
        pg.wait_for_timeout(300)
        if not ok: break
        st=pg.evaluate("""()=>{const vs=[...document.querySelectorAll('#story .visit')];
          const steps=[...document.querySelectorAll('#story > .step')];
          return {visits:vs.length, open:vs.filter(v=>!v.classList.contains('shut')).length,
            openSteps:steps.filter(s=>!s.classList.contains('shut')).length,
            total:document.getElementById('story').scrollHeight, view:document.getElementById('story').clientHeight,
            hiddenGo:[...document.querySelectorAll('#story .do.go')].filter(b=>b.getBoundingClientRect().width<2).length,
            visibleGo:[...document.querySelectorAll('#story .do.go')].filter(b=>b.getBoundingClientRect().width>2).length};}""")
        seen+=1
        if st['visits']>1 and st['open']>1: bad.append(f"step {i}: {st['open']} places open at once")
        if st['openSteps']>2: bad.append(f"step {i}: {st['openSteps']} hours open at once")
        if st['total']>st['view']*6: bad.append(f"step {i}: the reading runs {round(st['total']/st['view'],1)} screens long")
        if st['visibleGo']==0 and st['hiddenGo']>0: bad.append(f"step {i}: the way on is folded away")
    br.close()
if bad: print('FAILS:\n  '+'\n  '.join(bad[:8]))
else: print('focus checked: through',seen,'moves only the place you stand in stayed open, and the way on stayed in sight')
