/* a telling of a moment must tell the moment; talk about the book is allowed only as a tail note */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={SC,layersOf,SRC};');
/* a line that talks about the book, the poet, the copies or the manner of telling */
const ABOUT=/(कथा में|ग्रंथ में|पाठ में|रामायण में|वाली कथा|वहाँ ज़ोर|इसलिए वहाँ|वहाँ यह|पन्ने|पोथि|प्रति|पांडुलिपि|अनुवाद|सदी|कवि|भाषा में|छपी|संक्षेप में आता|आता ही नहीं|नहीं आता|थोड़े में है|सिमटी हुई)/;
/* a line that says a thing is missing must also say where it can be read in full */
const POINT=/(में पूरा|पूरा ब्योरा|वहाँ पूरा|पूरी कथा|की यात्रा में|भूमिका में)/;
const bad=[];let total=0;
Object.keys(T.SC).forEach(m=>{
 (T.layersOf(m)||[]).forEach(L=>{
  const lines=(L.say||[]);if(!lines.length)return;total++;
  const about=lines.filter(x=>ABOUT.test(x)).length;
  const scene=lines.length-about;
  const absent=lines.some(x=>/(नहीं आता|आता ही नहीं|नहीं मिलती|नहीं है)/.test(x));
  if(about>lines.length/2||scene<2){
   /* an absent moment is allowed, but only if it points at where it is told */
   if(absent&&lines.some(x=>POINT.test(x)))return;
   bad.push({m,src:L.src||'vr',about,scene,n:lines.length,first:lines[0].slice(0,68)});
  }
 });
});
const CEIL=+(process.argv[2]||0);
if(bad.length>CEIL){
 console.log('FAILS: '+bad.length+' tellings talk about the book instead of telling the moment (ceiling '+CEIL+')');
 bad.slice(0,16).forEach(b=>console.log('  ',b.m,'['+b.src+'] about',b.about,'of',b.n,'|',b.first));
}else console.log('katha checked: all '+total+' tellings tell their own moment');
fs.writeFileSync('/tmp/katha.json',JSON.stringify(bad));
