import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

import build

ROOT = Path(__file__).resolve().parents[1]
NS = {'s': 'http://www.w3.org/2000/svg'}


class ReadingFontTests(unittest.TestCase):
    def test_reading_and_terminal_fonts_are_separate(self):
        cfg = build.validate(json.loads((ROOT / 'config.json').read_text(encoding='utf-8')), ROOT / 'config.json')
        for theme in ('paper', 'violet'):
            sections = build.render_sections(cfg, theme)
            root = ET.fromstring(sections['hero'][0])
            texts = {node.text: node.attrib['font-family'] for node in root.findall('.//s:text', NS)}
            terminal = texts[cfg['profile']['username'] + '@github:~']
            prose = texts[cfg['profile']['tagline_zh']]
            self.assertIn('Microsoft YaHei', prose)
            self.assertNotEqual(prose, terminal)
            self.assertIn('Mono', terminal)
            self.assertEqual(texts[cfg['projects'][0]['description']], prose)
            self.assertEqual(texts['› ' + cfg['about']['lines'][0]], prose)
            self.assertEqual(texts['› ' + cfg['now'][0]], prose)
