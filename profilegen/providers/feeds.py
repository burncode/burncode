# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Small, safe RSS/Atom reader using Python stdlib. No external XML entities."""
import json,time,html,re
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse, urljoin, urlunparse
from xml.etree import ElementTree as ET

def _text(node):
    return ''.join(node.itertext()).strip() if node is not None else ''

def _article_url(raw, feed_url=''):
    """Normalize known Hexo placeholder hosts against the actual feed origin.

    Never accept an unrelated host or guess a missing path.
    """
    p=urlparse(raw)
    if p.hostname in ('yoursite.com','www.yoursite.com') and feed_url:
        feed=urlparse(feed_url)
        if feed.scheme!='https' or not feed.hostname:return ''
        return urlunparse(('https',feed.netloc,p.path or '/', '',p.query,''))
    if raw.startswith('/') and feed_url:return urljoin(feed_url,raw)
    return raw

def parse(xml,limit=5,feed_url=''):
    root=ET.fromstring(xml)
    items=[]
    if root.tag.lower().endswith('rss') or root.tag.lower().endswith('rdf'):
        nodes=[n for n in root.iter() if n.tag.split('}')[-1]=='item']
        for node in nodes:
            child=lambda tag:next((c for c in node if c.tag.split('}')[-1]==tag),None)
            title=html.unescape(_text(child('title')))
            url=_article_url(_text(child('link')),feed_url)
            if title and _safe(url):items.append({'title':title[:100],'url':url})
    else:
        nodes=[n for n in root.iter() if n.tag.split('}')[-1]=='entry']
        for node in nodes:
            title=html.unescape(_text(next((c for c in node if c.tag.split('}')[-1]=='title'),None)))
            links=[c for c in node if c.tag.split('}')[-1]=='link']
            link=next((c for c in links if c.attrib.get('rel','alternate')=='alternate'),links[0] if links else None)
            url=_article_url(link.attrib.get('href','') if link is not None else '',feed_url)
            if title and _safe(url):items.append({'title':title[:100],'url':url})
    return items[:limit]

def _safe(url):
    p=urlparse(url)
    return p.scheme=='https' and bool(p.hostname) and not (p.username or p.password)

def load(path,url):
    try:
        obj=json.loads(Path(path).read_text(encoding='utf8'))
        return obj if obj.get('feed_url')==url and isinstance(obj.get('items'),list) else None
    except (OSError,ValueError,AttributeError):return None

def refresh(url,path,limit=5,ttl_hours=12,force=False,fetcher=None):
    old=load(path,url)
    if old and not force and time.time()-old.get('fetched_at',0)<ttl_hours*3600:return old,'cached'
    try:
        req=Request(url,headers={'User-Agent':'burncode-profile/11.8','Accept':'application/rss+xml, application/atom+xml, application/xml'})
        with (fetcher(req) if fetcher else urlopen(req,timeout=8)) as resp:
            final=resp.geturl() if hasattr(resp,'geturl') else url
            if not _safe(final):raise ValueError('insecure feed redirect')
            data=resp.read(1024*1024+1)
        if len(data)>1024*1024:raise ValueError('feed too large')
        if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise ValueError('DTD not allowed')
        items=parse(data,limit,feed_url=url)
        result={'feed_url':url,'fetched_at':time.time(),'items':items, 'warning':('No valid article links found; check Hexo url configuration' if not items else '')}
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        Path(path).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        return result,'updated'
    except (OSError,ValueError,ET.ParseError,TimeoutError):
        return (old,'stale') if old else (None,'unavailable')
