/* every mission must be finishable with what that night and that role actually hold */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={MUHIM,ROLE,NIGHTS,SC,layersOf,DETOUR,CARDS};');
const bad=[];
const roles=Object.keys(T.ROLE);
/* what a night offers: places to visit, tellings to read, finds to pick up, journeys to walk */
function offers(N,role){
 let place=0,read=0,card=0,tour=0;
 /* a player does not get to see every place: one per watch, two once the first night is done */
 const allowed=N.id==="khoj"?1:2;
 N.watches.forEach((w,i)=>{
  place+=Math.min(w.spots.length,allowed);
  w.spots.forEach(sp=>{const k=N.id+"-"+sp+"-"+i;const L=T.layersOf(k)||[];
   read+=L.length;
   L.forEach(x=>{card+=(x.cards||[]).length;
    Object.keys(T.DETOUR).forEach(dk=>{const D=T.DETOUR[dk];
     if(D.only===role&&D.src===(x.src||'vr')&&D.at.indexOf(k)>-1)tour++;});});});
 });
 return {place,read,card,tour};
}
roles.forEach(role=>{
 const night=Object.keys(T.MUHIM).find(k=>T.MUHIM[k].size==="raat"&&T.MUHIM[k].only===role);
 if(!night){bad.push(role+': has no night mission of its own');return;}
 const M=T.MUHIM[night];
 T.NIGHTS.forEach(N=>{
  const o=offers(N,role);
  const have={place:o.place,read:o.read,card:o.card,
   placecard:o.place+o.card,placetour:o.place+o.tour,cardread:o.card+o.read,tour:o.tour}[M.count];
  if(have===undefined){bad.push(night+': counts something the check does not know: '+M.count);return;}
  if(have<M.goal)bad.push(role+' in '+N.id+': its night mission asks for '+M.goal+' but a player can only reach '+have);
 });
});
/* the watch missions must be possible in an ordinary watch too */
["g_dojagah","g_dobaat","g_dogranth"].forEach(k=>{
 const M=T.MUHIM[k];if(M.goal>3)bad.push(k+': a watch mission asking for '+M.goal+' is too much for one watch');
});
if(bad.length)console.log('FAILS:\n  '+bad.slice(0,10).join('\n  '));
else console.log('missions checked: every role can finish its night mission in every night, and the watch missions fit a watch');
