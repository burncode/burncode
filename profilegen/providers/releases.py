# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Fetch selected repository releases only; cache and failure-safe."""
import json,os,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from http.client import IncompleteRead

def load(path):
    try:
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        return data if isinstance(data,dict) and isinstance(data.get('items'),list) else None
    except (OSError,ValueError,TypeError):return None

def refresh(repositories,path,force=False,ttl_hours=24,fetcher=None):
    old=load(path);repos=list(dict.fromkeys(repositories))[:5]
    if old and old.get('repositories')==repos and not force and time.time()-old.get('fetched_at',0)<ttl_hours*3600:return old,'cached'
    headers={'User-Agent':'burncode-profile-generator','Accept':'application/vnd.github+json'}
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:headers['Authorization']='Bearer '+token
    items=[];errors=0
    for repo in repos:
        req=Request('https://api.github.com/repos/'+repo+'/releases/latest',headers=headers)
        try:
            with (fetcher(req) if fetcher else urlopen(req,timeout=8)) as resp:
                obj=json.loads(resp.read().decode('utf8'))
            if not isinstance(obj.get('tag_name'),str):continue
            items.append({'repo':repo,'tag':obj['tag_name'][:64],'date':str(obj.get('published_at') or '')[:10],'url':str(obj.get('html_url') or '')})
        except (OSError,ValueError,HTTPError,URLError,IncompleteRead,TimeoutError):errors+=1
    if errors and old:return old,'stale'
    data={'repositories':repos,'fetched_at':time.time(),'items':items}
    if not errors:
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return data,'partial' if errors else 'updated'
