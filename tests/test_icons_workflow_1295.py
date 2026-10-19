# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest
from pathlib import Path
from profilegen.icons.headings import icon_svg, SECTION_ICONS
from profilegen.icons.brands import mark

ROOT = Path(__file__).resolve().parents[1]

class IconsWorkflow1295(unittest.TestCase):
    def test_all_sections_have_mapping(self):
        for key in ('about','projects','languages','activity','now','stats','blog','recent_releases'):
            self.assertIn(key, SECTION_ICONS)
    def test_missing_icon_same_default(self):
        self.assertEqual(icon_svg('totally_unknown_section',0,0,20,'#333333'),
                         icon_svg('default',0,0,20,'#333333'))
    def test_missing_social_icon_not_blank(self):
        self.assertIn('<svg',mark('not-a-real-brand',0,0,'#333333'))
    def test_workflow_all_cache_targets(self):
        workflow=(ROOT/'.github/workflows/update-profile.yml').read_text(encoding='utf-8')
        for cache in ('github.json','account.json','contributions.json','languages.json','releases.json','blog_feed.json'):
            self.assertIn(cache,workflow)
        self.assertIn('--refresh-data',workflow)
        self.assertIn('assets/sections/',workflow)
    def test_documented_headings(self):
        doc=(ROOT/'ICONS.md').read_text(encoding='utf-8')
        for filename in ('user.svg','folder.svg','code.svg','git-branch.svg','rss.svg','chart-bar.svg'):
            self.assertIn(filename,doc)

if __name__=='__main__': unittest.main()
