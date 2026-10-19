import copy
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import build
from profilegen.components import companion
from profilegen.svg import Canvas

ROOT=Path(__file__).resolve().parents[1]


class FullCatalogTests(unittest.TestCase):
    def test_all_six_cats_and_native_actions_are_configurable(self):
        self.assertEqual(len(companion.CHARACTERS),6)
        for character in companion.CHARACTERS:
            for action in companion.ACTIONS:
                if character=='classic_cat' and action=='itch':continue
                cfg=build.read_json(ROOT/'config.json')
                cfg['companion']={'character':character,'animation':action}
                checked=build.validate(cfg,ROOT/'config.json')
                canvas=Canvas(build.load_theme('paper'))
                companion.render(canvas,0,checked)
                root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
                ids={n.get('id') for n in root.iter() if n.get('id')}
                self.assertTrue(all(not any(c.isspace() for c in ident) for ident in ids))
                self.assertTrue(all(n.get('href')[1:] in ids for n in root.iter('use')))

    def test_banner_can_be_selected_without_story(self):
        canvas=Canvas(build.load_theme('paper'))
        companion.render(canvas,0,{'companion':{'animation':'banner','banner':'Hi'}})
        root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
        self.assertEqual(root.find('.//g[@id="companion-banner"]/text').text,'Hi')

    def test_one_shot_actions_freeze_on_final_frame(self):
        for action in ('lay_down','stretch'):
            canvas=Canvas(build.load_theme('paper'))
            companion.render(canvas,0,{'companion':{'animation':action}})
            root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
            animations=root.findall('.//use/animate')
            self.assertTrue(animations)
            self.assertTrue(all(a.get('repeatCount')=='1' and a.get('fill')=='freeze' for a in animations))

    def test_auto_outline_only_on_dark_theme_black_cat_and_can_be_disabled(self):
        for theme,outline,expected in [('paper','auto',False),('violet','auto',True),('violet','off',False),('paper','on',True)]:
            canvas=Canvas(build.load_theme(theme))
            companion.render(canvas,0,{'companion':{'character':'tuxedo_cat','animation':'walk','outline':outline}})
            root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
            self.assertEqual(bool(root.findall('.//path[@data-role="contrast-outline"]')),expected)

    def test_missing_original_itch_is_reported(self):
        cfg=build.read_json(ROOT/'config.json')
        cfg['companion']={'character':'classic_cat','animation':'itch'}
        with self.assertRaisesRegex(build.ConfigError,'Itch'):
            build.validate(cfg,ROOT/'config.json')
