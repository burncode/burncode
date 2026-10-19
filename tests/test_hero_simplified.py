import copy
import json
import unittest
from pathlib import Path
import build

ROOT = Path(__file__).resolve().parents[1]


class HeroTests(unittest.TestCase):
    def test_retired_fields_rejected_and_not_required(self):
        cfg = json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
        cfg['profile'].pop('tags', None)
        cfg['profile'].pop('system', None)
        valid = build.validate(cfg, ROOT/'config.json')
        svg = build.render_sections(valid, 'paper')['hero'][0]
        self.assertIn('[ code | build | explore ]', svg)
        self.assertNotIn('MODE:', svg)
        for field, value in [('tags', ['unused']), ('system', {})]:
            old = copy.deepcopy(cfg)
            old['profile'][field] = value
            with self.assertRaises(build.ConfigError):
                build.validate(old, ROOT/'config.json')
