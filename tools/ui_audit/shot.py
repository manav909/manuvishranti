import sys
from playwright.sync_api import sync_playwright
go=sys.argv[1]; out=sys.argv[2]; W,H=(int(sys.argv[3]),int(sys.argv[4])) if len(sys.argv)>4 else (390,844)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':W,'height':H})
    pg.goto('file:///mnt/user-data/outputs/lanka-map3.html'); pg.wait_for_timeout(700)
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){};Object.assign(save,blankSave());save.role='jigyasu';save.rolePicked=true;save.nights.khoj=1;save.done.khoj=1;roleTint();}")
    pg.evaluate(go); pg.wait_for_timeout(1300)
    pg.screenshot(path=out)
    print(pg.evaluate("()=>[...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect();if(r.width<2)return false;const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return t&&(t===b||b.contains(t));}).map(b=>b.textContent.trim().slice(0,22))"))
    br.close()
