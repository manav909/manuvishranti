"""Search, answer engine and AI engine markup for every page of manuvishranti.com.
Run from anywhere: python3 tools/seo/apply.py
Idempotent: each page keeps its markup between <!-- seo:start --> / <!-- seo:end --> (in <head>)
and <!-- faq:start --> / <!-- faq:end --> (in <body>)."""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
sys.path.insert(0,HERE)
from common import *

def put(s, anchor, block, tag):
    a='<!-- %s:start -->'%tag; b='<!-- %s:end -->'%tag
    if a in s:
        i=s.index(a); j=s.index(b,i)+len(b); return s[:i]+a+'\n'+block+'\n'+b+s[j:]
    assert anchor in s, (tag, anchor[:40])
    return s.replace(anchor, a+'\n'+block+'\n'+b+'\n'+anchor, 1)

def strip_old_ld(s):
    head=s[:s.index('</head>')]
    seo=re.search(r'<!-- seo:start -->.*?<!-- seo:end -->',head,re.S)
    keep=seo.group(0) if seo else ''
    h2=head.replace(keep,'@@SEO@@') if keep else head
    h2=re.sub(r'<script type="application/ld\+json">.*?</script>\s*','',h2,flags=re.S)
    h2=h2.replace('@@SEO@@',keep)
    return h2+s[len(head):]

def set_meta(s, title=None, desc=None):
    if title: s=re.sub(r'<title>.*?</title>','<title>%s</title>'%title,s,count=1,flags=re.S)
    if desc: s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="%s">'%desc,s,count=1)
    return s

def write(path,s):
    nodash(s); open(path,'w').write(s); print('wrote',os.path.relpath(path,ROOT))

