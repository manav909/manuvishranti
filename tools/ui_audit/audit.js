(() => {
  const out = [];
  const parse = c => {
    if (!c) return null;
    let m = c.match(/rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
    m = c.match(/color\(srgb ([^)]+)\)/);
    if (m) { const p = m[1].split(/[ \/]+/).filter(Boolean).map(Number); return [p[0]*255, p[1]*255, p[2]*255, p.length > 3 ? p[3] : 1]; }
    return null;
  };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const blend = (top, under) => { const a = top[3]; return [top[0]*a + under[0]*(1-a), top[1]*a + under[1]*(1-a), top[2]*a + under[2]*(1-a), 1]; };
  const gradStops = bg => { const m = bg.match(/(rgba?\([^)]+\)|color\(srgb [^)]+\))/g); return m ? m.map(parse).filter(Boolean) : []; };
  // what the text is actually painted on
  function backdrop(el) {
    const layers = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      const bgi = cs.backgroundImage;
      if (bgi && bgi !== 'none' && /gradient/.test(bgi)) {
        const st = gradStops(bgi); if (st.length) layers.push({ grad: st });
      }
      const bc = parse(cs.backgroundColor);
      if (bc && bc[3] > 0) { layers.push({ col: bc }); if (bc[3] >= .98) break; }
    }
    let base = parse(getComputedStyle(document.body).backgroundColor) || [255,255,255,1];
    if (base[3] < 1) base = blend(base, [255,255,255,1]);
    // paint from the bottom up; for gradients keep every stop as a candidate
    let cands = [base];
    for (let i = layers.length - 1; i >= 0; i--) {
      const L = layers[i];
      if (L.col) cands = cands.map(c => blend(L.col, c));
      else cands = cands.flatMap(c => L.grad.map(g => blend(g, c)));
    }
    return cands;
  }
  function opacityOf(el) { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity || 1); return o; }
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode; const txt = t.nodeValue.replace(/\s+/g, ' ').trim();
    if (txt.length < 2) continue;
    const el = t.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    if (el.closest('svg')) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    // skip what is scrolled out of any panel or hidden by a closed ancestor
    let hidden = false; for (let n = el; n; n = n.parentElement) { const s = getComputedStyle(n); if (s.display === 'none' || s.visibility === 'hidden') { hidden = true; break; } }
    if (hidden) continue;
    const op = opacityOf(el); if (op < .05) continue;
    let fg = parse(cs.color); if (!fg) continue;
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const large = size >= 24 || (bold && size >= 18.66);
    const need = large ? 3 : 4.5;
    const bgs = backdrop(el);
    let worst = 99, worstBg = null;
    bgs.forEach(bg => { const f = blend([fg[0], fg[1], fg[2], fg[3] * op], bg); const c = ratio(f, bg); if (c < worst) { worst = c; worstBg = bg; } });
    if (worst < need) out.push({ kind: 'contrast', text: txt.slice(0, 40), ratio: +worst.toFixed(2), need, cls: el.className && String(el.className).slice(0, 40), tag: el.tagName, size: Math.round(size) });
    if (size < 11.5) out.push({ kind: 'tiny', text: txt.slice(0, 40), size, cls: String(el.className).slice(0, 40) });
    // text cut off inside its own box
    if ((cs.overflow === 'hidden' || cs.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 2 && cs.whiteSpace !== 'normal')
      out.push({ kind: 'clipped', text: txt.slice(0, 40), cls: String(el.className).slice(0, 40) });
  }
  // the page must never scroll sideways
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 1) out.push({ kind: 'sideways', text: 'page is ' + de.scrollWidth + ' wide in a ' + de.clientWidth + ' view' });
  // things poking out of the screen
  document.querySelectorAll('button, .chip, .do, p, h1, h2, h3').forEach(b => {
    const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
    if (cs.display === 'none' || r.width === 0) return;
    if (r.right > innerWidth + 2 && r.left < innerWidth) out.push({ kind: 'offscreen', text: (b.textContent || '').trim().slice(0, 40), cls: String(b.className).slice(0, 40) });
  });
  // buttons a finger cannot hit on a phone
  if (innerWidth < 500) document.querySelectorAll('button:not(.link)').forEach(b => {
    const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
    if (cs.display === 'none' || cs.visibility === 'hidden' || r.width === 0) return;
    if (r.height < 30 || r.width < 30) out.push({ kind: 'small-target', text: (b.textContent || b.getAttribute('aria-label') || '').trim().slice(0, 30), h: Math.round(r.height), w: Math.round(r.width), cls: String(b.className).slice(0, 30) });
  });
  // buttons with nothing to say
  document.querySelectorAll('button').forEach(b => {
    const cs = getComputedStyle(b); if (cs.display === 'none') return;
    const r = b.getBoundingClientRect(); if (r.width === 0) return;
    if (!(b.textContent || '').trim() && !b.getAttribute('aria-label')) out.push({ kind: 'mute-button', cls: String(b.className).slice(0, 40) });
  });
  // words that only a broken program writes
  const bad=/\b(undefined|NaN|null|\[object Object\])\b/;
  const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(tw.nextNode()){const n=tw.currentNode;const el=n.parentElement;if(!el)continue;
    const r=el.getBoundingClientRect();if(r.width<1)continue;
    let hid=false;for(let a=el;a;a=a.parentElement){const s=getComputedStyle(a);if(s.display==='none'||s.visibility==='hidden'){hid=true;break;}}
    if(!hid&&bad.test(n.nodeValue))out.push({kind:'broken-text',text:n.nodeValue.trim().slice(0,60),cls:String(el.className).slice(0,30)});}
  return out;
})()
