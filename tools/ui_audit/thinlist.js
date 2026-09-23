const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={SC,layersOf,SRC};');
const list=[];const from=+(process.argv[2]||0),to=+(process.argv[3]||11);
Object.keys(T.SC).forEach(m=>{(T.layersOf(m)||[]).forEach((x,i)=>{const say=x.say||[];
 if(i>0&&say.length<=3)list.push({m,src:x.src||'vr',say});});});
console.log('बचे हुए पतले पन्ने:',list.length);
list.slice(from,to).forEach(x=>{console.log('### '+x.m+' ['+x.src+'] '+(T.SRC[x.src]?T.SRC[x.src].n:''));
 x.say.forEach(t=>console.log('  - '+t));});
