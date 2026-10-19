# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Single-request public GitHub account metadata, cache-first and failure-tolerant."""
import json, os, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead

FIELDS=('followers','following','public_repos','public_gists')
def load(path,username):
    try:
        data=json.loads(Path(path).read_text(encoding='utf8'))
        if data.get('username')==username and all(type(data.get(k)) is int and data[k]>=0 for k in FIELDS):return data
    except (OSError,ValueError,AttributeError,TypeError):pass
    return None

def refresh(username,path,ttl_hours=24,force=False,fetcher=None):
    old=load(path,username)
    if old and not force and time.time()-old.get('fetched_at',0)<ttl_hours*3600:return old,'cached'
    headers={'User-Agent':'burncode-profile-generator','Accept':'application/vnd.github+json'}
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:headers['Authorization']='Bearer '+token
    request=Request('https://api.github.com/users/'+username,headers=headers)
    try:
        with (fetcher(request) if fetcher else urlopen(request,timeout=8)) as response:
            payload=json.loads(response.read().decode('utf8'))
        if not all(type(payload.get(k)) is int and payload[k]>=0 for k in FIELDS):raise ValueError('invalid profile data')
        result={'username':username,'fetched_at':time.time(),**{k:payload[k] for k in FIELDS}}
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        Path(path).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
        return result,'updated'
    except (OSError,ValueError,HTTPError,URLError,IncompleteRead,TimeoutError):
        return old,'stale' if old else 'unavailable'
