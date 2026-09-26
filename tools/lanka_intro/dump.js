const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const pg=await b.newPage();
await pg.route('https://cdnjs.cloudflare.com/**',r=>r.fulfill({status:200,contentType:'text/javascript',body:''}));
await pg.route('https://fonts.googleapis.com/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));
await pg.goto('http://127.0.0.1:8765/lanka_ki_khoj/',{waitUntil:'load'});
const d=await pg.evaluate(()=>{const r=(o,f)=>Object.fromEntries(Object.entries(o).map(([k,v])=>[k,f(v)]));
 return {ROLE:r(ROLE,v=>({n:v.n,t:v.t,x:v.x,tint:v.tint})),NIGHTS:NIGHTS.map(n=>({id:n.id,name:n.name,about:n.about,needs:n.needs||null})),
 CHINH:CHINH,KHEL:KHEL,PL:Object.values(PLACES).map(p=>[p.la,p.lo]),COAST_IN,COAST_LK,BRIDGE_N,BRIDGE_S,CITY,HILLS}});
fs.writeFileSync('lkdata.json',JSON.stringify(d));console.log(Object.keys(d.ROLE).length,d.NIGHTS.length,d.PL.length,JSON.stringify(d).length);await b.close();})();
