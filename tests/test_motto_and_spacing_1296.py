# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import json
import unittest
from pathlib import Path
from profilegen.svg import Canvas
from profilegen.components.motto import render as motto_render
from profilegen.components.footer import render as footer_render
from profilegen.widgets.fastfetch import render as device_render

ROOT=Path(__file__).resolve().parents[1]

class MottoSpacingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
        cls.theme=json.loads((ROOT/'profilegen/themes/mono.json').read_text(encoding='utf-8'))

    def test_motto_and_closing_both_visible(self):
        c=Canvas(self.theme)
        h=motto_render(c,self.cfg,0,{})
        svg=''.join(c.parts)
        self.assertGreaterEqual(h,60)
        for line in self.cfg['motto']:
            self.assertIn(line,svg)
        self.assertIn('$MOTTO',svg)
        self.assertNotIn('Session closed.',svg)
        f=Canvas(self.theme)
        footer_render(f,self.cfg,0,{})
        footer_svg=''.join(f.parts)
        self.assertIn('Session closed.',footer_svg)
        for line in self.cfg['motto']:
            self.assertNotIn(line,footer_svg)

    def test_device_value_rail_is_not_fixed_at_423(self):
        c=Canvas(self.theme)
        device_render(c,self.cfg,0,{})
        svg=''.join(c.parts)
        self.assertNotIn('x="423"',svg)
        self.assertIn('Arch Linux',svg)
