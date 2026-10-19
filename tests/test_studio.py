# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build import read_json, validate, render, ConfigError
ROOT=Path(__file__).resolve().parents[1]

class StudioTests(unittest.TestCase):
    def test_theme_scene_variation(self):
        cfg=validate(read_json(ROOT/'config.json'),ROOT/'config.json')
        self.assertNotEqual(render(cfg,'mono'),render(cfg,'graphite'))
    def test_invalid_scene_rejected(self):
        cfg=read_json(ROOT/'config.json')
        cfg['studio']={'scene':'unsupported'}
        with self.assertRaises(ConfigError):validate(cfg,ROOT/'config.json')
    def test_scene_override(self):
        cfg=read_json(ROOT/'config.json')
        cfg['layout'][0]['options']={'scene':'workshop'}
        self.assertIn('<svg',render(validate(cfg,ROOT/'config.json'),'mono'))