FAQ_CSS={}
# ------------------------------------------------------------------ home
HOME=SITE+'/'
home_qa=[
 ("Who is Manu Vishranti?","Manu Vishranti (मनु विश्रांति) is a meditator, writer and researcher. He writes in English and in Hindi, building each version from the ground up rather than translating."),
 ("What has Manu Vishranti made?","The Five Wounds, five novels and a companion volume in English; सपनों वाला जंगल, a Hindi comic for children; नेति नेति, a meditation diary in four parts, in Hindi; and लंका की खोज, a Hindi discovery game on the Sundar Kand."),
 ("When does The Five Wounds come out?","Walnut Publication brings out The Five Wounds in the last week of October 2026, as six books and as one complete edition."),
 ("Is सपनों वाला जंगल for children?","Yes. It is a colour comic in Hindi made for children, set in a dry forest over thirty nights."),
 ("Where can I play लंका की खोज?","In the browser, at manuvishranti.com/lanka_ki_khoj. Its introduction is at manuvishranti.com/game/LankaKiKhoj."),
 ("What does the name Manu Vishranti mean?","Manu is the one who thinks, in the old stories the first of us. Vishranti is rest, the moment the mind settles back into itself."),
]
def home():
    p=os.path.join(ROOT,'index.html'); s=open(p).read()
    s=strip_old_ld(s)
    s=set_meta(s,'Manu Vishranti (मनु विश्रांति): novels, a comic, a meditation diary and a game',
      'Manu Vishranti (मनु विश्रांति), meditator, writer and researcher: The Five Wounds novels, the Hindi comic सपनों वाला जंगल, the diary नेति नेति and the game लंका की खोज.')
    person=dict(PERSON); person.update({"jobTitle":"Meditator, writer and researcher","description":"Manu Vishranti writes about the small objects a family uses to carry what it cannot say aloud. He works in English and in Hindi, and also writes on meditation. The Five Wounds is his first published work of fiction.",
      "image":SITE+"/img/manu-vishranti.jpg","knowsLanguage":["en","hi"],"knowsAbout":["Fiction","Meditation","Upanishads","Ramayana","Sundar Kand"],
      "mainEntityOfPage":HOME,
      "subjectOf":[{"@id":SITE+"/novel/TheFiveWounds#series"},{"@id":SITE+"/comic/SapnonWalaJangal#book"},{"@id":SITE+"/diary/NetiNeti#book"},{"@id":SITE+"/game/LankaKiKhoj#game"}]})
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"WebSite","@id":HOME+"#site","url":HOME,"name":"Manu Vishranti","alternateName":"मनु विश्रांति","inLanguage":["en","hi"],"publisher":{"@id":PERSON["@id"]}},
      {"@type":"ProfilePage","@id":HOME+"#page","url":HOME,"name":"Manu Vishranti","isPartOf":{"@id":HOME+"#site"},"mainEntity":{"@id":PERSON["@id"]},"dateModified":TODAY,"inLanguage":"en"},
      person,
      {"@type":"BookSeries","@id":SITE+"/novel/TheFiveWounds#series","name":"The Five Wounds","url":SITE+"/novel/TheFiveWounds","author":{"@id":PERSON["@id"]}},
      {"@type":"Book","@id":SITE+"/comic/SapnonWalaJangal#book","name":"सपनों वाला जंगल","alternateName":"Sapnon Wala Jangal","url":SITE+"/comic/SapnonWalaJangal","author":{"@id":PERSON["@id"]}},
      {"@type":"Book","@id":SITE+"/diary/NetiNeti#book","name":"नेति नेति","alternateName":"Neti Neti","url":SITE+"/diary/NetiNeti","author":{"@id":PERSON["@id"]}},
      {"@type":"VideoGame","@id":SITE+"/game/LankaKiKhoj#game","name":"लंका की खोज","alternateName":"Lanka Ki Khoj","url":SITE+"/game/LankaKiKhoj","author":{"@id":PERSON["@id"]}},
      faq_ld(HOME,home_qa)]}
    s=put(s,'<link rel="preconnect" href="https://fonts.googleapis.com">',ld(graph),'seo')
    css='''<style>
.faq{padding:clamp(60px,8vw,110px) 0;border-top:1px solid rgba(236,230,218,.08)}
.faq-in{box-sizing:border-box;width:min(100%,900px);margin:0 auto;padding-inline:max(16px,4vw)}
.faq-k{margin:0 0 8px;font:500 13px/1 var(--latin);letter-spacing:.34em;text-transform:uppercase;color:var(--ash)}
.faq h2{margin:0 0 22px;font:400 clamp(34px,4vw,52px)/1.1 var(--bodoni);color:var(--moon)}
.faq details{border-top:1px solid rgba(236,230,218,.14)}
.faq details:last-child{border-bottom:1px solid rgba(236,230,218,.14)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;padding:16px 0;font:400 clamp(19px,1.8vw,22px)/1.35 var(--latin);color:var(--moon)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--lamp);font-size:24px;line-height:1;transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0 0 18px;max-width:62ch;color:#CFCAD8}
</style>'''
    block=css+'\n'+faq_html('Questions people ask',home_qa,kick='About the work')
    s=put(s,'</div>\n\n<!-- The Five Wounds -->',block,'faq')
    # one h1 only: the Lanka world's title is a heading two on this page
    s=s.replace('<h1 class="gi-title" id="giTitle">','<h2 class="gi-title" id="giTitle">').replace('लंका की खोज</h1>','लंका की खोज</h2>')
    s=s.replace('h1.gi-title','.gi-title')
    write(p,s)

