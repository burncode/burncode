import unittest
import xml.etree.ElementTree as ET
import build
from profilegen.svg import Canvas
from profilegen.components import companion


class CompanionBannerTests(unittest.TestCase):
    def test_speech_bubble_has_rounded_body_and_tail_toward_cat(self):
        canvas=Canvas(build.load_theme('paper'))
        companion.render(canvas,0,{'companion':{'animation':'story','sequence':['banner'],'banner':'Hello'}})
        root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
        bubble=root.find('.//g[@id="companion-banner"]')
        self.assertGreaterEqual(float(bubble.find('rect').get('rx')),4)
        tail=bubble.find('path[@id="companion-speech-tail"]')
        self.assertIsNotNone(tail)
        self.assertEqual(tail.get('stroke'),canvas.c['accent'])
        self.assertEqual(bubble.find('text').text,'Hello')

    def test_banner_resizes_for_complete_text_and_keeps_cat_side_anchored(self):
        for density in ('showcase', 'github'):
            widths=[]
            for message in ('Hi', 'I love you', '你好，世界！', 'A very long banner'):
                canvas=Canvas(build.load_theme('paper'))
                canvas.density=density
                companion.render(canvas,0,{'companion':{'animation':'story','sequence':['banner'],'banner':message}})
                root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
                banner=root.find('.//g[@id="companion-banner"]')
                rect=banner.find('rect');text=banner.find('text')
                self.assertEqual(text.text,message)
                self.assertAlmostEqual(float(rect.get('x'))+float(rect.get('width')),-9)
                self.assertEqual(float(text.get('x'))-float(rect.get('x')),8)
                widths.append(float(rect.get('width')))
            self.assertLess(widths[0],widths[1])
            self.assertLess(widths[1],widths[3])

    def test_direction_changes_at_return_leg_without_mirroring_banner(self):
        for motion, turn in [('walk', '0.5'), ('wander', '0.48'), ('story', '0.80')]:
            with self.subTest(motion=motion):
                canvas = Canvas(build.load_theme('paper'))
                companion.render(canvas, 0, {'companion': {'animation': motion}})
                root = ET.fromstring('<svg>' + ''.join(canvas.parts) + '</svg>')
                facing = root.find('.//g[@id="companion-facing"]')
                self.assertIsNotNone(facing)
                animation = facing.find('animateTransform')
                self.assertEqual(animation.get('values'), '1 1;-1 1;1 1')
                self.assertEqual([float(t) for t in animation.get('keyTimes').split(';')], [0,float(turn),1])
                self.assertEqual(animation.get('calcMode'), 'discrete')
                self.assertIsNone(facing.find('.//g[@id="companion-banner"]'))

    def test_banner_follows_track_without_body_deformation(self):
        canvas = Canvas(build.load_theme('paper'))
        companion.render(canvas, 0, {'companion': {'animation': 'story', 'sequence': ['walk', 'banner'], 'banner': 'Hello'}})
        root = ET.fromstring('<svg>' + ''.join(canvas.parts) + '</svg>')
        pose = root.find('.//g[@id="companion-pose"]')
        banner = root.find('.//g[@id="companion-banner"]')
        self.assertIsNotNone(banner)
        self.assertIsNone(pose.find('.//g[@id="companion-banner"]'))
        sprite = root.find('.//g[@id="companion-sprite"]')
        self.assertIn(banner, list(sprite))
        self.assertFalse(pose.findall('.//animateTransform'))
        self.assertEqual(pose.get('data-source'),'LuizMelo/Pet Cats Pack')
