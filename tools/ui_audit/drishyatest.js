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
/* every motion must be counted in time, not in frames, so a slow phone behaves the same */
const timed=(page.match(/performance&&performance\.now/g)||[]).length;
if(timed<3)bad.push('some of these scenes still move by frame count, not by the clock');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('visual screens checked: doors, books and tray each open full and wide, name what they show, offer a way back, wait their turn, and move by the clock');
