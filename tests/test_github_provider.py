# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Deterministic GitHub provider tests, no network required."""
import io
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from profilegen.providers.github import refresh, apply

class Response:
    def __init__(self, data, etag='"abc"'):
        self._data=data
        self.headers={'ETag':etag}
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return self._data

class ProviderTests(unittest.TestCase):
    def test_fetch_and_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'github.json'
            calls=[]
            def fetch(req):
                calls.append(req.full_url)
                return Response(b'{"stargazers_count":12,"forks_count":3,"updated_at":"2026-01-01T00:00:00Z"}')
            cache,states=refresh(['owner/repo'],p,fetcher=fetch,now=100000)
            self.assertEqual(cache['owner/repo']['stars'],12)
            self.assertEqual(states['owner/repo'],'updated')
            cache,states=refresh(['owner/repo'],p,fetcher=fetch,now=100100)
            self.assertEqual(states['owner/repo'],'cached')
            self.assertEqual(len(calls),1)
    def test_offline_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'github.json'
            refresh(['owner/repo'],p,fetcher=lambda req:Response(b'{"stargazers_count":4,"forks_count":2}'),now=100)
            def offline(req):raise URLError('offline')
            cache,states=refresh(['owner/repo'],p,fetcher=offline,force=True,now=200)
            self.assertEqual(states['owner/repo'],'stale')
            self.assertEqual(cache['owner/repo']['forks'],2)
    def test_etag_not_modified(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'github.json'
            refresh(['owner/repo'],p,fetcher=lambda req:Response(b'{"stargazers_count":4,"forks_count":2}'),now=100)
            def not_modified(req):
                self.assertEqual(req.get_header('If-none-match'),'"abc"')
                raise HTTPError(req.full_url,304,'Not Modified',{},None)
            cache,states=refresh(['owner/repo'],p,fetcher=not_modified,force=True,now=200)
            self.assertEqual(states['owner/repo'],'not-modified')
            self.assertEqual(cache['owner/repo']['fetched_at'],200)
    def test_missing_data_not_zero(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'github.json'
            cache,states=refresh(['owner/repo'],p,fetcher=lambda req:Response(b'{"message":"Not Found"}'),now=100)
            self.assertEqual(states['owner/repo'],'unavailable')
            self.assertNotIn('owner/repo',cache)
            cfg={'projects':[{'repository':'owner/repo','name':'x'}]}
            apply(cfg,cache)
            self.assertNotIn('stars',cfg['projects'][0])

if __name__=='__main__':unittest.main()
