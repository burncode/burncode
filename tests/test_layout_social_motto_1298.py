# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Regression tests for independently ordered social and restored motto."""
import copy
import json
import unittest
from pathlib import Path
import build

ROOT=Path(__file__).resolve().parents[1]

class LayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))

    def test_social_can_be_first_last_or_disabled(self):
        for index in (0,3,100):
            cfg=copy.deepcopy(self.original)
            cfg['layout']=[x for x in cfg['layout'] if x['type']!='social']
            cfg['layout'].insert(min(index,len(cfg['layout'])),{'type':'social','enabled':True})
            cfg=build.validate(cfg,ROOT/'config.json')
            readme=build.make_readme(cfg)
            self.assertIn('social-toolbar',readme)
            # Match the actual order of enabled layout sections, ignoring internal gap SVGs.
            positions=[]
            for item in cfg['layout']:
                kind=item['type']
                if not item.get('enabled',True):continue
                if kind=='social':marker='class="social-toolbar"'
                elif kind=='projects':marker='/projects-heading.svg'
                elif kind=='blog':marker='/blog-heading.svg'
                else:marker=f'/{kind}.svg'
                if marker in readme:positions.append((kind,readme.index(marker)))
            self.assertEqual([x[0] for x in positions],[x[0] for x in sorted(positions,key=lambda x:x[1])])
        cfg=copy.deepcopy(self.original)
        next(x for x in cfg['layout'] if x['type']=='social')['enabled']=False
        cfg=build.validate(cfg,ROOT/'config.json')
        self.assertNotIn('social-toolbar',build.make_readme(cfg))

    def test_no_implicit_social_when_not_in_layout(self):
        cfg=copy.deepcopy(self.original)
        cfg['layout']=[x for x in cfg['layout'] if x['type']!='social']
        cfg=build.validate(cfg,ROOT/'config.json')
        self.assertNotIn('social-toolbar',build.make_readme(cfg))

    def test_motto_uses_original_terminal_echo(self):
        cfg=build.validate(copy.deepcopy(self.original),ROOT/'config.json')
        self.assertIn('$MOTTO',build.render_sections(cfg,cfg['themes']['light'])['motto'][0])
        self.assertIn('echo',build.render_sections(cfg,cfg['themes']['light'])['motto'][0])
