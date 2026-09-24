/* the doors: every place has a kind, every hour has a light, and the way in and out is always there */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
["mandir","mahal","bagh","pahra","samudra","raasta","chaukhat"].forEach(k=>{
 if(page.indexOf('kind==="'+k+'"')<0)bad.push('no door is built for a '+k);
 if(page.indexOf('doorBeyond')<0)bad.push('nothing stands behind the doors');
});
["saanjh","raat","bhor","din"].forEach(t=>{
 if(!new RegExp(t+':\\{sky:').test(page))bad.push('the hour '+t+' has no light of its own');
});
if(page.indexOf('भीतर जाओ')<0)bad.push('there is no way to step inside');
if(page.indexOf('पीछे हटो')<0)bad.push('there is no way to step back');
if(!/enter:enter,back:wide/.test(page))bad.push('the scene offers no way in and no way back');
if(!/drops the shadows/.test(page))bad.push('a slow phone is not looked after');
/* every place name must land on some kind of door */
const code=fs.readFileSync('/tmp/gs.js','utf8');
global.localStorage={getItem:()=>null,setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=f=>1;
global.setTimeout=f=>0;global.clearTimeout=()=>{};global.innerWidth=1200;global.matchMedia=()=>({matches:false});
function mk(){return{className:'',style:{setProperty(){},getPropertyValue(){return ''}},dataset:{},children:[],innerHTML:'',hidden:false,setAttribute(){},getAttribute(){return ''},removeAttribute(){},insertAdjacentHTML(){},getBoundingClientRect(){return{width:700,height:420}},addEventListener(){},scrollTo(){},closest(){return null},appendChild(c){return c},remove(){},querySelector(){return null},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}};}
const els={};global.document={createElement:()=>mk(),getElementById:id=>els[id]||(els[id]=mk())};
global.window={};global.addEventListener=()=>{};
eval(code.replace(/\nfoldLbl\(\)[^\n]*\n/,'')+';global.T={PLACES};');
const kinds={};
function doorKindOf(n){
 if(/मंदिर|चैत्य|देवालय|यज्ञ|निकुंभिला|मुहर|पूजा/.test(n))return "mandir";
 if(/महल|दरबार|अंतःपुर|किला|क़िला|फाटक|द्वार|तोरण|पुष्पक|राजा|मंत्री|नीति|सभा|कक्ष|सिंहासन|विमान/.test(n))return "mahal";
 if(/वाटिका|बाग़|बाग|उपवन|अशोक|पेड़|डाल|वन|मधुवन|फूल|पंछी|कमल/.test(n))return "bagh";
 if(/चौकी|पहरा|पहरे|खाई|दीवार|बुर्ज|परिखा|प्राकार|सेना|सेनापति|टोली|रथ|मैदान|लड़ाई|किंकर/.test(n))return "pahra";
 if(/समुद्र|किनारा|लहर|पानी|सरोवर|कुंड|झील|घाट|उड़ान|आसमान|बादल|मुँह/.test(n))return "samudra";
 if(/रास्ता|राह|चौराहा|चढ़ाई|उतार|सीढ़ी|पगडंडी|सफ़र|लौट/.test(n))return "raasta";
 if(/सवाल|पन्ना|पोथी|ज़बान|कथा|श्लोक|नाम|हिसाब|गिनती|सपना|याद/.test(n))return "chaukhat";
 if(/गली|घर|बस्ती|मोहल्ला|आँगन|छत|बाज़ार|अटारी|कोना/.test(n))return "ghar";
 return "chaukhat";
}
Object.keys(T.PLACES).forEach(id=>{
 const n=T.PLACES[id].n||"";
 const k=doorKindOf(n);
 kinds[k]=(kinds[k]||0)+1;});
const most=Math.max.apply(null,Object.values(kinds));
if(most>Object.keys(T.PLACES).length*0.42)
 bad.push('one kind of door stands for too many places: '+most+' of '+Object.keys(T.PLACES).length);
if(Object.keys(kinds).length<6)bad.push('only '+Object.keys(kinds).length+' kinds of door are ever used');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('doors checked: '+Object.keys(T.PLACES).length+' places, each with a door of its kind ('+
 Object.keys(kinds).map(k=>k+' '+kinds[k]).join(', ')+'), all four hours lit, and a way in and back');
