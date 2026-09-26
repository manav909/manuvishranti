import re,sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
URL='https://manuvishranti.com/novel/TheFiveWounds'
DESC='The Five Wounds by Manu Vishranti: five novels and a companion diary following one Indian family across sixty years, from a surgeon with clean hands to a man with no surname. Published by Walnut Publication, coming the last week of October 2026.'
old_t='<title>The Five Wounds: Opening and Cast (Prototype 1)</title>'; assert s.count(old_t)==1
head=f'''<title>The Five Wounds by Manu Vishranti: five novels and a companion volume</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="book">
<meta property="og:site_name" content="Manu Vishranti">
<meta property="og:title" content="The Five Wounds by Manu Vishranti">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://manuvishranti.com/novel/TheFiveWounds/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="The Five Wounds by Manu Vishranti">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://manuvishranti.com/novel/TheFiveWounds/img/share.jpg">
<meta name="author" content="Manu Vishranti">
<meta name="theme-color" content="#000000">'''
s=s.replace(old_t,head)
f0=re.findall(r'<footer>.*?</footer>',s,re.S); assert len(f0)==1
_au=re.findall(r'<div class="author">.*?</div>\s*</div>',f0[0],re.S);AUTH=_au[0] if _au else ''
s=s.replace(f0[0],'''<footer>
  '''+AUTH+'''
  <p><i>The Five Wounds</i> by <a href="/">Manu Vishranti</a>. Five novels and a companion volume: <i>Clean Hands</i>, <i>Peacetime</i>, <i>All the Summers at Once</i>, <i>The House of Auspicious Hours</i>, <i>Dead Letter</i> and <i>The Third Woman</i>.</p>
  <p>Published by Walnut Publication. Coming the last week of October 2026. More of his work at <a href="/">manuvishranti.com</a>.</p>
  <p>The drawings in the opening are Nandita’s, from <i>The Third Woman</i>. Every character in these books is fictional, and every face drawn here is invented.</p>
</footer>''')
s=s.replace('src="img/','src="/novel/TheFiveWounds/img/')
open(dst,'w').write(s)
for bad in ['Prototype','claude.ai','Adatia']: assert s.count(bad)==0,bad
print(dst,len(s)//1024,'KB dashes',len(re.findall('[–—]',s)))
