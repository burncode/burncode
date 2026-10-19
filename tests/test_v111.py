# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Showcase refresh and optional languages widget."""
import copy,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
class V111Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
    def test_showcase_default(self):
        self.assertEqual(self.cfg['layout_mode'],'showcase')
        self.assertIn('viewBox="0 0 1100 ',build.render(self.cfg,'mono'))
    def test_languages_disabled(self):
        c=copy.deepcopy(self.cfg);c['widgets']['languages']['enabled']=False
        self.assertNotIn('/ languages',build.render(c,'mono'))
    def test_languages_enabled(self):
        c=copy.deepcopy(self.cfg);c['widgets']['languages']={'enabled':True,'source':'manual','items':[{'name':'Python','value':60},{'name':'Ruby','value':40}]}
        c=build.validate(c,ROOT/'config.json');s=build.render(c,'mono')
        self.assertIn('Python 60%',s);self.assertIn('Ruby 40%',s);ET.fromstring(s)
    def test_languages_invalid_empty(self):
        c=copy.deepcopy(self.cfg);c['widgets']['languages'].update({'enabled':True,'source':'manual','items':[]})
        with self.assertRaises(build.ConfigError):build.validate(c,ROOT/'config.json')
