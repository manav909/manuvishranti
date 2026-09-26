"""Shared helpers for the site's search and answer engine markup.
Every FAQ answer here is also visible on its page, word for word."""
import json, html, re
SITE='https://manuvishranti.com'
TODAY='2026-09-27'
PERSON={"@type":"Person","@id":SITE+"/#person","name":"Manu Vishranti","alternateName":["मनु विश्रांति"],"url":SITE+"/"}
PUBLISHER={"@type":"Organization","@id":"https://walnutpublication.com/#org","name":"Walnut Publication","url":"https://walnutpublication.com/"}

def ld(obj):
    return '<script type="application/ld+json">\n'+json.dumps(obj,ensure_ascii=False,indent=1)+'\n</script>'

def faq_ld(url,qa):
    return {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]}

def crumbs(url,name):
    return {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Manu Vishranti","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":name,"item":url}]}

def faq_html(title,qa,lang=None,kick=None):
    l=' lang="%s"'%lang if lang else ''
    items=''.join('\n      <details><summary>%s</summary><p>%s</p></details>'%(html.escape(q),html.escape(a)) for q,a in qa)
    k='<p class="faq-k">%s</p>'%kick if kick else ''
    return '<section class="faq" id="faq" aria-labelledby="faq-h"%s>\n  <div class="faq-in">\n    %s<h2 id="faq-h">%s</h2>\n    <div class="faq-list">%s\n    </div>\n  </div>\n</section>'%(l,k,title,items)

def swap_block(s,start,end,new):
    """replace text between two marker comments (markers kept) or insert markers if absent"""
    if start in s:
        i=s.index(start)+len(start); j=s.index(end,i); return s[:i]+'\n'+new+'\n'+s[j:]
    return None

def nodash(s):
    assert not re.search('[–—]',s),'dash found'
    return s
