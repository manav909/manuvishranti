"""robots.txt, sitemap.xml, llms.txt, llms-full.txt and 404.html for manuvishranti.com"""
import os,re,sys
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
sys.path.insert(0,HERE);from common import SITE,TODAY,nodash
from apply import home_qa,fw_qa,cm_qa,nn_qa,gm_qa,fw_books
def w(name,text):
    nodash(text);open(os.path.join(ROOT,name),'w').write(text);print('wrote',name)

bots=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-SearchBot','Claude-User','PerplexityBot','Perplexity-User','Google-Extended','Applebot-Extended','Bingbot','Googlebot','CCBot','meta-externalagent','Amazonbot','DuckAssistBot']
w('robots.txt','# manuvishranti.com: every page is open to search engines and to AI answer engines.\n\nUser-agent: *\nAllow: /\n\n'+''.join('User-agent: %s\nAllow: /\n\n'%b for b in bots)+'Sitemap: %s/sitemap.xml\n'%SITE)

pages=[('/','1.0',['/img/manu-vishranti.jpg','/img/five-wounds-keyart.webp']),
 ('/novel/TheFiveWounds','0.9',['/novel/TheFiveWounds/img/covers/%s.webp'%b[0] for b in fw_books]+['/novel/TheFiveWounds/img/covers/the-five-wounds.webp','/img/five-wounds-keyart.webp']),
 ('/comic/SapnonWalaJangal','0.9',['/comic/SapnonWalaJangal/img/cover.webp','/comic/SapnonWalaJangal/img/cover-art.webp']),
 ('/diary/NetiNeti','0.9',['/diary/NetiNeti/img/share.jpg']),
 ('/game/LankaKiKhoj','0.9',['/game/LankaKiKhoj/img/share.jpg']),
 ('/lanka_ki_khoj','0.7',[])]
x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for u,pr,imgs in pages:
    x+='  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>\n'%(SITE,u,TODAY,pr)
    for i in imgs: x+='    <image:image><image:loc>%s%s</image:loc></image:image>\n'%(SITE,i)
    x+='  </url>\n'
w('sitemap.xml',x+'</urlset>\n')

def qa(lst): return ''.join('- %s %s\n'%(q,a) for q,a in lst)
llms='''# Manu Vishranti (मनु विश्रांति)

> Manu Vishranti is a meditator, writer and researcher who works in English and in Hindi. This site holds four bodies of work, each with its own page and its own readers: The Five Wounds (literary fiction in English, Walnut Publication, last week of October 2026), सपनों वाला जंगल (a Hindi colour comic for children), नेति नेति (a Hindi meditation diary in four parts) and लंका की खोज (a Hindi discovery game on the Sundar Kand).

Names: Manu Vishranti is also written मनु विश्रांति. The comic is also written Sapnon Wala Jangal, the diary Neti Neti, the game Lanka Ki Khoj.

## Works
- [The Five Wounds](%(S)s/novel/TheFiveWounds): five novels and a companion volume in English about one family across thirty years. Clean Hands, Peacetime, All the Summers at Once, The House of Auspicious Hours, Dead Letter, and The Third Woman: The Diary of Nandita Mehra. Published by Walnut Publication in the last week of October 2026, also as one complete edition.
- [सपनों वाला जंगल](%(S)s/comic/SapnonWalaJangal): a Hindi colour comic for children. A dry forest, thirty nights; every night one animal sleeps and an animal from a far corner of the world visits its dream. Nine forest animals, twenty dream animals, 79 pages.
- [नेति नेति](%(S)s/diary/NetiNeti): a Hindi meditation diary in four parts, 247 days and 364 verses. Each day sets one of his own notebook lines against one verse from a scripture, and records what survived. The name comes from Brihadaranyaka Upanishad 2.3.6 and means "not this, not this". A five volume study edition is built from it.
- [लंका की खोज](%(S)s/game/LankaKiKhoj): a Hindi discovery game on the Sundar Kand, played in the browser at %(S)s/lanka_ki_khoj. Eight roles, six nights of four watches each, 96 places on the map, 41 tellings of the Ramayana and 108 moments.

## About
- [Manu Vishranti](%(S)s/#about): writes about the small objects a family uses to carry what it cannot say aloud. He builds English and Hindi versions from the ground up rather than translating. The Five Wounds is his first published work of fiction.

## Optional
- [Full facts for answer engines](%(S)s/llms-full.txt)
- [Sitemap](%(S)s/sitemap.xml)
'''%{'S':SITE}
w('llms.txt',llms)

