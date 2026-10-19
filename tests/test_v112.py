# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""GitHub language provider and modular clickable output tests."""
import copy
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from io import BytesIO
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.providers.languages import fetch,load

class FakeResponse:
    headers={}
    def __init__(self,obj):self.data=json.dumps(obj).encode()
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self):return self.data

class V112Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
    def test_hero_ribbon(self):
        svg=build.render(self.cfg,'mono')
        self.assertNotIn('MODE: indie dev',svg)
        self.assertIn(self.cfg['profile']['tagline'],svg)
        self.assertNotIn('SYSTEM / PROFILE',svg)
        self.assertIn('Pixel', 'Pixel')
    def test_github_empty_languages_placeholder(self):
        svg=build.render(self.cfg,'mono')
        self.assertIn('暂无语言数据',svg)
        ET.fromstring(svg)
    def test_modular_project_link(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['projects'][0]['url']='https://github.com/burncode/example'
        text=build.make_readme(cfg)
        self.assertIn('<a href="https://github.com/burncode/example" target="_blank"',text)
        self.assertIn('project-1.svg',text)
        self.assertIn('project-1.svg',build.make_readme(cfg))
        strips=build.render_sections(cfg,'mono')
        self.assertEqual(strips['project-1'][1],cfg['projects'][0]['url'])
        for svg,_ in strips.values():ET.fromstring(svg)
    def test_provider_aggregates_and_caches(self):
        calls=[]
        def fake(req):
            calls.append(req.full_url)
            if '/users/' in req.full_url:
                return FakeResponse([{'full_name':'burncode/a','fork':False,'archived':False},{'full_name':'burncode/fork','fork':True,'archived':False},{'full_name':'burncode/b','fork':False,'archived':False}])
            if req.full_url.endswith('/a/languages'):return FakeResponse({'Python':500,'Ruby':200})
            return FakeResponse({'Python':100,'JavaScript':300})
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'langs.json'
            data,status=fetch('burncode',path,fetcher=fake,now=100000,repositories=['burncode/a','burncode/b'],sleep=lambda _:None)
            self.assertEqual(status,'updated')
            self.assertEqual(data['items'][0],{'name':'Python','value':600})
            self.assertEqual(data['repositories'],2)
            self.assertEqual(len(calls),2)
            self.assertEqual(load('burncode',path,repositories=['burncode/a','burncode/b'])['items'],data['items'])
            cached,status=fetch('burncode',path,fetcher=lambda req:1/0,now=100100,repositories=['burncode/a','burncode/b'])
            self.assertEqual(status,'cached')
    def test_provider_failure_does_not_fabricate(self):
        with tempfile.TemporaryDirectory() as td:
            data,status=fetch('burncode',Path(td)/'langs.json',fetcher=lambda req: (_ for _ in ()).throw(OSError('offline')),repositories=['burncode/a'],sleep=lambda _:None)
            self.assertIsNone(data)
            self.assertEqual(status,'unavailable')


class ModularPreviewRegressionTests(unittest.TestCase):
    def test_preview_uses_same_project_links(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        cfg['projects'][0]['url']='https://github.com/burncode/example'
        preview=build.make_preview_html(cfg)
        readme=build.make_readme(cfg)
        self.assertIn('<a href="https://github.com/burncode/example" target="_blank"',preview)
        self.assertIn('<a href="https://github.com/burncode/example" target="_blank"',readme)
        self.assertIn('assets/sections/'+cfg['themes']['light']+'/project-1.svg',preview)
        self.assertIn('assets/sections/'+cfg['themes']['dark']+'/project-1.svg',preview)

    def test_missing_url_not_linked(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        for p in cfg['projects']: p['url']=''
        preview=build.make_preview_html(cfg)
        self.assertNotIn('href="https://github.com/burncode/example"',preview)
