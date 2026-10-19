# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""v10.5 theme scene and hero variants regression tests."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.components.studio import SCENES

class ThemeIdentityTests(unittest.TestCase):
    def test_all_theme_scenes_and_variants(self):
        for name in build.theme_names():
            with self.subTest(name=name):
                t=build.load_theme(name)
                self.assertIn(t['studio']['scene'],SCENES)
                self.assertIn(t['components']['hero']['variant'],('classic','compact','editorial'))
    def test_scene_styles_are_distinct(self):
        pairs={(build.load_theme(n)['studio']['scene'],build.load_theme(n)['components']['hero']['variant']) for n in build.theme_names()}
        self.assertGreaterEqual(len(pairs),5)
    def test_invalid_variant_rejected(self):
        p=ROOT/'profilegen/themes/mono.json'
        import json
        original=p.read_text(encoding='utf-8')
        try:
            data=json.loads(original)
            data['components']['hero']['variant']='injected'
            p.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaises(build.ConfigError):build.load_theme('mono')
        finally:
            p.write_text(original,encoding='utf-8')
    def test_render_every_scene(self):
        from profilegen.svg import Canvas
        from profilegen.components.studio import render
        for scene in SCENES:
            with self.subTest(scene=scene):
                canvas=Canvas(build.load_theme('mono'))
                render(canvas,0,0,368,243,scene)
                result=''.join(canvas.parts)
                if scene=='none':self.assertFalse(result)
                else:self.assertIn('</g>',result)

if __name__=='__main__':unittest.main()
