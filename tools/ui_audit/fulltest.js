/* how much of the telling is actually on the page */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={SC,layersOf,SRC};');
let count=0,sumL=0,sumC=0;const small=[],mains=[];
Object.keys(T.SC).forEach(m=>{const L=T.layersOf(m)||[];
 L.forEach((x,i)=>{const say=(x.say||[]);if(!say.length)return;count++;sumL+=say.length;
  const c=say.join(' ').length;sumC+=c;
  if(i===0)mains.push({m,l:say.length,c});
  if(say.length<=3&&c<300)small.push({m,src:x.src||'vr',l:say.length,c});});});
const CEIL=+(process.argv[2]||31);
const thinMains=mains.filter(x=>x.l<=3).length;
if(thinMains>CEIL)console.log('FAILS: '+thinMains+' main tellings still hold only three lines (ceiling '+CEIL+')');
else console.log('fullness checked: '+count+' telling pages, '+(sumL/count).toFixed(1)+' lines each on average, '+thinMains+' main tellings still at three lines');
fs.writeFileSync('/tmp/thin.json',JSON.stringify({small,mains}));
mains.filter(x=>x.l<=3).slice(0,10).forEach(t=>console.log('  ',t.m,t.l,'lines',t.c,'letters'));
