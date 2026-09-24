#!/bin/bash
# every check must run to its end and say it passed: a crash is a failure, not a pass
pass=0; fail=0
for f in vastutest linktest layouttest sidetest sanity langtest playtest cardtest quiztest threadtest \
 gifttest scrolltest2 onecardtest flowtest scrolltest repeattest paneltest blocktest minitest camtest \
 viewtest overlap mousetest panetest textstest bhenttest adhikartest padvitest diotest tourtest deeptest \
 findtest kahitest ghaditest roletest feeltest formattest dupetest pixtest covertest kathatest detourtest \
 sprite3d muhimtest raattest doortest drishyatest smoothtest rangtest vajantest; do
  out=$(node /tmp/$f.js 2>&1); code=$?
  if [ $code -ne 0 ]; then echo "== $f टूट गई"; echo "$out" | head -3; fail=$((fail+1))
  elif echo "$out" | grep -qi fail; then echo "== $f"; echo "$out" | head -3; fail=$((fail+1))
  elif ! echo "$out" | grep -qiE 'checked|passed|no overlap'; then echo "== $f ने कुछ नहीं कहा"; fail=$((fail+1))
  else pass=$((pass+1)); fi
done
echo "पास: $pass | फ़ेल: $fail"