# ------------------------------------------------------------------ The Five Wounds (source prototype, then make_live)
FW=SITE+'/novel/TheFiveWounds'
fw_books=[
 ('clean-hands','Clean Hands',1,'Dev Mehra has four hundred surgeries behind him and not one death, and the steel frame in the hospital lobby says so. What it does not say is how the record was built: by never touching a patient he might lose. Across the river, in a worn hospital with a wall of photographs, another surgeon has been taking the ones Dev sends away. When a schoolteacher collapses in her classroom and her name reaches both hospitals on the same afternoon, twenty years of arrangement begin to come apart, one transfer form at a time.'),
 ('peacetime','Peacetime',2,'A woman who counted a whole town and left one line in a register.'),
 ('all-the-summers-at-once','All the Summers at Once',3,"For forty years Prem Babu made certain that other people’s words arrived. One letter did not, and he is the reason it did not. Now, with ten months left and a house gone quiet, he sets out to find the child that letter was addressed to, who is a grown man somewhere and does not know he was ever written to."),
 ('the-house-of-auspicious-hours','The House of Auspicious Hours',4,'In the Malhotra house, time is a bazaar. Three generations have bought their whole lives in the sanctioned hours of one family almanac: marriages, businesses, the day a child may be born. The longest and the loudest of the five.'),
 ('dead-letter','Dead Letter',5,'Ashu has no surname and has never needed one. Thirteen months after his uncle dies, a registered letter arrives, posted before that death and paid for in advance. Five letters, each with its own condition, and the fifth burns the others if he asks for it.'),
 ('the-third-woman','The Third Woman: The Diary of Nandita Mehra',6,'There is a person in every family who is told last. Nandita Mehra kept an account of a family that told her nothing. Her diary crosses all five novels from a seat nobody thought to look at. A companion volume, not a sixth novel.'),
]
fw_qa=[
 ("What is The Five Wounds?","A series by Manu Vishranti: five novels and a companion volume about one family across thirty years, and the small arrangements that hold a house together until somebody asks what they cost."),
 ("What are the books, in order?","Book One, Clean Hands. Book Two, Peacetime. Book Three, All the Summers at Once. Book Four, The House of Auspicious Hours. Book Five, Dead Letter. And a companion volume, The Third Woman: The Diary of Nandita Mehra."),
 ("Is The Third Woman a sixth novel?","No. It is a companion volume: the diary of Nandita Mehra, which crosses all five novels from a seat nobody thought to look at."),
 ("When and by whom is it published?","Walnut Publication publishes The Five Wounds in the last week of October 2026. There is also a complete edition with the whole series in one."),
 ("Who wrote The Five Wounds?","Manu Vishranti, a meditator, writer and researcher who works in English and in Hindi. The Five Wounds is his first published work of fiction."),
 ("Are the characters real people?","No. Every character in these books is fictional, and every face drawn on this site is invented."),
]
def fivewounds():
    src='/home/claude/fw/five-wounds-opening-and-cast.html'
    s=open(src).read()
    s=strip_old_ld(s)
    parts=[]
    for slug,name,pos,desc in fw_books:
        b={"@type":"Book","@id":FW+"#book-"+slug,"name":name,"url":FW+"#book-"+slug,"position":pos,"description":desc,
           "image":FW+"/img/covers/"+slug+".webp","inLanguage":"en","author":{"@id":PERSON["@id"]},"publisher":{"@id":PUBLISHER["@id"]},"isPartOf":{"@id":FW+"#series"}}
        if pos==6: b["genre"]="Companion volume"
        else: b["bookEdition"]="Book "+["One","Two","Three","Four","Five"][pos-1]; b["genre"]="Literary fiction"
        parts.append(b)
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":FW+"#page","url":FW,"name":"The Five Wounds by Manu Vishranti","isPartOf":{"@id":SITE+"/#site"},"about":{"@id":FW+"#series"},"breadcrumb":{"@id":FW+"#crumbs"},"inLanguage":"en","dateModified":TODAY,"primaryImageOfPage":FW+"/img/share.jpg"},
      {"@type":"BookSeries","@id":FW+"#series","name":"The Five Wounds","url":FW,"description":"Five novels and one companion volume. One family, thirty years, and the small arrangements that hold a house together until somebody asks what they cost.",
       "author":{"@id":PERSON["@id"]},"publisher":{"@id":PUBLISHER["@id"]},"inLanguage":"en","genre":"Literary fiction","image":FW+"/img/covers/the-five-wounds.webp","hasPart":[{"@id":b["@id"]} for b in parts]},
      {"@type":"Book","@id":FW+"#book-the-five-wounds","name":"The Five Wounds (complete edition)","url":FW+"#book-the-five-wounds","description":"The complete series in one edition: five novels and one companion volume.","image":FW+"/img/covers/the-five-wounds.webp","inLanguage":"en","author":{"@id":PERSON["@id"]},"publisher":{"@id":PUBLISHER["@id"]}},
      *parts, PERSON, PUBLISHER, crumbs(FW,"The Five Wounds"), faq_ld(FW,fw_qa)]}
    s=put(s,'<link rel="preconnect" href="https://fonts.googleapis.com">',ld(graph),'seo')
    css='''<style>
.faq{max-width:1180px;margin:0 auto;padding:12vh 6vw 4vh}
.faq-in{max-width:880px}
.faq-k{margin:0 0 14px;font:500 12px/1 "EB Garamond",serif;letter-spacing:.34em;text-transform:uppercase;color:var(--bone2)}
.faq h2{margin:0 0 26px;font:400 clamp(36px,5vw,64px)/1.05 "Bodoni Moda",serif;color:var(--bone)}
.faq details{border-top:1px solid rgba(236,226,200,.14)}
.faq details:last-child{border-bottom:1px solid rgba(236,226,200,.14)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;padding:18px 0;font:italic 400 clamp(20px,1.9vw,24px)/1.3 "EB Garamond",serif;color:var(--bone)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-style:normal;color:var(--foil);font-size:24px;line-height:1;transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0 0 20px;max-width:62ch;color:var(--bone2)}
</style>'''
    s=put(s,'<section id="author"',css+'\n'+faq_html('Questions readers ask',fw_qa,kick='The Five Wounds'),'faq')
    open(src,'w').write(nodash(s)); print('wrote',src)
    ml=os.path.join(ROOT,'tools','make_live_fivewounds.py')
    t=open(ml).read()
    t=t.replace("<title>The Five Wounds by Manu Vishranti</title>","<title>The Five Wounds by Manu Vishranti: five novels and a companion volume</title>")
    open(ml,'w').write(t)
    os.system('python3 "%s" "%s" "%s"'%(ml,src,os.path.join(ROOT,'novel','TheFiveWounds','index.html')))

