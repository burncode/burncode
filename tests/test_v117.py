# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import json, tempfile, unittest, sys, copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from profilegen.providers.languages import load, fetch
ROOT=Path(__file__).resolve().parents[1]

class V117Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
    def test_single_repo_cache_hit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'languages.json'
            path.write_text(json.dumps({'burncode:selected:burncode/only':{'items':[{'name':'Python','value':123}], 'fetched_at':99999}}))
            self.assertEqual(load('burncode',path,repositories=['burncode/only'])['items'][0]['name'],'Python')
            self.assertEqual(load('BURNcode',path,repositories=['BURNcode/ONLY'])['items'][0]['value'],123)
            self.assertIsNone(load('burncode',path,repositories=['burncode/other']))
    def test_zero_only_cache_is_not_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'languages.json'
            path.write_text(json.dumps({'burncode:selected:burncode/only':{'items':[{'name':'Python','value':0}]}}))
            self.assertIsNone(load('burncode',path,repositories=['burncode/only']))
    def test_blog_modular_links(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['widgets']['blog']['posts']=[{'title':'A blog post','url':'https://example.com/post'}]
        strips=build.render_sections(cfg,'mono')
        self.assertEqual(strips['blog-1'][1],'https://example.com/post')
        self.assertIn('Open article:',build.make_readme(cfg))
    def test_about_not_two_columns(self):
        svg=build.render(self.cfg,'mono')
        self.assertIn('独立开发者，喜欢创造实用而有趣的软件',svg)
        self.assertIn('GitHub',svg)
    def test_blog_reject_bad_url(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['widgets']['blog']['posts']=[{'title':'Bad','url':'javascript:alert(1)'}]
        with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')
