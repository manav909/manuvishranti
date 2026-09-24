/* every colour name the page uses must actually exist, and none may be lost to a missing semicolon */
const fs=require('fs');const page=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const bad=[];
const css=page.split('<style')[1]?page.split('<style')[1].split('</style>')[0]:'';
if(!css)bad.push('no style block found');
/* what is defined */
const defined=new Set();
/* a name may be set in the style block, in an inline style, or handed over from the code */
(page.match(/--[a-zA-Z0-9_-]+\s*:/g)||[]).forEach(d=>defined.add(d.split(':')[0].trim()));
(page.match(/setProperty\(\s*["']--[a-zA-Z0-9_-]+/g)||[]).forEach(d=>defined.add(d.replace(/.*["']/,'').trim()));
/* what is used */
const used=new Set();
(css.match(/var\(\s*--[a-zA-Z0-9_-]+/g)||[]).forEach(u=>used.add(u.replace(/var\(\s*/,'').trim()));
(page.match(/var\(\s*--[a-zA-Z0-9_-]+/g)||[]).forEach(u=>used.add(u.replace(/var\(\s*/,'').trim()));
const missing=[...used].filter(u=>!defined.has(u));
if(missing.length)bad.push('these colour names are used but never set: '+missing.slice(0,8).join(', '));
/* a declaration that forgets its semicolon swallows the next one */
const lines=css.split('\n');
lines.forEach((ln,i)=>{
 const t=ln.trim();
 if(!t||t.startsWith('/*')||t.startsWith('*')||t.endsWith('{')||t.endsWith('}')||t.endsWith(';')||t.endsWith(',')||t.startsWith('@'))return;
 const next=(lines[i+1]||'').trim();
 if(/^--/.test(next)&&/:/.test(t))bad.push('line '+(i+1)+' has no semicolon, so the colour name after it is lost: '+t.slice(0,46));
});
/* the palm leaf page must keep its own colours */
["--leaf1","--leafInk","--leafWood1"].forEach(k=>{
 if(!defined.has(k))bad.push('the palm leaf page lost its colour '+k);});
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('colour names checked: '+defined.size+' names set, '+used.size+' used, none missing, none lost to a missing semicolon');
