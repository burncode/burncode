# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Regression tests for native narrow layout and story companion."""
import copy,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build

class NarrowAndCompanionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')

    def test_narrow_viewbox_is_native(self):
        cfg=copy.deepcopy(self.cfg);cfg['layout_mode']='github'
        svg=build.render(cfg,'mono')
        self.assertIn('viewBox="0 0 900 ',svg)
        self.assertNotIn('scale(0.818',svg)
        ET.fromstring(svg)

    def test_showcase_kept(self):
        cfg=copy.deepcopy(self.cfg);cfg['layout_mode']='showcase'
        self.assertIn('viewBox="0 0 1100 ',build.render(cfg,'mono'))

    def test_story_sequence_and_banner(self):
        svg=build.render(self.cfg,'mono')
        self.assertIn(self.cfg['companion']['banner'],svg)
        self.assertIn('calcMode="discrete"',svg)
        self.assertIn('>z</text>',svg)

    def test_story_input_rejected(self):
        cfg=copy.deepcopy(self.cfg);cfg['companion']['sequence']=['walk','<script>']
        with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')

    def test_banner_escaped(self):
        cfg=copy.deepcopy(self.cfg);cfg['companion']['banner']='LOVE & YOU'
        svg=build.render(build.validate(cfg,ROOT/'config.json'),'mono')
        self.assertIn('LOVE &amp; YOU',svg)
        ET.fromstring(svg)

if __name__=='__main__':unittest.main()
