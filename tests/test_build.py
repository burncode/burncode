# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.text import wrap,ellipsize,width


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=build.read_json(ROOT/'config.json')

    def validate(self,config=None):
        return build.validate(config or self.config,ROOT/'config.json')

    def test_default_config(self):
        self.assertEqual(self.validate()['profile']['username'],'burncode')

    def test_single_theme_cli_fixed(self):
        cfg=copy.deepcopy(self.config)
        args=type('Args',(),{'themes':'mono','light':None,'dark':None})()
        build.resolve_theme_selection(cfg,args)
        self.assertEqual(cfg['themes']['light'],'mono')
        self.assertEqual(cfg['themes']['dark'],'mono')
        self.assertEqual(cfg['themes']['generate'],['mono'])
        self.validate(cfg)

    def test_two_theme_cli_fixed(self):
        cfg=copy.deepcopy(self.config)
        args=type('Args',(),{'themes':'mono,amber','light':None,'dark':None})()
        build.resolve_theme_selection(cfg,args)
        self.assertEqual((cfg['themes']['light'],cfg['themes']['dark']),('mono','amber'))

    def test_theme_plugins(self):
        for name in build.theme_names():
            theme=build.load_theme(name)
            self.assertIn('fonts',theme)
            self.assertIn('style',theme)

    def test_reorder_and_hide(self):
        cfg=copy.deepcopy(self.config)
        cfg['layout_mode']='showcase'
        cfg['layout']=[{'type':'footer','enabled':True},{'type':'projects','enabled':False},{'type':'hero','enabled':True}]
        svg=build.render(self.validate(cfg),'mono')
        self.assertLess(svg.index('Session closed.'),svg.index('burncode@github:~</text>'))
        self.assertNotIn('./projects',svg)

    def test_long_cjk_and_latin_wrap(self):
        text='超长中文项目名称与EnglishWordsMixedTogetherWithoutAnySpaces' * 4
        lines=wrap(text,250,14,2)
        self.assertLessEqual(len(lines),2)
        self.assertTrue(all(width(line,14)<=255 for line in lines))
        self.assertTrue(ellipsize(text,100,14).endswith('…'))

    def test_escape_svg_injection(self):
        cfg=copy.deepcopy(self.config)
        cfg['projects'][0]['name']='A <B> & "C"'
        svg=build.render(self.validate(cfg),'mono')
        self.assertIn('A &lt;B&gt; &amp;',svg)
        self.assertNotIn('<B>',svg)

    def test_long_description_not_overflow(self):
        cfg=copy.deepcopy(self.config)
        cfg['projects'][0]['description']='中文Chinese ' * 35
        svg=build.render(self.validate(cfg),'mono')
        self.assertIn('<svg',svg)
        self.assertNotIn('中文Chinese '*35,svg)

    def test_write_and_guard(self):
        cfg=self.validate()
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            paths=build.build(cfg,root)
            self.assertGreaterEqual(len(paths),1+len(cfg["themes"]["generate"]))
            self.assertTrue((root/'README.md').exists())
            build.build(cfg,root)
            (root/'README.md').write_text('personal content')
            with self.assertRaises(build.ConfigError):build.build(cfg,root)

    def test_single_theme_subprocess(self):
        p=subprocess.run([sys.executable,str(ROOT/'build.py'),'--themes','mono','--check'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)

    def test_invalid_theme(self):
        with self.assertRaises(build.ConfigError):build.load_theme('../oops')

    def test_invalid_layout(self):
        cfg=copy.deepcopy(self.config)
        cfg['layout']=[{'type':'unknown'}]
        with self.assertRaises(build.ConfigError):self.validate(cfg)


if __name__=='__main__':unittest.main()

class DiagnosticsTests(unittest.TestCase):
    def test_file_state_and_idempotence(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'), ROOT/'config.json')
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            first=build.build(cfg,root)
            self.assertTrue(all(state=='CREATE' for _,state in first))
            second=build.build(cfg,root)
            self.assertTrue(all(state=='UNCHANGED' for _,state in second))
            cfg['profile']['tagline']='Changed tagline'
            third=build.build(cfg,root)
            self.assertEqual(dict((p.name,state) for p,state in third)['README.md'],'UNCHANGED')
            self.assertEqual(dict((p.name,state) for p,state in third)['hero.svg'],'UPDATE')
    def test_check_reports_themes(self):
        p=subprocess.run([sys.executable,str(ROOT/'build.py'),'--check'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('Light theme:  '+build.read_json(ROOT/'config.json')['themes']['light'],p.stdout)
        self.assertIn('Dark theme:   '+build.read_json(ROOT/'config.json')['themes']['dark'],p.stdout)
    def test_dry_run_no_write(self):
        p=subprocess.run([sys.executable,str(ROOT/'build.py'),'--dry-run'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('Dry run',p.stdout)


class V107Tests(unittest.TestCase):
    def test_header_configuration_and_cat_toggle(self):
        cfg=build.read_json(ROOT/'config.json')
        cfg['header_nav']=['projects','notes']
        cfg['header_cat']=False
        svg=build.render(build.validate(cfg,ROOT/'config.json'),'mono')
        self.assertIn('[ projects | notes ]',svg)
        self.assertNotIn('cat_y',svg)

    def test_header_rejects_bad_configuration(self):
        cfg=build.read_json(ROOT/'config.json')
        cfg['header_cat']='yes'
        with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')

    def test_textual_stats_in_middle_column(self):
        cfg=build.read_json(ROOT/'config.json')
        cfg['projects'][0]['stars']=19
        cfg['projects'][0]['forks']=11
        svg=build.render(build.validate(cfg,ROOT/'config.json'),'mono')
        self.assertIn('>19</text>',svg)
        self.assertIn('>11</text>',svg)
        self.assertNotIn('>⑂</text>',svg)

    def test_theme_style_controls(self):
        t=build.load_theme('mono')
        self.assertIn('divider_color',t['components']['projects'])
        self.assertIn('stat_background',t['components']['projects'])

    def test_three_equal_footer_columns(self):
        cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        cfg['layout_mode']='showcase'
        svg=build.render(cfg,'mono')
        self.assertIn('M367 ',svg)
        self.assertIn('M734 ',svg)

class ModularConnectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
        for item in cls.cfg['layout']:
            if item['type']=='social':item['enabled']=True

    def test_social_rows_are_clickable_and_no_duplicate_footer(self):
        html=build.make_readme(self.cfg)
        self.assertIn('connect-1.svg',html)
        self.assertIn('connect-2.svg',html)
        self.assertIn('title="Open GitHub"',html)
        self.assertIn('target="_blank"',html)
        self.assertNotIn('<p align="center">',html)

    def test_connect_rows_are_valid_svg(self):
        import xml.etree.ElementTree as ET
        strips=build.render_sections(self.cfg,'mono')
        for i in range(1,3):
            svg,url=strips[f'connect-{i}']
            ET.fromstring(svg)
            self.assertTrue(url.startswith('https://'))
        self.assertLess(float(ET.fromstring(strips['connect-1'][0]).get('width')),240)

    def test_preview_matches_modular_links(self):
        preview=build.make_preview_html(self.cfg)
        self.assertIn('connect-1.svg',preview)
        self.assertIn('Open Repositories',preview)
        self.assertNotIn('GitHub · Repositories',preview)

class V113Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')

    def test_theme_labels_are_next_to_generated_theme_names(self):
        raw=build.read_json(ROOT/'config.json')
        self.assertNotIn('theme_catalog',raw)
        self.assertEqual(raw['themes']['generate']['mono'],'light')
        self.assertEqual(raw['themes']['generate']['graphite'],'dark')
        self.assertIn('mono',self.cfg['themes']['generate'])

    def test_wrong_inline_theme_label_is_rejected(self):
        raw=build.read_json(ROOT/'config.json')
        raw['themes']['generate']['mono']='dark'
        with self.assertRaisesRegex(build.ConfigError,'actual theme mode'):
            build.validate(raw,ROOT/'config.json')

    def test_icon_catalog(self):
        self.assertEqual(self.cfg['projects'][0]['icon'],'terminal')
        cfg=build.read_json(ROOT/'config.json')
        cfg['projects'][0]['icon']='unknown'
        with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')

    def test_motto_is_separate(self):
        svg=build.render(self.cfg,'mono')
        self.assertIn('Session closed. Ideas still running.',svg)
        modular=build.make_readme(self.cfg)
        self.assertIn('motto.svg',modular)
        self.assertLess(modular.index('projects-heading.svg'),modular.index('motto.svg'))
        # Social may be disabled or independently reordered; footer is the closing block.
        self.assertLess(modular.index('motto.svg'),modular.index('footer.svg'))

    def test_optional_widgets(self):
        cfg=build.read_json(ROOT/'config.json')
        for widget in ('github_stats',):
            cfg['widgets'][widget]['enabled']=True
            for component in cfg['layout']:
                if component['type']==widget:component['enabled']=True
        checked=build.validate(cfg,ROOT/'config.json')
        svg=build.render(checked,'mono')
        self.assertIn('Featured stars',svg)
