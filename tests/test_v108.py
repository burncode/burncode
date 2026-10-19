# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest, sys, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
class V108Tests(unittest.TestCase):
    def setUp(self):
        self.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
    def test_cat_walk_svg(self):
        s=build.render(self.cfg,'mono')
        self.assertIn('id="pixel-companion"',s)
        self.assertIn('animateTransform',s)
    def test_cat_static_fallback(self):
        c=copy.deepcopy(self.cfg);c['companion']['animation']='static'
        s=build.render(c,'mono')
        self.assertIn('id="pixel-companion"',s)
        self.assertNotIn('animateTransform',s)
    def test_cat_disabled(self):
        c=copy.deepcopy(self.cfg);c['header_cat']=False
        self.assertNotIn('id="pixel-companion"',build.render(c,'mono'))
    def test_cat_config_validation(self):
        c=copy.deepcopy(self.cfg);c['cat']={'motion':'fly','duration':1}
        with self.assertRaises(build.ConfigError):build.validate(c,ROOT/'config.json')
    def test_readme_links_visible(self):
        c=copy.deepcopy(self.cfg);c['projects'][0]['url']='https://github.com/burncode/sample'
        c['social']=[{'label':'Email','url':'mailto:hello@example.com'}]
        text=build.make_readme(c)
        self.assertIn('project-1.svg',text)
        self.assertIn('sample',text)
        self.assertIn('connect-1.svg',text)
        self.assertIn('mailto:hello@example.com',text)
    def test_theme_modes(self):
        self.assertEqual(build.load_theme('mono')['mode'],'light')
        self.assertEqual(build.load_theme('graphite')['mode'],'dark')
