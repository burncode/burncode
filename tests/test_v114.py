# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""v11.4 project metadata, reusable icon, social width and stats contracts."""
import copy
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from profilegen.icons import ICONS, draw_icon
from profilegen.svg import Canvas

ROOT=Path(__file__).resolve().parents[1]
class V114Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
    def test_icon_is_reusable(self):
        self.assertIn('terminal',ICONS)
        c=Canvas(build.load_theme('mono'))
        draw_icon(c,0,0,'terminal','#ff6654')
        svg=''.join(c.parts)
        self.assertIn('stroke="'+build.load_theme('mono')['colors']['border']+'"',svg)
        self.assertIn('fill="#ff6654"',svg)
    def test_project_metrics_and_chips(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['projects'][0]['stars']=82;cfg['projects'][0]['forks']=10
        svg=build.render(cfg,'mono')
        self.assertIn('>82</text>',svg)
        self.assertIn('>10</text>',svg)
        self.assertIn('>'+cfg['projects'][0]['tags'][0]+'</text>',svg)
    def test_modular_connect_is_compact(self):
        md=build.make_readme(self.cfg)
        self.assertIn('class="social-toolbar"',md)
        self.assertIn('width="99"',md)
        self.assertNotIn('social links below',md)
    def test_stats_optional(self):
        cfg=copy.deepcopy(self.cfg)
        self.assertIn('>Followers</text>',build.render(cfg,'mono'))
        cfg['widgets']['github_stats']['enabled']=False
        self.assertNotIn('>Followers</text>',build.render(cfg,'mono'))
    def test_chinese_default_and_english_metrics(self):
        self.assertEqual(self.cfg['i18n']['locale'],'zh-CN')
        svg=build.render(self.cfg,'mono')
        self.assertIn('>Followers</text>',svg)
