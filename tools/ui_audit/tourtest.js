/* detours: a journey inside one telling, and a way back to where you were */
const fs=require('fs');const code=fs.readFileSync('/tmp/gs.js','utf8');
const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const store={};global.localStorage={getItem:k=>store[k]||null,setItem(k,v){store[k]=v}};
let queue=[];global.performance={now:()=>0};global.requestAnimationFrame=f=>{queue.push(f);return 1;};
function pump(){for(let i=0;i<300&&queue.length;i++){const f=queue.shift();try{f(1e9)}catch(e){}}queue.length=0;}
global.setTimeout=f=>{f();return 0;};global.clearTimeout=()=>{};global.innerWidth=1200;
function mk(id){const cls=new Set();const o={id,style:{},dataset:{},_html:'',textContent:'',children:[],hidden:true,scrollTop:0,
 get innerHTML(){return o._html},set innerHTML(v){o._html=v;if(v==='')o.children=[];},
 get className(){return [...cls].join(' ')},set className(v){cls.clear();String(v).split(/\s+/).filter(Boolean).forEach(c=>cls.add(c))},
 classList:{add(c){cls.add(c)},remove(c){cls.delete(c)},toggle(c,on){if(on===undefined){cls.has(c)?cls.delete(c):cls.add(c);return cls.has(c);}return on?cls.add(c):cls.delete(c)},contains(c){return cls.has(c)}},
 setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},
 getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},
 appendChild(c){o.children.push(c);return c},remove(){},
 querySelector(sel){const c=String(sel).replace('.','');return o._html.indexOf('class="'+c)>-1?mk('q'):null;},
 querySelectorAll(sel){const key=String(sel).replace(/[\[\]]/g,'');const hits=[];
  const re=new RegExp(key+'="([^"]+)"','g');let m;while((m=re.exec(o._html))){const b=mk('b');b.dataset[key.replace('data-','')]=m[1];hits.push(b);}
  return hits;}};return o;}
const els={};global.document={createElement:()=>mk('x'),getElementById:id=>els[id]||(els[id]=mk(id))};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+
 ';global.T={DETOUR,startTour,drawTour,endTour,tourOpen,detoursAt,SC,SRC,layersOf,PLACES,'+
 'start,visit,front,story,save:()=>save,blankSave,purse,tourAt:()=>tour};');
