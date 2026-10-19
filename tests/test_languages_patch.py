# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import copy
import json
import tempfile
import unittest
from http.client import IncompleteRead
from pathlib import Path
import build
from profilegen.providers.languages import fetch,load

class FakeResponse:
    def __init__(self, value):self.value=value
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return json.dumps(self.value).encode()

class LanguagePatchTests(unittest.TestCase):
    def test_empty_selection_makes_no_requests(self):
        data,status=fetch('burncode','/nonexistent/langs.json',repositories=[],fetcher=lambda r:1/0)
        self.assertIsNone(data)
        self.assertEqual(status,'no-selected-repositories')
    def test_profile_one_request_and_excludes_forks(self):
        calls=[]
        def fake(req):
            calls.append(req.full_url)
            return FakeResponse([{'language':'Python','fork':False,'archived':False},
                {'language':'Ruby','fork':True,'archived':False},
                {'language':'Python','fork':False,'archived':False}])
        with tempfile.TemporaryDirectory() as d:
            data,status=fetch('burncode',Path(d)/'data.json',mode='profile',fetcher=fake)
            self.assertEqual(status,'updated')
            self.assertEqual(len(calls),1)
            self.assertEqual(data['measure'],'repository-count')
            self.assertEqual(data['items'][0]['value'],2)
    def test_incomplete_read_retry(self):
        calls=[]
        def fake(req):
            calls.append(1)
            if len(calls)==1:raise IncompleteRead(b'partial',4)
            return FakeResponse({'Ruby':123})
        with tempfile.TemporaryDirectory() as d:
            data,status=fetch('burncode',Path(d)/'data.json',repositories=['burncode/test'],fetcher=fake,sleep=lambda _:None)
            self.assertEqual(status,'updated')
            self.assertEqual(len(calls),2)
    def test_stale_on_failure(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'data.json'
            fetch('burncode',path,repositories=['burncode/test'],fetcher=lambda r:FakeResponse({'Ruby':123}),now=100)
            data,status=fetch('burncode',path,repositories=['burncode/test'],fetcher=lambda r: (_ for _ in ()).throw(IncompleteRead(b'',3)),now=999999,ttl_hours=1,sleep=lambda _:None)
            self.assertEqual(status,'stale')
            self.assertEqual(data['items'][0]['name'],'Ruby')
    def test_selected_cache_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'data.json'
            fetch('burncode',path,repositories=['burncode/a'],fetcher=lambda r:FakeResponse({'Python':3}))
            self.assertIsNone(load('burncode',path,repositories=['burncode/b']))
    def test_config_validation(self):
        cfg=build.read_json(Path(build.ROOT)/'config.json')
        cfg['widgets']['languages'].update({'mode':'selected','repositories':['burncode/a'],'max_repositories':5})
        self.assertEqual(build.validate(cfg,Path(build.ROOT)/'config.json')['widgets']['languages']['max_repositories'],5)
        cfg['widgets']['languages']['repositories']=['bad']
        with self.assertRaises(build.ConfigError):build.validate(cfg,Path(build.ROOT)/'config.json')

if __name__=='__main__':unittest.main()
