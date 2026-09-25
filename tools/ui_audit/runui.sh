#!/bin/bash
# the three browser checks, one after another, each with its own patience
cd /tmp/ui
out(){ python3 - "$1" "$2" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[2]))
except Exception:
    print(sys.argv[1],'| पूरी नहीं हुई'); raise SystemExit
n=len(d.get('issues',[]))
ok=d.get('ok') or d.get('steps') or []
print('%s | %d बातें पास | %d शिकायतें'%(sys.argv[1],len(ok),n))
for i in d.get('issues',[])[:6]:
    print('   ✗', i if isinstance(i,str) else (i.get('where','')+' | '+i.get('msg','')))
PY
}
timeout 280 python3 puranatest.py > pt.json 2>&1; out "पुराना खेल" pt.json
timeout 280 python3 bahav.py     > bh.json 2>&1; out "पूरा बहाव"  bh.json
# the layout check builds every 3D scene, so it is slow: run it on its own
if [ "$1" = "all" ]; then
  timeout 280 python3 vislayout.py phone > vl.json 2>&1; out "दृश्यों की बनावट" vl.json
else
  echo 'दृश्यों की बनावट | अलग चलाओ: ./runui.sh all'
fi