# ------------------------------------------------------------------ comic
CM=SITE+'/comic/SapnonWalaJangal'
cm_qa=[
 ("सपनों वाला जंगल क्या है?","यह बच्चों के लिए हिंदी में एक रंगीन कॉमिक है। एक सूखा जंगल है और तीस रातें हैं। हर रात कोई जानवर सोता है, और सपने में दुनिया के किसी दूर कोने का जानवर उससे मिलने आता है।"),
 ("इसमें कौन कौन से जानवर हैं?","जंगल के नौ जानवर हैं: काला पंछी, हथिनी, भालू, कछुआ, मोर, अजगर, गिद्ध, बाघिन और चींटीखोर। सपनों में बीस और जानवर आते हैं, दुनिया भर से।"),
 ("सपनों का नियम क्या है?","ताक़त माँगोगे तो चलेगी नहीं। सीख लोगे, तो काम आएगी।"),
 ("क्या जानवरों के बारे में लिखी बातें सच हैं?","हाँ। इस किताब में हर जानवर के बारे में जो लिखा है, वो सच है।"),
 ("किताब में कितने पन्ने हैं?","79 रंगीन पन्ने।"),
 ("यह कॉमिक किसकी है?","मनु विश्रांति की। उनके उपन्यास, ध्यान डायरी और खेल भी manuvishranti.com पर हैं।"),
]
def comic():
    p=os.path.join(ROOT,'comic','SapnonWalaJangal','index.html'); s=open(p).read()
    s=strip_old_ld(s)
    s=set_meta(s,'सपनों वाला जंगल (Sapnon Wala Jangal): बच्चों के लिए हिंदी कॉमिक · मनु विश्रांति',None)
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":CM+"#page","url":CM,"name":"सपनों वाला जंगल","isPartOf":{"@id":SITE+"/#site"},"about":{"@id":CM+"#book"},"breadcrumb":{"@id":CM+"#crumbs"},"inLanguage":"hi","dateModified":TODAY},
      {"@type":"Book","@id":CM+"#book","name":"सपनों वाला जंगल","alternateName":"Sapnon Wala Jangal","alternativeHeadline":"जहाँ हर जानवर किसी और का सपना देखता है","url":CM,
       "description":"बच्चों के लिए हिंदी में एक रंगीन कॉमिक। एक सूखा जंगल, तीस रातें, और हर रात कोई जानवर दुनिया के किसी दूर कोने के जानवर का सपना देखता है।",
       "genre":["Comic","Children's literature"],"inLanguage":"hi","numberOfPages":79,"image":CM+"/img/cover.webp","author":{"@id":PERSON["@id"]},
       "audience":{"@type":"PeopleAudience","audienceType":"children"},"about":["जानवर","जंगल","सपने"]},
      PERSON, crumbs(CM,"सपनों वाला जंगल"), faq_ld(CM,cm_qa)]}
    s=put(s,'<link rel="preconnect" href="https://fonts.googleapis.com">',ld(graph),'seo')
    css='''<style>
.faq{background:var(--night2);padding:clamp(60px,8vw,100px) 0;border-top:4px solid #000}
.faq-in{box-sizing:border-box;width:min(100%,900px);margin:0 auto;padding-inline:max(16px,4vw)}
.faq-k{display:inline-block;margin:0 0 12px;background:#fff;color:#000;border:3px solid #000;box-shadow:4px 4px 0 #000;padding:4px 12px 2px;font:700 15px/1.3 var(--f);transform:rotate(-2deg)}
.faq h2{margin:0 0 20px;font:800 clamp(34px,5vw,56px)/1.1 var(--f);color:var(--gold);-webkit-text-stroke:2px #000;paint-order:stroke fill;text-shadow:4px 4px 0 #000}
.faq details{background:#fff;color:#15100A;border:3px solid #000;box-shadow:5px 5px 0 #000;border-radius:6px;margin:0 0 14px;padding:0 16px}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:12px;padding:14px 0;font:700 clamp(18px,1.8vw,21px)/1.4 var(--f)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:26px;line-height:1;color:var(--sun);transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0 0 16px;font:500 18px/1.6 var(--f)}
</style>'''
    s=put(s,'<footer>',css+'\n'+faq_html('पूछे जाने वाले सवाल',cm_qa,kick='सवाल जवाब'),'faq')
    write(p,s)

