# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""GitHub REST metadata provider; stdlib only, cache-first, no fabricated metrics."""
from __future__ import annotations
import json
import os
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')

def refresh(repositories, cache_path, token=None, ttl_hours=12, force=False, fetcher=None, now=None):
    """Return {repo: {stars, forks, updated_at, fetched_at, source}}.

    No network unless cache is stale or force=True. Failed requests keep prior cache.
    Cached data are never replaced by unverified zeros.
    """
    now = time.time() if now is None else now
    cache_path = Path(cache_path)
    try:
        saved = json.loads(cache_path.read_text(encoding='utf-8'))
        if not isinstance(saved, dict): saved = {}
    except (OSError, ValueError):
        saved = {}
    result = dict(saved)
    outcomes = {}
    for name in dict.fromkeys(repositories):
        if not REPO.fullmatch(name):
            outcomes[name] = 'invalid'; continue
        old = result.get(name)
        if not force and isinstance(old, dict) and now - old.get('fetched_at', 0) < ttl_hours*3600:
            outcomes[name] = 'cached'; continue
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'burncode-profile-generator', 'X-GitHub-Api-Version':'2022-11-28'}
        auth = token or os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if auth: headers['Authorization'] = 'Bearer ' + auth
        if isinstance(old, dict) and old.get('etag'): headers['If-None-Match'] = old['etag']
        req = Request('https://api.github.com/repos/' + name, headers=headers)
        try:
            if fetcher is None:
                response = urlopen(req, timeout=8)
            else:
                response = fetcher(req)
            with response as r:
                data = json.loads(r.read().decode('utf-8'))
                if type(data.get('stargazers_count')) is not int or type(data.get('forks_count')) is not int:
                    raise ValueError('GitHub returned invalid metrics')
                result[name] = {'stars':data['stargazers_count'], 'forks':data['forks_count'],
                                'updated_at':data.get('updated_at'), 'fetched_at':now,
                                'etag':r.headers.get('ETag'), 'source':'github'}
            outcomes[name] = 'updated'
        except HTTPError as exc:
            if exc.code == 304 and isinstance(old, dict):
                result[name] = {**old, 'fetched_at':now}
                outcomes[name] = 'not-modified'
            else: outcomes[name] = 'stale' if old else 'unavailable'
        except (URLError, OSError, ValueError, KeyError, TimeoutError):
            outcomes[name] = 'stale' if old else 'unavailable'
    if result != saved:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n',encoding='utf-8')
    return result, outcomes

def apply(cfg, cache):
    """Prefer verified API metrics over manual values; never invent metrics."""
    for project in cfg.get('projects', []):
        entry = cache.get(project.get('repository', ''))
        if isinstance(entry, dict) and type(entry.get('stars')) is int and type(entry.get('forks')) is int:
            project['stars'] = entry['stars']
            project['forks'] = entry['forks']
            project['_metrics_source'] = 'github-cache'
    return cfg


def infer_repository(url):
    """Recognize only direct GitHub repository URLs, never profile/issue links."""
    from urllib.parse import urlparse
    try:
        u=urlparse(url)
        if u.scheme!='https' or u.hostname not in ('github.com','www.github.com'):
            return None
        parts=[part for part in u.path.strip('/').split('/') if part]
        if len(parts)!=2 or parts[1] in ('repositories','followers','following'):
            return None
        name='/'.join(parts)
        return name if REPO.fullmatch(name) else None
    except (ValueError,TypeError):
        return None