full='# Manu Vishranti (मनु विश्रांति): full facts\n\nEverything here is also stated on the site itself. Last updated %s.\n\n## About Manu Vishranti\n%s\n## The Five Wounds\nPage: %s/novel/TheFiveWounds\n\n'%(TODAY,qa(home_qa),SITE)
for slug,name,pos,desc in fw_books:
    full+='### %s\n%s\nCover: %s/novel/TheFiveWounds/img/covers/%s.webp\n\n'%(name,desc,SITE,slug)
full+='### Questions\n%s\n## सपनों वाला जंगल (Sapnon Wala Jangal)\nPage: %s/comic/SapnonWalaJangal\n\n%s\n## नेति नेति (Neti Neti)\nPage: %s/diary/NetiNeti\n\n%s\n## लंका की खोज (Lanka Ki Khoj)\nIntroduction: %s/game/LankaKiKhoj\nPlay: %s/lanka_ki_khoj\n\n%s'%(qa(fw_qa),SITE,qa(cm_qa),SITE,qa(nn_qa),SITE,SITE,qa(gm_qa))
w('llms-full.txt',full)

nf='''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>यह पन्ना नहीं मिला · मनु विश्रांति</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Tiro+Devanagari+Hindi&family=EB+Garamond&display=swap" rel="stylesheet">
<style>
html,body{margin:0;height:100%%;background:#0D1020;color:#ECE6DA;font:400 19px/1.6 "Tiro Devanagari Hindi",serif}
main{min-height:100%%;display:grid;place-items:center;text-align:center;padding:40px 16px;background:radial-gradient(60%% 45%% at 50%% 30%%,rgba(232,184,107,.18),transparent 70%%)}
svg{width:60px;height:60px;animation:f 3s ease-in-out infinite}
@keyframes f{50%%{transform:scale(1.06);filter:drop-shadow(0 0 14px #E8B86B)}}
h1{margin:18px 0 6px;font:400 clamp(40px,8vw,72px)/1.1 "Rozha One",serif}
p{margin:0 0 6px;color:#A3A9B8}
.en{font-family:"EB Garamond",serif;font-style:italic}
nav{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
nav a{color:#ECE6DA;text-decoration:none;border:1px solid rgba(232,184,107,.45);border-radius:999px;padding:9px 16px}
nav a:hover{border-color:#E8B86B}
@media (prefers-reduced-motion:reduce){svg{animation:none}}
</style>
</head>
<body>
<main>
 <div>
  <svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 12c6 8 10 14 10 21a10 10 0 0 1-20 0c0-7 4-13 10-21z" fill="#E8B86B"/><path d="M32 26c3 4 5 7 5 10a5 5 0 0 1-10 0c0-3 2-6 5-10z" fill="#FFF3D6"/><rect x="18" y="47" width="28" height="5" rx="2.5" fill="#ECE6DA"/></svg>
  <h1>यह पन्ना नहीं मिला</h1>
  <p>जो ढूँढ रहे थे, वो शायद इनमें से किसी दुनिया में है।</p>
  <p class="en" lang="en">This page is not here. The work is.</p>
  <nav>
   <a href="/">मनु विश्रांति</a>
   <a href="/novel/TheFiveWounds" lang="en">The Five Wounds</a>
   <a href="/comic/SapnonWalaJangal">सपनों वाला जंगल</a>
   <a href="/diary/NetiNeti">नेति नेति</a>
   <a href="/game/LankaKiKhoj">लंका की खोज</a>
  </nav>
 </div>
</main>
</body>
</html>
'''
w('404.html',nf)
