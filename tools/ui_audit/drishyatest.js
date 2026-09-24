/* the three screens that carry the game without words: doors, books, tray */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
/* each screen must exist, be built in 3D, and be reachable */
[["doorScene","the doors"],["scrollScene","the books on the table"],["trayScene","the tray of finds"]].forEach(([fn,what])=>{
 if(page.indexOf("function "+fn+"(")<0)bad.push(what+" have no scene of their own");
 if(page.indexOf(fn)===page.lastIndexOf(fn))bad.push(what+" are built but never opened");
});
/* every one of them must name what it shows, and offer a way back */
[["darwazeOpen","नक्शे पर लौटो"],["pothiOpen","कथा पर लौटो"],["thaalOpen","कथा पर लौटो"]].forEach(([fn,back])=>{
 const i=page.indexOf("function "+fn+"(");
 if(i<0){bad.push(fn+" is missing");return;}
 const seg=page.slice(i,i+2600);
 if(seg.indexOf("bigShow")<0)bad.push(fn+" does not open a full screen");
 if(seg.indexOf(back)<0)bad.push(fn+" offers no way back");
 if(seg.indexOf("wide:true")<0)bad.push(fn+" does not use the wide screen");
});
/* only one full screen at a time, and a hand-asked one comes first */
if(page.indexOf("function stageAsk(")<0)bad.push('there is no queue for the full screens');
/* the tray must be what the basket opens */
if(page.indexOf("if(!thaalDikhao(basket))")<0)bad.push('tapping the basket no longer brings out the tray');
if(!/mine&&busy\.dataset\.auto==="1"/.test(page))bad.push('a screen the player asked for cannot push aside an automatic one');
/* names on things, so nothing needs a written list beside it */
["CanvasTexture","SpriteMaterial"].forEach(k=>{
 if(page.indexOf(k)<0)bad.push('the things carry no name boards ('+k+')');});
/* a picture alone is not enough: the same choices must stand as plain buttons, read aloud and reachable */
if(page.indexOf('function sunoList(')<0)bad.push('the pictures carry no plain list beside them');
if(page.indexOf('.srlist{')<0)bad.push('the plain list has no place to stand');
if(!/cv\.setAttribute\("aria-label"/.test(page))bad.push('the picture has no name to be read aloud');
['darwazeOpen','pothiOpen','thaalOpen'].forEach(fn=>{
 const i=page.indexOf('function '+fn+'(');
 if(i<0)return;
 if(page.slice(i,i+2600).indexOf('sunoList(')<0)bad.push(fn+' offers no plain list of its choices');});
/* the pictures must also answer to a keyboard, not only to a finger */
['doorScene','scrollScene','trayScene'].forEach(fn=>{
 const i=page.indexOf('function '+fn+'(');
 if(i<0)return;
 const seg=page.slice(i,i+9000);
 if(seg.indexOf('canvas.onkeydown')<0)bad.push(fn+' cannot be used with a keyboard');
 if(seg.indexOf('canvas.tabIndex')<0)bad.push(fn+' cannot even be reached by the tab key');
 if(seg.indexOf('"ArrowRight"')<0)bad.push(fn+' does not answer to the arrow keys');
 if(seg.indexOf('"Enter"')<0)bad.push(fn+' has no key that chooses');});
/* less movement: the scenes must hold still when the player has asked for that */
if(page.indexOf('function lessMove(')<0)bad.push('the scenes do not know about the less movement setting');
['doorScene','scrollScene','trayScene'].forEach(fn=>{
 const i=page.indexOf('function '+fn+'(');
 if(i<0)return;
 if(page.slice(i,i+7000).indexOf('lessMove()')<0&&page.slice(i,i+7000).indexOf('calm')<0)
  bad.push(fn+' keeps moving even when the player asked for less movement');});
if(page.indexOf('.bigshow.calm .brays')<0)bad.push('the full screen show keeps its rays and petals moving in calm');
if(!/host\.classList\.toggle\("calm"/.test(page))bad.push('the show does not carry the calm setting, since it lives outside the game box');
/* every motion must be counted in time, not in frames, so a slow phone behaves the same */
const timed=(page.match(/performance&&performance\.now/g)||[]).length;
if(timed<3)bad.push('some of these scenes still move by frame count, not by the clock');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('visual screens checked: doors, books and tray each open full and wide, name what they show, offer a way back, wait their turn, and move by the clock');