# ------------------------------------------------------------------ diary
NN=SITE+'/diary/NetiNeti'
nn_qa=[
 ("नेति नेति क्या है?","नेति नेति मनु विश्रांति की ध्यान डायरी है, चार भागों में। हर दिन उनकी अपनी एक पंक्ति होती है, उसके सामने किसी ग्रंथ का एक श्लोक, और नीचे उनका हिसाब, कि उस भिड़ंत में से क्या बचा।"),
 ("नेति नेति का मतलब क्या है?","यह नहीं, यह नहीं। यह शब्द बृहदारण्यक उपनिषद् २.३.६ से आया है: अथात आदेशो नेति नेति।"),
 ("इसके चार भाग कौन से हैं?","पहला भाग मृत्यु और काल, दूसरा छाया और प्राण, तीसरा प्रकाश, आत्मा और ध्वनि, और चौथा आयाम। चारों में मिलाकर दो सौ सैंतालीस दिन हैं।"),
 ("क्या इसे पढ़ने के लिए संस्कृत आनी चाहिए?","संस्कृत जानना ज़रूरी नहीं। हर श्लोक के नीचे उसका अर्थ है। हर पाठ और संख्या छपी हुई प्रति से मिलाई गई है, और जो न मिला वह छपा नहीं।"),
 ("यह किताब किसके लिए है?","यह उसके लिए है जिसके पास अपनी कोई बात है। जिसने कभी कुछ ऐसा सोचा या महसूस किया हो जो उसे सच लगा, पर जिसे वह आज तक किसी के सामने रख नहीं सका।"),
 ("अध्ययन संस्करण क्या है?","इन्हीं किताबों से बना पाँच खंडों का अध्ययन संस्करण भी है: मृत्यु और काल, छाया प्राण और डर, प्रकाश आत्मा और ध्वनि, आयाम और शब्द, काम घर और चोट।"),
]
def diary():
    p=os.path.join(ROOT,'diary','NetiNeti','index.html'); s=open(p).read()
    s=strip_old_ld(s)
    s=set_meta(s,'नेति नेति (Neti Neti): एक ध्यान यात्रा · मनु विश्रांति',None)
    parts=[("पहला भाग","मृत्यु और काल"),("दूसरा भाग","छाया और प्राण"),("तीसरा भाग","प्रकाश, आत्मा और ध्वनि"),("चौथा भाग","आयाम")]
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":NN+"#page","url":NN,"name":"नेति नेति","isPartOf":{"@id":SITE+"/#site"},"about":{"@id":NN+"#book"},"breadcrumb":{"@id":NN+"#crumbs"},"inLanguage":"hi","dateModified":TODAY},
      {"@type":"Book","@id":NN+"#book","name":"नेति नेति","alternateName":["Neti Neti","नेति नेति: एक ध्यान यात्रा"],"alternativeHeadline":"एक ध्यान यात्रा","url":NN,
       "description":"मनु विश्रांति की ध्यान डायरी, चार भागों में। हर दिन उनकी अपनी एक पंक्ति, उसके सामने किसी ग्रंथ का एक श्लोक, और नीचे हिसाब कि क्या बचा। दो सौ सैंतालीस दिन, तीन सौ चौंसठ श्लोक।",
       "genre":["Meditation diary","Spirituality"],"inLanguage":"hi","author":{"@id":PERSON["@id"]},"image":NN+"/img/share.jpg",
       "about":["ध्यान","उपनिषद्","भगवद्गीता","महाभारत"],
       "hasPart":[{"@type":"Book","name":"नेति नेति, %s: %s"%(a,b),"position":i+1,"inLanguage":"hi"} for i,(a,b) in enumerate(parts)]},
      PERSON, crumbs(NN,"नेति नेति"), faq_ld(NN,nn_qa)]}
    s=put(s,'<link rel="preconnect" href="https://fonts.googleapis.com">',ld(graph),'seo')
    css='''<style>
.faq{position:relative;padding:clamp(70px,9vw,120px) 0;background:var(--ink)}
.faq-in{box-sizing:border-box;width:min(100%,900px);margin:0 auto;padding-inline:max(16px,5vw)}
.faq-k{margin:0 0 10px;font:400 15px/1.4 var(--deva);color:var(--rose);letter-spacing:.1em}
.faq h2{margin:0 0 24px;font:400 clamp(36px,5vw,60px)/1.12 var(--disp);color:var(--moon)}
.faq details{border-top:1px solid rgba(236,230,218,.14)}
.faq details:last-child{border-bottom:1px solid rgba(236,230,218,.14)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:14px;padding:16px 0;font:400 clamp(20px,2vw,24px)/1.45 var(--deva);color:var(--moon)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold);font:400 24px/1 var(--latin);transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0 0 18px;max-width:40em;font-size:clamp(19px,1.8vw,21px);line-height:1.8;color:var(--ash)}
</style>'''
    s=put(s,'</main>',css+'\n'+faq_html('पूछे जाने वाले सवाल',nn_qa,kick='सवाल जवाब'),'faq')
    write(p,s)

