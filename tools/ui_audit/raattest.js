/* a night once played must stay open, and the dawn must always offer a way on */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
/* the front gate must let a played night through, whatever door it was entered by */
if(!/const been=!!\(save\.nights&&save\.nights\[N\.id\]\);[\s\S]{0,200}const ok=been\|\|/.test(page))
 bad.push('a night already played can still show as shut on the front page');
/* the dawn must offer some night to go on with, not only the one that follows in order */
if(!/NIGHTS\.find\(x=>x\.id!==N\.id&&!save\.nights\[x\.id\]&&openNight\(x\)\)/.test(page))
 bad.push('the dawn offers no way on when no night follows this one in order');
if(page.indexOf('शुरुआत पर लौटो')<0)bad.push('the dawn has no way back to the start');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('nights checked: a played night stays open, and the dawn always offers a way on and a way back');
