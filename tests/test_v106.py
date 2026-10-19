# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import sys, unittest, tempfile, io, contextlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.components.studio import render_asset
from profilegen.svg import Canvas

class V106Tests(unittest.TestCase):
    def test_console_gbk(self):
        class GBK:
            encoding='gbk'
            def __init__(self):self.output=''
            def write(self,s):self.output+=s
            def flush(self):pass
        sink=GBK()
        build.console_print('  ✓ ↻ ◆ 你好',stream=sink)
        sink.output.encode('gbk')
        self.assertIn('你好',sink.output)
    def test_studio_assets_inline(self):
        for name in ('studio-day','studio-night'):
            c=Canvas(build.load_theme('mono'))
            render_asset(c,0,0,354,241,name)
            self.assertIn('viewBox', ''.join(c.parts))
    def test_reject_asset_path(self):
        c=Canvas(build.load_theme('mono'))
        with self.assertRaises(ValueError):render_asset(c,0,0,354,241,'../etc/passwd')
    def test_render_theme_asset(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        self.assertIn('preserveAspectRatio',build.render(cfg,'mono'))
