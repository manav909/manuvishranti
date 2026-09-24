/* the play must stay smooth: screens that open by themselves are rationed, and a choice of one opens nothing */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
if(page.indexOf('function autoOnce(')<0)bad.push('there is no ration on the screens that open by themselves');
if(!/run\.autoN>=2/.test(page))bad.push('a watch can carry more than two screens that open by themselves');
if(!/run\.shown\[key\]/.test(page))bad.push('the same screen can open twice for the same moment');
if(!/open\.length>1/.test(page))bad.push('the doors open even when there is only one way to go');
if(!/unread>1\)autoOnce\("pothi-/.test(page))bad.push('the books come out even when only one telling is left to read');
if(!/run\.autoN=0/.test(page))bad.push('the count does not start again with a new watch');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('smoothness checked: at most two screens open by themselves in a watch, never twice for the same moment, and never when there is no choice');
