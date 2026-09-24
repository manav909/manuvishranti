/* the game must stay light enough to open on a slow phone */
const fs=require('fs'),zlib=require('zlib');
const raw=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html');
const gz=zlib.gzipSync(raw,{level:9}).length;
const budget=430*1024;            /* what a phone on a weak line can pull without giving up */
const warn=400*1024;
const bad=[];
if(gz>budget)bad.push('the game weighs '+(gz/1024).toFixed(0)+' KB pressed, over the '+(budget/1024)+' KB budget');
if(bad.length)console.log('FAILS:\n  '+bad.join('\n  '));
else console.log('weight checked: '+(raw.length/1024/1024).toFixed(2)+' MB raw, '+(gz/1024).toFixed(0)+
 ' KB pressed, budget '+(budget/1024)+' KB'+(gz>warn?' (close to the line)':''));
