/* a find arrives wrapped: it shines, it opens, it closes, and it tells everything inside */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const store={};global.localStorage={getItem:k=>store[k]||null,setItem(k,v){store[k]=v}};
let queue=[];global.performance={now:()=>0};global.requestAnimationFrame=f=>{queue.push(f);return 1;};
function pump(){for(let i=0;i<300&&queue.length;i++){const f=queue.shift();try{f(1e9)}catch(e){}}queue.length=0;}
global.setTimeout=f=>{f();return 0;};global.clearTimeout=()=>{};global.innerWidth=1200;
function mk(t){const cls=new Set();const o={t,style:{},dataset:{},innerHTML:'',textContent:'',children:[],hidden:false,par:null,
 get className(){return [...cls].join(' ')},set className(v){cls.clear();String(v).split(/\s+/).filter(Boolean).forEach(c=>cls.add(c))},
 classList:{add(c){cls.add(c)},remove(c){cls.delete(c)},toggle(c,on){if(on===undefined){cls.has(c)?cls.delete(c):cls.add(c);return cls.has(c);}return on?cls.add(c):cls.delete(c)},contains(c){return cls.has(c)}},
 setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},
 getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},
 appendChild(c){c.par=o;o.children.push(c);return c},remove(){},querySelector(){return null},querySelectorAll(){return []}};return o;}
const els={};global.document={createElement:t=>mk(t),getElementById:id=>els[id]||(els[id]=mk(id)),querySelector:()=>null};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+
 ';global.T={mainList,start,visit,story,CARDS,L,save:()=>save,blankSave,front,NIGHTS,run:()=>run};');
let bad=[];const must=(c,m)=>{if(!c)bad.push(m)};
function find(n,cls,out){out=out||[];(n.children||[]).forEach(c=>{
 if(String(c.className).split(' ').includes(cls))out.push(c);find(c,cls,out);});return out;}
function deep(n){let o=String(n.innerHTML||'')+' '+String(n.textContent||'');
 (n.children||[]).forEach(c=>o+=' '+deep(c));return o;}
Object.assign(T.save(),T.blankSave());
T.front();pump();T.start('khoj');pump();
let gifts=[];
const W0=T.NIGHTS.find(n=>n.id==='khoj').watches;
outer: for(let i=0;i<W0.length;i++){
 for(const sp of W0[i].spots){
  const r=T.run();r.w=i;r.used=0;r.pickedHere=[];r.busy=false;
  r.ghadi=(T.mainList(i).indexOf(sp)>-1?0:1);
  T.visit(sp);pump();
  gifts=find(T.story,'gift');
  if(gifts.length)break outer;
 }
}
must(gifts.length>0,'a find did not arrive as a wrapped box');
const g=gifts[0];
must(g.classList.contains('shut'),'the box arrived already open, with no surprise left');
const lid=g.children[0],body=g.children[1];
must(String(lid.className).includes('giftlid'),'the box has no lid to tap');
/* a fresh find says खोलो; one already read says फिर से पढ़ो and carries its mark */
must(deep(lid).indexOf('खोलो')>-1||deep(lid).indexOf('फिर से पढ़ो')>-1,'the lid does not say it can be opened');
must(deep(lid).length>8,'the lid does not name the find');
must(['g-chh','g-man','g-gr'].some(k=>g.classList.contains(k)),'the box does not show which kind it is');
must(deep(lid).indexOf(T.L.chh)>-1||deep(lid).indexOf(T.L.man)>-1||deep(lid).indexOf(T.L.gr)>-1,
 'the lid does not name the kind');
/* opening shows the whole thing with its citation */
lid.onclick();
must(!g.classList.contains('shut'),'tapping the lid did not open the box');
must(deep(body).indexOf('fsrc')>-1,'the opened box carries no citation');
const shown=Object.keys(T.CARDS).find(c=>deep(body).indexOf(T.CARDS[c].t)>-1);
must(shown,'the opened box names no find');
if(shown)must(deep(body).indexOf(T.CARDS[shown].x.slice(0,20))>-1,'the opened box does not hold the thing itself');
must(deep(lid).indexOf('बंद करो')>-1,'the open box does not offer to close');
/* and it closes again */
lid.onclick();
must(g.classList.contains('shut'),'the box could not be closed again');
/* the shine and the opening have their own movement */
must(/\.gift\.shut\{[^}]*animation/.test(page),'the wrapped box does not move at all');
must(/giftshine/.test(page),'the wrapped box has no shine');
must(/giftopen/.test(page),'opening the box has no movement');
must(/\.gift\.g-man\{/.test(page)&&/\.gift\.g-gr\{/.test(page),'the kinds of box look the same');
console.log(bad.length?('FAILS ('+bad.length+'):\n  '+bad.slice(0,8).join('\n  ')):
 'gift boxes checked: shut on arrival, open and close by tap, three kinds');
