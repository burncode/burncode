import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import build
from profilegen.svg import Canvas
from profilegen.components import companion

ROOT=Path(__file__).resolve().parents[1]


class PetCatsPackTests(unittest.TestCase):
    def test_native_walk_has_all_eight_original_frames_without_deformation(self):
        canvas=Canvas(build.load_theme('paper'))
        companion.render(canvas,0,{'companion':{'character':'classic_cat','animation':'walk'}})
        root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
        art=root.find('.//g[@id="companion-pose"]')
        self.assertEqual(art.get('data-source'),'LuizMelo/Pet Cats Pack')
        self.assertEqual(art.get('transform'),'scale(2)')
        self.assertEqual(len(root.findall('.//defs/g[@data-action="Walk"]')),8)
        self.assertFalse(art.findall('.//animateTransform'))

    def test_original_colors_are_identical_across_themes(self):
        paths=[]
        for theme in ('paper','violet'):
            canvas=Canvas(build.load_theme(theme))
            companion.render(canvas,0,{'companion':{'character':'tuxedo_cat','animation':'walk'}})
            root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
            paths.append([n.attrib for n in root.findall('.//defs/g/path[@data-role="source-pixels"]')])
        self.assertTrue(paths[0])
        self.assertEqual(paths[0],paths[1])

    def test_all_original_pixels_and_alpha_survive_import(self):
        # Pillow is a development-only dependency; normal build remains stdlib.
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Pillow unavailable for source PNG comparison')
        import zipfile
        from io import BytesIO
        data=companion._pack()
        with zipfile.ZipFile(ROOT/'assets/pet-cats-pack.zip') as archive:
            for cat in data['characters'].values():
                for action in cat['actions'].values():
                    sheet=Image.open(BytesIO(archive.read(action['source']))).convert('RGBA')
                    for i,runs in enumerate(action['frames']):
                        restored=Image.new('RGBA',(50,50))
                        for x,y,length,color in runs:
                            rgba=tuple(bytes.fromhex(color[1:]))
                            if len(rgba)==3:rgba+=(255,)
                            for px in range(x+12,x+12+length):restored.putpixel((px,y+14),rgba)
                        frame=sheet.crop((i*50,0,(i+1)*50,50))
                        expected=[px if px[3] else (0,0,0,0) for px in frame.get_flattened_data()]
                        self.assertEqual(list(restored.get_flattened_data()),expected)

    def test_sleep_uses_original_lying_sleeping_and_waking_frames(self):
        canvas=Canvas(build.load_theme('paper'))
        companion.render(canvas,0,{'companion':{'animation':'story','duration':24}})
        root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
        actions={g.get('data-action') for g in root.findall('.//defs/g')}
        self.assertTrue({'Walk','Idle','Laying','Sleeping1','Stretching','Meow'}<=actions)

    def test_static_uses_original_sitting_without_animations(self):
        canvas=Canvas(build.load_theme('paper'))
        companion.render(canvas,0,{'companion':{'animation':'static'}})
        root=ET.fromstring('<svg>'+''.join(canvas.parts)+'</svg>')
        self.assertFalse(root.findall('.//animateTransform'))
        self.assertFalse(root.findall('.//animate'))
        self.assertEqual(root.find('.//defs/g').get('data-action'),'Sitting')

    def test_imported_frame_counts(self):
        data=json.loads((ROOT/'assets/companions/pet-cats/frames.json').read_text())
        self.assertEqual(data['license'],'CC0-1.0')
        for cat in data['characters'].values():
            self.assertEqual(len(cat['actions']['Walk']['frames']),8)
            self.assertEqual(len(cat['actions']['Idle']['frames']),10)
            self.assertEqual(len(cat['actions']['Stretching']['frames']),13)
