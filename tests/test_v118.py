# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest,tempfile,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from profilegen.providers.feeds import parse,refresh,load
ROOT=Path(__file__).resolve().parents[1]
class V118Tests(unittest.TestCase):
 def test_rss(self):
  self.assertEqual(parse(b'<rss><channel><item><title>A</title><link>https://example.com/a</link></item></channel></rss>')[0]['title'],'A')
 def test_atom(self):
  self.assertEqual(parse(b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>B</title><link href="https://example.com/b"/></entry></feed>')[0]['url'],'https://example.com/b')
 def test_reject_insecure_links(self):
  self.assertEqual(parse(b'<rss><channel><item><title>A</title><link>javascript:alert(1)</link></item></channel></rss>'),[])
 def test_blog_style(self):
  cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
  cfg['_blog_posts']=[{'title':'A sample post','url':'https://example.com/a'}]
  svg=build.render(cfg,'mono')
  self.assertIn('A sample post',svg)
  self.assertNotIn('示例 · 请替换',svg)
  self.assertEqual(build.render_sections(cfg,'mono')['blog-1'][1],'https://example.com/a')
 def test_feed_config_validation(self):
  cfg=build.read_json(ROOT/'config.json');cfg['widgets']['blog'].update({'source':'rss','feed_url':'http://example.com/feed'})
  with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')
