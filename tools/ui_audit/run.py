import json, sys, collections
from playwright.sync_api import sync_playwright
RAW = open('/tmp/ui/audit.js', encoding='utf8').read()
# measure the settled colours: stop every transition before reading
AUDIT = "(()=>{let st=document.getElementById('__audit');if(!st){st=document.createElement('style');st.id='__audit';st.textContent='*,*:before,*:after{transition:none!important;animation-duration:0s!important}';document.head.appendChild(st);} document.body.offsetHeight; return " + RAW.strip().rstrip(';') + ";})()"
URL = 'file:///mnt/user-data/outputs/lanka-map3.html'
VIEWS = {'phone': (390, 844), 'tablet': (820, 1180), 'desktop': (1366, 820)}
ROLES = ['jigyasu','yatri','kathapremi','balak','yoddha','shastri','sadhak','raja']
SKIES = ['night','dawn','day','dusk']
NIGHTS = ['khoj','aag','khabar','vilanka','shakti','vidya']
found = collections.OrderedDict()
errors = []
def note(ctx, items):
    for it in items:
        key = (it['kind'], it.get('cls',''), it.get('text',''))
        if key not in found: found[key] = {**it, 'where': []}
        if len(found[key]['where']) < 6: found[key]['where'].append(ctx)
def settle(pg, ms=120): pg.wait_for_timeout(min(ms,150))
def fresh(pg, role):
    pg.evaluate("""r=>{try{localStorage.clear()}catch(e){};
      Object.assign(save, blankSave()); save.role=r; save.rolePicked=true;
      ['khoj','aag','khabar','vilanka','shakti'].forEach(n=>{save.nights[n]=1;save.done[n]=1;});
      save.katha=save.katha||{}; Object.keys(KATHA||{}).forEach(k=>save.katha[k]=1);
      roleTint();}""", role)
def at_sky(pg, sky):
    pg.evaluate("s=>{app.dataset.sky=s; roleTint();}", sky)
def run(scheme_list, view_list, role_list):
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        for scheme in scheme_list:
            for vname,(w,h) in [(v,VIEWS[v]) for v in view_list]:
                ctx = br.new_context(viewport={'width':w,'height':h}, color_scheme=scheme)
                pg = ctx.new_page()
                pg.on('pageerror', lambda e, v=vname, s=scheme: errors.append(f'{s}/{v}: {e}'))
                pg.on('console', lambda m, v=vname, s=scheme: errors.append(f'{s}/{v} console: {m.text}') if m.type=='error' else None)
                pg.goto(URL); settle(pg, 600)
                roles = role_list
                for role in roles:
                    fresh(pg, role)
                    # the picking screen, and one role page
                    pg.evaluate("()=>roleScreen()"); settle(pg)
                    note(f'{scheme}/{vname}/{role}/चुनने का पन्ना', pg.evaluate(AUDIT))
                    pg.evaluate("r=>roleDetail(r)", role); settle(pg)
                    note(f'{scheme}/{vname}/{role}/भूमिका का पन्ना', pg.evaluate(AUDIT))
                    pg.evaluate("()=>front()"); settle(pg)
                    note(f'{scheme}/{vname}/{role}/रातों का पन्ना', pg.evaluate(AUDIT))
                    nights = NIGHTS if role in ('jigyasu','raja') else ['khoj','aag']
                    for night in nights:
                        pg.evaluate("n=>start(n)", night); settle(pg, 400)
                        skies = SKIES if vname=='phone' else [None]
                        for sky in skies:
                            if sky: at_sky(pg, sky)
                            note(f'{scheme}/{vname}/{role}/{night}/{sky or "अपना"}/रात की शुरुआत', pg.evaluate(AUDIT))
                        # walk the first ghadi, then open the free choice
                        pg.evaluate("""()=>{const r=run;r.busy=false;
                          const m=mainList(r.w); if(m.length){visit(m[0]);} }"""); settle(pg, 500)
                        note(f'{scheme}/{vname}/{role}/{night}/पल', pg.evaluate(AUDIT))
                        pg.evaluate("""()=>{const r=run;r.busy=false;r.ghadi=1;r.used=0;offer();}"""); settle(pg)
                        note(f'{scheme}/{vname}/{role}/{night}/दूसरी घड़ी', pg.evaluate(AUDIT))
                        pg.evaluate("()=>{run.w=run.N.watches.length;run.busy=false;turn();}"); settle(pg, 500)
                        note(f'{scheme}/{vname}/{role}/{night}/सुबह', pg.evaluate(AUDIT))
                    # the notebook, each page
                    pg.evaluate("()=>showPanel('pothi')"); settle(pg)
                    tabs = pg.evaluate("()=>[...document.querySelectorAll('#pothi .tabs button')].map(b=>b.textContent)")
                    for i,tb in enumerate(tabs):
                        pg.evaluate("i=>{const b=document.querySelectorAll('#pothi .tabs button')[i]; if(b) b.click();}", i); settle(pg)
                        note(f'{scheme}/{vname}/{role}/पोथी/{tb}', pg.evaluate(AUDIT))
                    pg.evaluate("()=>showPanel('story')")
                    pg.evaluate("()=>helpPanel()"); settle(pg)
                    note(f'{scheme}/{vname}/{role}/मदद', pg.evaluate(AUDIT))
                    pg.evaluate("()=>closeDeep()")
                    pg.evaluate("()=>openCard()"); settle(pg)
                    note(f'{scheme}/{vname}/{role}/पत्र', pg.evaluate(AUDIT))
                    pg.evaluate("()=>closeCard()")
                    # quiet mode must not change what can be read
                    pg.evaluate("()=>{const b=document.getElementById('calmBtn'); if(b) b.click();}"); settle(pg)
                    note(f'{scheme}/{vname}/{role}/हरकत कम', pg.evaluate(AUDIT))
                    pg.evaluate("()=>{const b=document.getElementById('calmBtn'); if(b) b.click();}")
                ctx.close()
        br.close()
sc, vw, rl = sys.argv[1].split(','), sys.argv[2].split(','), sys.argv[3].split(',')
run(sc, vw, rl)
with open('/tmp/ui/report.jsonl','a',encoding='utf8') as f:
    for v in found.values(): f.write(json.dumps(v,ensure_ascii=False)+'\n')
    for e in errors[:40]: f.write(json.dumps({'kind':'error','text':e},ensure_ascii=False)+'\n')
kinds = collections.Counter(v['kind'] for v in found.values())
print('अलग अलग गड़बड़ियाँ:', len(found), dict(kinds), '| ब्राउज़र की ग़लतियाँ:', len(errors))
