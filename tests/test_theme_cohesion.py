import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import build

ROOT = Path(__file__).resolve().parents[1]


class ThemeCohesionTests(unittest.TestCase):
    def test_all_themes_have_readable_fonts_and_matching_studio_background(self):
        for name in build.theme_names():
            with self.subTest(theme=name):
                theme = build.load_theme(name)
                for family in ('body', 'heading', 'reading'):
                    self.assertIn('Microsoft YaHei', theme['fonts'][family])
                asset = ROOT/'assets'/'studio'/(theme['studio']['asset']+'.svg')
                root = ET.parse(asset).getroot()
                self.assertEqual(list(root)[0].get('fill'), theme['colors']['background'])

    def test_paper_palette_is_preserved(self):
        theme = build.load_theme('paper')
        self.assertEqual(theme['colors']['background'], '#fffdf8')
        self.assertEqual(theme['colors']['accent'], '#b65f3d')
