/* every detour belongs to exactly one role, and no two roles ever walk the same one */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={DETOUR,ROLE,SC,layersOf};');
const bad=[];const roles=Object.keys(T.ROLE);
const by={};roles.forEach(r=>by[r]=[]);
Object.keys(T.DETOUR).forEach(k=>{const D=T.DETOUR[k];
 if(!D.only)bad.push(k+': belongs to no role');
 else if(!by[D.only])bad.push(k+': belongs to a role that does not exist: '+D.only);
 else by[D.only].push(k);});
/* no role may be left without journeys of its own, and each set must reach several tellings and nights */
roles.forEach(r=>{
 const mine=by[r];
 if(mine.length<6)bad.push(r+': only '+mine.length+' journeys of its own');
 const srcs=new Set(mine.map(k=>T.DETOUR[k].src));
 if(srcs.size<5)bad.push(r+': its journeys come from only '+srcs.size+' tellings');
 const nights=new Set();mine.forEach(k=>T.DETOUR[k].at.forEach(a=>nights.add(a.split('-')[0])));
 if(nights.size<2)bad.push(r+': its journeys all sit in one night');
 /* the three long nights must each hold at least one journey of this role's own */
 ['khoj','aag','khabar'].forEach(n=>{if(!nights.has(n))bad.push(r+': no journey of its own in the '+n+' night');});
});
/* the same journey must never show up for two roles */
const seen={};
roles.forEach(r=>by[r].forEach(k=>{if(seen[k])bad.push(k+': shared by '+seen[k]+' and '+r);seen[k]=r;}));
/* and what a role is offered at a moment must be its own */
Object.keys(T.SC).forEach(m=>{(T.layersOf(m)||[]).forEach(L=>{
 Object.keys(T.DETOUR).forEach(k=>{const D=T.DETOUR[k];
  if(D.src===(L.src||'vr')&&D.at.indexOf(m)>-1&&!D.only)bad.push(m+': a journey with no role is offered here');});});});
if(bad.length)console.log('FAILS:\n  '+[...new Set(bad)].slice(0,12).join('\n  '));
else console.log('detours checked: '+Object.keys(T.DETOUR).length+' journeys, each one belonging to a single role, '+
 roles.map(r=>T.ROLE[r].n+' '+by[r].length).join(', '));
