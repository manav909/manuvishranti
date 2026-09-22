const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={DETOUR,PX_SPR,pixScene};');
const bad=[];const MIN_DONE=+(process.argv[2]||144);
const all=[];Object.keys(T.DETOUR).forEach(k=>T.DETOUR[k].stops.forEach((st,i)=>all.push({k,i,st})));
const done=all.filter(x=>x.st.px);
const sig={};
done.forEach(({k,i,st})=>{
 const P=st.px,where=k+' #'+(i+1);
 const key=JSON.stringify([P.bg,P.gr,(P.it||[]).map(t=>t[0]).sort()]);
 if(sig[key])bad.push('two stops draw the same scene: '+sig[key]+' and '+where);else sig[key]=where;
 if(!P.me)bad.push(where+': the player is not in the scene');
 if((P.it||[]).length<4)bad.push(where+': fewer than four things in the scene');
 const moves=(P.it||[]).some(t=>(T.PX_SPR[t[0]]&&T.PX_SPR[t[0]].f.length>1)||(t[4]&&t[4].drift));
 if(!moves)bad.push(where+': nothing in the scene moves');
 (P.it||[]).forEach(t=>{if(!T.PX_SPR[t[0]])bad.push(where+': unknown sprite '+t[0]);});
 const text=(st.n+' '+st.say.join(' '));
 const hit=(P.it||[]).some(t=>{const tg=(T.PX_SPR[t[0]]||{}).t||'';return tg.split(' ').some(w=>w&&text.includes(w));});
 if(!hit)bad.push(where+' ('+st.n+'): nothing in the picture is named in the stop text');
 const svg=T.pixScene(P,'raja');if(svg.length<500)bad.push(where+': the scene came out empty');
});
if(done.length<MIN_DONE)bad.push('only '+done.length+' stops have their own scene, fewer than '+MIN_DONE);
console.log(bad.length?'FAILS ('+bad.length+'):\n  '+bad.slice(0,20).join('\n  '):'detour scenes checked: '+done.length+' of '+all.length+' stops have their own moving scene with the player, none alike');
