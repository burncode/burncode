# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest
from pathlib import Path
import json
import build

class V10Tests(unittest.TestCase):
    def setUp(self):
        self.config=build.read_json(Path('config.json'))
    def test_localization(self):
        self.config['i18n']={'locale':'zh-CN'}
        cfg=build.validate(self.config,Path('config.json'))
        self.assertIn('项目',build.render(cfg,'mono'))
    def test_social(self):
        for item in self.config['layout']:
            if item['type']=='social':item['enabled']=True
        cfg=build.validate(self.config,Path('config.json'))
        self.assertIn('GitHub',build.make_readme(cfg))
    def test_metric(self):
        self.config['projects'][0]['stars']=42
        cfg=build.validate(self.config,Path('config.json'))
        self.assertIn('42',build.render(cfg,'mono'))
    def test_invalid_metric(self):
        self.config['projects'][0]['stars']=-1
        with self.assertRaises(build.ConfigError):build.validate(self.config,Path('config.json'))
if __name__=='__main__':unittest.main()
