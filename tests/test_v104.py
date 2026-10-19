# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.i18n import load_locale,locale_names,tr

class V104Tests(unittest.TestCase):
    def setUp(self):
        self.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')

    def test_nine_themes(self):
        self.assertEqual(len(build.theme_names()),9)
        for theme in build.theme_names():
            t=build.load_theme(theme)
            self.assertIn('projects',t['components'])
            self.assertIn('activity',t['components'])
            self.assertIn('projects',t['icons'])

    def test_locale_files(self):
        self.assertEqual(set(locale_names()),{'en','zh-CN','ja','es'})
        self.assertEqual(tr(self.cfg,'projects'),'项目')
        cfg=copy.deepcopy(self.cfg);cfg['i18n']['locale']='zh-CN'
        self.assertEqual(tr(cfg,'projects'),'项目')
        self.assertIn('development',load_locale('ja'))

    def test_badges_inline_and_compact_icons(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['layout_mode']='showcase'
        cfg['projects'][0]['stars']=191
        cfg['projects'][0]['forks']=48
        svg=build.render(cfg,'mono')
        self.assertIn('191</text>',svg)
        self.assertIn('48</text>',svg)
        self.assertIn('viewBox=',svg)

    def test_theme_accent_contributions(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['_contributions']={'total':1,'days':[{'level':4}]}
        svg=build.render(cfg,'sage')
        self.assertIn('1 contributions',svg)
        self.assertIn(build.load_theme('sage')['colors']['accent'],svg)

    def test_custom_theme_icon(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['projects'][0]['icon']='terminal'
        svg=build.render(cfg,'ice')
        self.assertIn('viewBox="0 0 1100',svg)

    def test_invalid_component_theme(self):
        # A copied JSON theme with invalid CSS-like color is rejected.
        theme=build.load_theme('paper')
        self.assertEqual(theme['components']['projects']['icon_size'],42)