# ------------------------------------------------------------------ the game's intro page (template, then its builder)
GM=SITE+'/game/LankaKiKhoj'; PLAY=SITE+'/lanka_ki_khoj'
gm_qa=[
 ("लंका की खोज क्या है?","सुंदरकांड पर बना एक खोज वाला खेल, हिंदी में। आप ख़ुद लंका में घूमते हैं, अपनी जगह चुनते हैं और वो बातें ढूँढते हैं जो बहुत कम लोगों ने सुनी हैं।"),
 ("इसे कहाँ खेलें?","सीधे ब्राउज़र में, manuvishranti.com/lanka_ki_khoj पर। कुछ डाउनलोड नहीं करना पड़ता।"),
 ("इसमें कितनी भूमिकाएँ हैं?","आठ: जिज्ञासु, यात्री, कथा प्रेमी, बालक, योद्धा, शास्त्री, साधक और राजा। पहली पाँच शुरू से खुली हैं, बाक़ी तीन खेलते खेलते खुलती हैं।"),
 ("खेल में कितनी रातें और जगहें हैं?","छह रातें, हर रात चार प्रहर, और नक्शे पर 96 जगहें। साथ में 41 रामकथाएँ, भारत और दुनिया भर से, और 108 पल।"),
 ("छोटे खेल कौन से हैं?","चार: समुद्र की छलाँग, छत दर छत, परछाईं पहचानो और दीया जोड़ो। इनमें पढ़ना नहीं है।"),
 ("क्या खेल बीच में छोड़कर बाद में खेल सकते हैं?","हाँ। जहाँ छोड़ोगे, खेल वहीं से शुरू होगा। सब उसी फ़ोन या कंप्यूटर पर सहेजा रहता है।"),
]
def game_graph(page):
    return {"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":page+"#page","url":page,"name":"लंका की खोज","isPartOf":{"@id":SITE+"/#site"},"about":{"@id":GM+"#game"},"breadcrumb":{"@id":page+"#crumbs"},"inLanguage":"hi","dateModified":TODAY},
      {"@type":"VideoGame","@id":GM+"#game","name":"लंका की खोज","alternateName":"Lanka Ki Khoj","url":GM,"description":"सुंदरकांड पर बना एक खोज वाला खेल, हिंदी में। आठ भूमिकाएँ, छह रातें, नक्शे पर 96 जगहें, 41 रामकथाएँ और 108 पल।",
       "genre":["Educational game","Exploration"],"gamePlatform":"Web browser","applicationCategory":"Game","operatingSystem":"Any","playMode":"SinglePlayer","numberOfPlayers":{"@type":"QuantitativeValue","value":1},
       "inLanguage":"hi","author":{"@id":PERSON["@id"]},"image":GM+"/img/share.jpg","about":["सुंदरकांड","रामायण","हनुमान","लंका"],
       "potentialAction":{"@type":"PlayAction","target":PLAY}},
      PERSON, crumbs(page,"लंका की खोज")]+([faq_ld(page,gm_qa)] if page==GM else [])}
