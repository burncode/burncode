# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Verified GitHub contribution calendar via GraphQL; no synthetic statistics."""
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

QUERY='''query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}'''
LEVELS={'NONE':0,'FIRST_QUARTILE':1,'SECOND_QUARTILE':2,'THIRD_QUARTILE':3,'FOURTH_QUARTILE':4}

def load_contributions(path,username):
    try:
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if data.get('username')==username and isinstance(data.get('days'),list):return data
    except (OSError,ValueError,AttributeError):pass
    return None

def refresh_contributions(username,path,token=None,fetcher=None,now=None):
    """Return (verified calendar or prior cache, status). Token is required."""
    previous=load_contributions(path,username)
    token=token or os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:return previous,'token-required (GH_TOKEN or GITHUB_TOKEN)'
    req=Request('https://api.github.com/graphql',data=json.dumps({'query':QUERY,'variables':{'login':username}}).encode(),headers={
        'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
        'Content-Type':'application/json','User-Agent':'burncode-profile-generator'},method='POST')
    try:
        with (fetcher(req) if fetcher else urlopen(req,timeout=12)) as r:
            payload=json.loads(r.read().decode('utf-8'))
        calendar=payload['data']['user']['contributionsCollection']['contributionCalendar']
        total=calendar['totalContributions']
        if type(total) is not int or total<0:raise ValueError('invalid total')
        days=[]
        for week in calendar['weeks']:
            for day in week['contributionDays']:
                level=LEVELS[day['contributionLevel']]
                count=day['contributionCount']
                if type(count) is not int or count<0:raise ValueError('invalid count')
                days.append({'date':day['date'],'count':count,'level':level})
        result={'username':username,'total':total,'days':days,'fetched_at':time.time() if now is None else now,'source':'github-graphql'}
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return result,'updated'
    except (HTTPError,URLError,OSError,ValueError,KeyError,TypeError,TimeoutError,AttributeError):
        return previous,'stale' if previous else 'unavailable (API error)'
