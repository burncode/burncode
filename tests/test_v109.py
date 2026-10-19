# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest, copy, json
import xml.etree.ElementTree as ET
from pathlib import Path
import build

ROOT=Path(__file__).resolve().parents[1]
class CompanionAndWidthTests(unittest.TestCase):
    def cfg(self):
        return json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    def test_three_characters(self):
        for char in ('classic_cat','tuxedo_cat','orange_cat'):
            c=self.cfg();c['companion']['character']=char
            cfg=build.validate(c,ROOT/'config.json')
            svg=build.render(cfg,'mono')
            self.assertIn('pixel-companion',svg)
    def test_motion_modes(self):
        for mode in ('wander','walk','idle','static'):
            c=self.cfg();c['companion']['animation']=mode
            svg=build.render(build.validate(c,ROOT/'config.json'),'mono')
            cat=ET.fromstring(svg).find('.//{http://www.w3.org/2000/svg}g[@id="pixel-companion"]')
            animated=any(n.tag.rsplit('}',1)[-1] in ('animate','animateTransform') for n in cat.iter())
            self.assertEqual(animated,mode!='static')
    def test_bad_character(self):
        c=self.cfg();c['companion']['character']='dog'
        with self.assertRaises(build.ConfigError):build.validate(c,ROOT/'config.json')
    def test_modes(self):
        for mode in ('github','showcase'):
            c=self.cfg();c['layout_mode']=mode
            self.assertEqual(build.validate(c,ROOT/'config.json')['layout_mode'],mode)
    def test_preview_widths(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            build.write_preview(build.validate(self.cfg(),ROOT/'config.json'),tmp)
            html=(Path(tmp)/'preview.html').read_text()
            self.assertIn('max-width:1100px',html)