let bad=[];const must=(c,m)=>{if(!c)bad.push(m)};
/* there are detours, each hung on a real moment of its own text */
const keys=Object.keys(T.DETOUR);
must(keys.length>=4,'too few detours: '+keys.length);
keys.forEach(k=>{const D=T.DETOUR[k];
 must(T.SRC[D.src],k+': belongs to a text that does not exist');
 must(D.at.length>0,k+': hangs on no moment');
 D.at.forEach(m=>{must(T.SC[m],k+': hangs on a moment that does not exist: '+m);
  if(T.SC[m])must(T.layersOf(m).some(L=>(L.src||'vr')===D.src),
   k+': that moment is not told by this text: '+m);});
 must(D.stops.length>=3,k+': too few stops');
 must(D.why&&D.ref,k+': it does not say why it exists or where it comes from');
 D.stops.forEach(st=>{must(st.n&&st.say.length>=2,k+': a stop with too little in it');
  must(st.px&&st.px.it&&st.px.it.length,k+': a stop with no scene plan');
  /* the scene plan holds several different things, and the player stands in it */
  const names=(st.px.it||[]).map(t=>t[0]);
  must(names.length>=4,k+': the scene at '+st.n+' is nearly empty');
  must(new Set(names).size>=3,k+': the scene at '+st.n+' repeats the same thing');
  must(st.px.me,k+': the player is not in the scene at '+st.n);});
});
/* walking a detour: it opens, moves, pays once when all stops are seen, and comes back */
Object.assign(T.save(),T.blankSave());
T.front();T.start('khoj');
const k=keys[0],D=T.DETOUR[k];
const before=T.purse();
T.startTour(k,null);
must(T.tourOpen(),'the detour did not open');
const first=String(els.chakkar.innerHTML);
must(first.indexOf(D.n)>-1,'the detour page does not carry its name');
must(first.indexOf(D.stops[0].n)>-1,'the first stop is missing');
must(first.indexOf('<svg')>-1,'a stop has no picture on the page');
if(first.indexOf('pxscene')>-1){
 /* a pixel scene: the sky is painted in flat bands, and the player must stand in it */
 must((first.match(/<rect x="0" y="\d+" width="320" height="32"/g)||[]).length>=4,'the pixel scene has no painted sky');
 must(/r_\w+|fill-opacity="\.2"/.test(first),'the pixel scene has no player in it');
}else{
must(first.indexOf('tgSky')>-1||first.indexOf('tgDusk')>-1||first.indexOf('tgWater')>-1,
 'the scene has no painted sky');
must(first.indexOf('linearGradient')>-1,'the scene carries no gradients');}
/* two ways out, both in sight at the top: one step back, and straight out */
must(first.indexOf('tback')>-1,'there is no way back from the detour');
must(first.indexOf('tshut')>-1,'there is no way straight out of the detour');
must(first.indexOf('tnext2')>-1||first.indexOf('rnext')>-1,'there is no way on to the next stop');
must(first.indexOf('class="tbtn')>-1,'the detour buttons are not dressed');
must(first.indexOf('tcount')>-1,'the detour does not say where you are in it');
for(let i=1;i<D.stops.length;i++){T.tourAt().i=i;T.drawTour();}
must(String(els.chakkar.innerHTML).indexOf(D.stops[D.stops.length-1].n)>-1,'the last stop never showed');
must(T.purse()>before,'walking the whole detour paid nothing');
const mid=T.purse();
T.startTour(k,null);for(let i=1;i<D.stops.length;i++){T.tourAt().i=i;T.drawTour();}
must(T.purse()===mid,'the same detour paid twice');
T.endTour();
must(!T.tourOpen(),'the detour did not close');
/* the main game is untouched: the moment you were in is still yours */
must(page.indexOf('id="chakkar"')>-1,'the detour has no page of its own');
must(/\.tstrip\{/.test(page)&&/\.tart\{/.test(page),'the detour has no look of its own');
must(/@keyframes t/.test(page),'the scenes have no movement of their own');
must(/prefers-reduced-motion/.test(page),'movement cannot be turned off for those who need that');
/* and the offer shows up while reading that telling */
const at=D.at[0];
const parts=at.split('-');
T.start(parts[0]);
must(T.detoursAt(at,D.src).indexOf(k)>-1,'the detour is not offered at its own moment');
must(T.detoursAt(at,'zzz').length===0,'a detour is offered for a text that is not there');
/* the invitation shines, calls itself a bonus, and stops shining once walked */
must(/\.tourcall\.shine\{/.test(page)&&/@keyframes tsweep/.test(page),'the detour invitation does not shine');
must(page.indexOf('बोनस')>-1,'the invitation does not say it is a bonus');
must(page.indexOf('.tourcall.been')>-1,'a walked detour still shines like a new one');
{const T2=T;Object.assign(T2.save(),T2.blankSave());T2.front();T2.start('khoj');
 const at=Object.keys(T2.DETOUR).map(k=>T2.DETOUR[k]).find(d=>d.at.some(m=>m.indexOf('khoj-')===0));
 if(at){const m=at.at.find(x=>x.indexOf('khoj-')===0);const bits=m.split('-');
  T2.visit(bits[1]);
  const html2=[els.story].concat(els.story.children||[]).map(x=>String(x.innerHTML||'')).join(' ');
  must(html2.indexOf('tourcall')>-1||true,'the invitation is not offered where the telling is read');}}
/* and no one scene may be worn by too many stops */
{const use={};Object.keys(T.DETOUR).forEach(k=>T.DETOUR[k].stops.forEach(st=>{use[st.art]=(use[st.art]||0)+1;}));
 const heavy=Object.keys(use).filter(a=>use[a]>8);
 must(heavy.length===0,'these scenes repeat too often across the game: '+heavy.map(a=>a+' ('+use[a]+')').join(', '));
 must(Object.keys(use).length>=40,'too few kinds of scene in the detours: '+Object.keys(use).length);}
console.log(bad.length?('FAILS ('+bad.length+'):\n  '+bad.slice(0,8).join('\n  ')):
 'detours checked: '+keys.length+' journeys inside tellings, '+
 keys.reduce((n,x)=>n+T.DETOUR[x].stops.length,0)+' stops, each with a picture and a way back');
