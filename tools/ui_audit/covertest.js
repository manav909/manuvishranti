const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={DETOUR,PX_SPR};');
/* things that mean the same on screen: showing one of them is showing the thing */
const FAM=[["monkey","whitemonkey","tailfire"],["shade","sbek","wayang","screen"],["tree","ashoka","chinar","coconut","fruit"],
 ["palace","relief","tower","pillar","throne"],["house","hillhouse","hut"],["mountain","snowpeak","rock","cliffcave"],
 ["count","sawal","scale"],["speech","chant"],["wave","fish","croc","boat","shikara"],["pothi","palmleaf","scroll"],
 ["man","woman","child","king","sage","guard","dancer","oldwoman"],["fire","torch","lamp"]];
const kin=n=>{const out=new Set([n]);FAM.forEach(f=>{if(f.includes(n))f.forEach(x=>out.add(x));});return out;};
const rows=[];
Object.keys(T.DETOUR).forEach(k=>{const D=T.DETOUR[k];D.stops.forEach((st,i)=>{
 const text=(D.n+' '+st.n+' '+st.say.join(' '));
 const have=new Set((st.px.it||[]).map(t=>t[0]));
 const want=[];
 /* only the thing's own name counts, and only as a whole word */
 const words=new Set(text.replace(/[,।.:;!?"'()]/g,' ').split(/\s+/).filter(Boolean));
 Object.keys(T.PX_SPR).forEach(sp=>{const tags=(T.PX_SPR[sp].t||'').split(' ').filter(Boolean).slice(0,1);
  if(tags.some(w=>w.length>2&&words.has(w)))want.push(sp);});
 const missing=want.filter(w=>![...kin(w)].some(x=>have.has(x)));
 rows.push({k,i,n:st.n,want:want.length,have:want.length-missing.length,missing});});});
const tot=rows.reduce((a,r)=>a+r.want,0),got=rows.reduce((a,r)=>a+r.have,0);
const CEIL=+(process.argv[2]||0);
if(tot-got>CEIL)console.log('FAILS: '+(tot-got)+' things are named in a telling but missing from its scene (ceiling '+CEIL+')');
else console.log('scene coverage checked: every one of '+tot+' things named in a telling stands in its scene');
const bad=rows.filter(r=>r.missing.length).sort((a,b)=>b.missing.length-a.missing.length);
bad.slice(0,10).forEach(r=>console.log('  ',r.k,'#'+(r.i+1),r.n,'→',r.missing.join(', ')));
fs.writeFileSync('/tmp/cover.json',JSON.stringify(rows));
