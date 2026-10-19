import unittest
from xml.etree import ElementTree as ET
from profilegen.svg import Canvas
from profilegen.widgets import about
import build


class AboutSpacingTests(unittest.TestCase):
    def test_full_labels_and_balanced_spacing(self):
        labels = ['Open Source', 'Developer Tools', 'Creative Coding'] * 4
        canvas = Canvas(build.load_theme('paper'))
        canvas.density = 'showcase'
        height = about.render(canvas, {'about': {'lines': ['First', 'Second'], 'highlights': labels}}, 0, {})
        root = ET.fromstring('<svg>' + ''.join(canvas.parts) + '</svg>')
        texts = root.findall('text')
        for label in set(labels):
            self.assertEqual(sum(t.text == label for t in texts), 4)
        chips = [r for r in root.findall('rect') if r.get('height') == '28']
        self.assertEqual(len(chips), len(labels))
        self.assertGreater(len({r.get('y') for r in chips}), 1)
        self.assertTrue(all(float(r.get('x')) + float(r.get('width')) <= 1065 for r in chips))
        bottom = max(float(r.get('y')) + float(r.get('height')) for r in chips)
        self.assertEqual(height - bottom, 22)