def game():
    tpl=os.path.join(ROOT,'tools','lanka_intro','lkpage.tpl'); s=open(tpl).read()
    s=strip_old_ld(s)
    s=set_meta(s,'लंका की खोज (Lanka Ki Khoj): सुंदरकांड पर बना एक खेल · मनु विश्रांति',None)
    s=put(s,'<link rel="preconnect" href="https://fonts.googleapis.com">',ld(game_graph(GM)),'seo')
    css='''<style>
.faq{background:#F0F2ED;color:#17222F;padding:clamp(60px,8vw,110px) 0;border-top:1px solid #C6CFC8;font-family:"Tiro Devanagari Hindi",serif}
.faq-in{box-sizing:border-box;width:min(100%,900px);margin:0 auto;padding-inline:max(16px,4vw)}
.faq-k{display:inline-block;margin:0 0 10px;padding:4px 12px 2px;border-radius:999px;background:#17222F;color:#F0F2ED;font-size:14px}
.faq h2{margin:0 0 22px;font:400 clamp(34px,4.6vw,56px)/1.12 "Rozha One","Tiro Devanagari Hindi",serif}
.faq details{background:#fff;border:1px solid #C6CFC8;border-radius:14px;margin:0 0 12px;padding:0 18px}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:12px;padding:15px 0;font-size:clamp(19px,1.9vw,22px)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:#216761;font:400 26px/1 serif;transition:transform .3s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:0 0 16px;font-size:18px;line-height:1.7;color:#344553}
</style>'''
    if '<!-- faq:start -->' not in s:
        s=s.replace('<script>/*SCRIPT*/','<!-- faq:start -->\n'+css+'\n'+faq_html('पूछे जाने वाले सवाल',gm_qa,kick='सवाल जवाब')+'\n<!-- faq:end -->\n<script>/*SCRIPT*/',1)
    else:
        a=s.index('<!-- faq:start -->');b=s.index('<!-- faq:end -->')
        s=s[:a]+'<!-- faq:start -->\n'+css+'\n'+faq_html('पूछे जाने वाले सवाल',gm_qa,kick='सवाल जवाब')+'\n'+s[b:]
    open(tpl,'w').write(nodash(s)); print('wrote tpl')
    os.system('python3 "%s"'%os.path.join(ROOT,'tools','lanka_intro','buildlk.py'))
    # the game itself: head only, nothing else touched
    p=os.path.join(ROOT,'lanka_ki_khoj','index.html'); g=open(p).read()
    head_extra='''<link rel="canonical" href="%s">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="मनु विश्रांति">
<meta property="og:title" content="लंका की खोज · सुंदरकांड पर बना एक खेल">
<meta property="og:description" content="समुद्र पार करो, लंका में घूमो, और वो बातें ढूँढो जो बहुत कम लोगों ने सुनी हैं।">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
%s'''%(PLAY,PLAY,GM,ld(game_graph(PLAY)))
    g=put(g,'<link rel="preconnect" href="https://fonts.googleapis.com">',head_extra,'seo')
    g=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="लंका की खोज: सुंदरकांड पर बना एक खेल, हिंदी में। सुंदरकांड की एक रात, असली भूगोल के नक्शे पर। आठ भूमिकाएँ, छह रातें और 96 जगहें।">',g,count=1)
    write(p,g)

if __name__=='__main__':
    home(); fivewounds(); comic(); diary(); game()
