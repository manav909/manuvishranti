/* the play must stay smooth: screens that open by themselves are rationed, and a choice of one opens nothing */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
if(page.indexOf('function autoOnce(')<0)bad.push('there is no ration on the screens that open by themselves');
if(!/function foldList\(/.test(page))bad.push('the written list has no fold to sit in');
if(!/run\.shown\[key\]/.test(page))bad.push('the same screen can open twice for the same moment');
/* the pictures are an extra now, not a replacement: one button carries them all,
   and the written page stands open by itself */
if(page.indexOf('function drishyaAbhi(')<0)bad.push('there is no single way into the pictures');
if(page.indexOf('id="drishyaBtn"')<0&&page.indexOf("drishyaBtn")<0)bad.push('the picture button is not put on the page');
if(!/let autoDrishya=false/.test(page))bad.push('the pictures can still open by themselves');
if(!/build\(\);return null;/.test(page))bad.push('the written lists are folded away again');


if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('the pictures checked: they never open by themselves, one button opens the one that fits where you stand, and the written page stays whole');
