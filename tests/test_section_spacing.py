import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import build

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}


class SectionSpacingTests(unittest.TestCase):
    def test_exported_sections_have_no_embedded_bottom_spacer(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        for name,(svg,_) in build.render_sections(cfg,'mono').items():
            if name.startswith('connect-'):continue
            root=ET.fromstring(svg)
            clip=root.find('.//s:clipPath/s:rect',NS)
            self.assertAlmostEqual(float(root.get('height')),float(clip.get('height'))-.5,msg=name)

    def test_preview_uses_native_image_alignment_instead_of_css_gap_hack(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        preview=build.make_preview_html(cfg)
        self.assertNotIn('.readme>div{line-height:0}',preview)
        self.assertNotIn('.readme>div img{display:block',preview)
        self.assertIn('font-size:16px;line-height:1.5',preview)
        self.assertIn('align="top"',preview)
        self.assertIn('align="top"',build.make_readme(cfg))
