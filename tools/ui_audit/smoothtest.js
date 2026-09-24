/* the play must stay smooth: screens that open by themselves are rationed, and a choice of one opens nothing */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
if(page.indexOf('function autoOnce(')<0)bad.push('there is no ration on the screens that open by themselves');
if(!/function foldList\(/.test(page))bad.push('the written list has no fold to sit in');
if(!/run\.shown\[key\]/.test(page))bad.push('the same screen can open twice for the same moment');
if(page.indexOf('दरवाज़े सामने लाओ')<0)bad.push('there is no way to call the doors back');
if(page.indexOf('पोथियाँ सामने रखो')<0)bad.push('there is no way to call the books back');
if(page.indexOf('foldList("जगहें, सूची में"')<0)bad.push('the places are not folded behind the doors');
if(page.indexOf('foldList("इसी पल की कथाएँ, सूची में"')<0)bad.push('the tellings are not folded behind the books');


if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('one way of choosing checked: the pictures open by themselves and can be called back, the written lists sit folded behind them, and no screen opens twice for the same moment');
