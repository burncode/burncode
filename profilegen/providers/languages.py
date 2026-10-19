# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Bounded GitHub language collection. Only explicitly selected repositories are queried."""
import json
import os
import re
import time
from http.client import IncompleteRead, RemoteDisconnected
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = 'https://api.github.com'
REPO = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
TRANSIENT = (OSError, ValueError, KeyError, TypeError, HTTPError, URLError,
             TimeoutError, IncompleteRead, RemoteDisconnected)


def _valid(entry):
    """Do not treat empty, zero-only or malformed cached values as usable."""
    return (isinstance(entry, dict) and isinstance(entry.get('items'), list)
            and any(isinstance(i, dict) and isinstance(i.get('name'), str)
                    and type(i.get('value')) in (int, float) and i['value'] > 0
                    for i in entry['items']))


def _cached(saved, username, mode, repositories):
    key = _key(username, mode, repositories)
    if _valid(saved.get(key)):
        return saved[key]
    # Compatibility with cache keys whose repository ordering/casing differs.
    prefix = username.lower() + ':' + mode + ':'
    requested = {r.casefold() for r in repositories}
    for candidate, entry in saved.items():
        if not isinstance(candidate, str) or not candidate.casefold().startswith(prefix):
            continue
        existing = {r.casefold() for r in candidate[len(prefix):].split(',') if r}
        if existing == requested and _valid(entry):
            return entry
    return None


def load(username, cache_path, mode='selected', repositories=None):
    try:
        data = json.loads(Path(cache_path).read_text(encoding='utf-8'))
        return _cached(data, username, mode, repositories or []) if isinstance(data, dict) else None
    except (OSError, ValueError, AttributeError, TypeError):
        return None


def _key(username, mode, repositories):
    return username.lower() + ':' + mode + ':' + ','.join(sorted(r.lower() for r in repositories))


def fetch(username, cache_path, token=None, ttl_hours=168, force=False,
          fetcher=None, now=None, mode='selected', repositories=None,
          max_repositories=10, retries=2, sleep=None):
    """Returns (data, status). Network failures never crash optional widget rendering.

    selected: one /languages request per selected repo (at most max_repositories).
    profile: one /users/{user}/repos request; counts primary language per repo,
             NOT byte percentages. No per-repository requests.
    """
    now = time.time() if now is None else now
    sleep = time.sleep if sleep is None else sleep
    cache_path = Path(cache_path)
    repositories = list(dict.fromkeys(repositories or []))
    if mode not in ('selected', 'profile'):
        raise ValueError('unsupported languages mode')
    if not isinstance(max_repositories, int) or not 1 <= max_repositories <= 20:
        raise ValueError('max_repositories must be 1..20')
    if mode == 'selected':
        repositories = [r for r in repositories if isinstance(r, str) and REPO.fullmatch(r)][:max_repositories]
    else:
        repositories = []
    try:
        saved = json.loads(cache_path.read_text(encoding='utf-8'))
        if not isinstance(saved, dict): saved = {}
    except (OSError, ValueError):
        saved = {}
    key = _key(username, mode, repositories)
    old = _cached(saved, username, mode, repositories)
    if mode == 'selected' and not repositories:
        return old, 'cached' if old else 'no-selected-repositories'
    if not force and old and now - old.get('fetched_at', 0) < ttl_hours * 3600:
        return old, 'cached'
    headers = {'Accept':'application/vnd.github+json', 'User-Agent':'burncode-profile-generator',
               'X-GitHub-Api-Version':'2022-11-28'}
    auth = token or os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if auth: headers['Authorization'] = 'Bearer ' + auth

    def get(url):
        for attempt in range(retries + 1):
            try:
                request = Request(url, headers=headers)
                with (fetcher(request) if fetcher else urlopen(request, timeout=12)) as response:
                    return json.loads(response.read().decode('utf-8'))
            except HTTPError as exc:
                # Stop immediately on rate limiting, auth errors, or missing repos.
                if exc.code in (401, 403, 404, 429): raise
                if exc.code < 500 or attempt >= retries: raise
            except (OSError, URLError, TimeoutError, IncompleteRead, RemoteDisconnected, ValueError):
                if attempt >= retries: raise
            sleep(min(2 ** attempt, 4))

    try:
        counts = {}
        if mode == 'profile':
            repos = get(f'{API}/users/{username}/repos?type=owner&per_page=100&page=1')
            if not isinstance(repos, list): raise ValueError('invalid repository list')
            selected = [r for r in repos if isinstance(r, dict) and not r.get('fork')
                        and not r.get('archived') and r.get('language')]
            for repo in selected:
                lang = repo['language']
                counts[lang] = counts.get(lang, 0) + 1
            repo_count = len(selected)
            measure = 'repository-count'
        else:
            for full in repositories:
                data = get(f'{API}/repos/{full}/languages')
                if not isinstance(data, dict): raise ValueError('invalid language response')
                for lang, value in data.items():
                    if isinstance(lang, str) and type(value) is int and value >= 0:
                        counts[lang] = counts.get(lang, 0) + value
            repo_count = len(repositories)
            measure = 'bytes'
        items = [{'name':name,'value':value} for name,value in
                 sorted(counts.items(), key=lambda p:(-p[1],p[0])) if value > 0][:6]
        if not items: return old, 'stale' if old else 'no-public-language-data'
        result = {'items':items, 'repositories':repo_count, 'fetched_at':now,
                  'source':'github', 'mode':mode, 'measure':measure}
        saved[key] = result
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = cache_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(saved, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        temporary.replace(cache_path)
        return result, 'updated'
    except TRANSIENT:
        return old, 'stale' if old else 'unavailable'
