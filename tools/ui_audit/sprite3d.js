/* anything a scene plan can hold must have a shape in 3D, or it vanishes without a word */
const fs=require('fs');const src=fs.readFileSync('/mnt/user-data/outputs/lanka-map3.html','utf8');
const js=src.split('<script>')[1].split('</script>')[0];
const names=new Set();
const re=/\bit:\[(.*?)\],me:/gs;let m;
while((m=re.exec(js))){const part=m[1];const r2=/\["([a-z_]+)"/g;let x;while((x=r2.exec(part)))names.add(x[1]);}
const built=new Set();
const b=js.slice(js.indexOf('const S3B={'), js.indexOf('/* casting'));
const r3=/([a-z_]+)\s*:\s*\([a-z]*\)\s*=>/g;let y;while((y=r3.exec(b)))built.add(y[1]);
/* the casting step can also hand a thing its shape */
const cst=js.slice(js.indexOf('function s3cast'), js.indexOf('function s3role'));
const r4=/name==="([a-z_]+)"/g;let z;while((z=r4.exec(cst)))built.add(z[1]);
const rg=js.slice(js.indexOf('function s3regional'), js.indexOf('const S3REGION'));
const r5=/name==="([a-z_]+)"/g;let w;while((w=r5.exec(rg)))built.add(w[1]);
const roleFall=/^(r_)/;
const missing=[...names].filter(n=>!built.has(n)&&!roleFall.test(n));
if(missing.length)console.log('FAILS: these things stand in a scene plan but have no 3D shape: '+missing.join(', '));
else console.log('shapes checked: all '+names.size+' things a scene can hold have a 3D shape');
