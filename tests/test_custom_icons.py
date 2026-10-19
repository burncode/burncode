# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
from profilegen.icons import svg_icons

class CustomIcons(unittest.TestCase):
 def test_only_custom_source(self):
  self.assertNotIn('vendor',str(svg_icons.ROOT))
  with tempfile.TemporaryDirectory() as t:
   root=Path(t); (root/'outline').mkdir()
   (root/'outline'/'brand-github.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M1 2h3"/></svg>')
   with patch.object(svg_icons,'ROOT',root):
    svg_icons._load.cache_clear()
    self.assertIn('<path',svg_icons.draw('github',0,0,24,'#123456'))
    self.assertEqual('',svg_icons.draw('nonexistent',0,0,24,'#123456'))
    ET.fromstring(svg_icons.draw('github',0,0,24,'#123456'))
   svg_icons._load.cache_clear()
 def test_reject_traversal(self):
  self.assertEqual('',svg_icons.draw('../escape',0,0,24,'#222'))

class DeviceAndReadme(unittest.TestCase):
 def test_animated_logo_and_contrast(self):
  import build
  from profilegen.widgets import fastfetch
  from profilegen.svg import Canvas
  from pathlib import Path
  cfg=build.validate(build.read_json(Path(__file__).resolve().parents[1]/'config.json'),Path(__file__).resolve().parents[1]/'config.json')
  cfg['device']['logo']='arch'
  cfg['device']['logo_animate']=True
  canvas=Canvas(build.load_theme('mono'))
  fastfetch.render(canvas,cfg,0,{})
  text=''.join(canvas.parts)
  self.assertIn('attributeName="opacity"',text)
  self.assertIn('OS:',text)
  self.assertIn('Arch Linux',text)
  self.assertNotIn('Model:',text)
 def test_logo_animation_requires_boolean(self):
  import build,copy
  from pathlib import Path
  path=Path(__file__).resolve().parents[1]/'config.json'
  cfg=build.read_json(path);cfg['device']['logo_animate']='yes'
  with self.assertRaises(build.ConfigError):build.validate(cfg,path)
 def test_readme_no_changelog(self):
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  text=(root/'README.md').read_text()
  self.assertNotIn('## Changelog',text)
  self.assertNotIn('更新日志',text)
