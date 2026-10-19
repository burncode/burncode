# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import copy,json,tempfile,unittest,sys,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from profilegen.providers.releases import refresh,load
ROOT=Path(__file__).resolve().parents[1]
class V116Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
 def test_tags_not_truncated(self):
  cfg=copy.deepcopy(self.cfg);cfg['projects'][0]['tags']=['Python','Excel','Automation']
  svg=build.render(cfg,'mono')
  for t in cfg['projects'][0]['tags']:self.assertIn('>'+t+'</text>',svg)
  self.assertNotIn('>Aut...</text>',svg)
 def test_stats_five_and_cat_shift(self):
  cfg=copy.deepcopy(self.cfg);cfg['_account']={'followers':8,'following':5,'public_repos':40,'public_gists':1}
  svg=build.render(cfg,'mono');self.assertIn('Featured stars',svg);self.assertIn('translate(1036 ',svg)
 def test_social_brand_mark(self):
  strips=build.render_sections(self.cfg,'mono')
  s=strips['connect-1'][0];ET.fromstring(s)
  self.assertIn('viewBox="0 0 99 38"',s)
  self.assertNotIn('>GH</text>',s)
 def test_focus_removed_from_default_layout(self):
  self.assertNotIn('development_focus',[x['type'] for x in self.cfg['layout']])
 def test_release_provider_cache(self):
  class Fake:
   def __enter__(self):return self
   def __exit__(self,*a):return False
   def read(self):return json.dumps({'tag_name':'v2.1','published_at':'2026-10-10T12:00:00Z','html_url':'https://github.com/a/b/releases/tag/v2.1'}).encode()
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'releases.json'
   data,status=refresh(['a/b'],path,fetcher=lambda _:Fake())
   self.assertEqual(status,'updated');self.assertEqual(data['items'][0]['tag'],'v2.1')
   self.assertEqual(load(path)['items'][0]['repo'],'a/b')
   data,status=refresh(['a/b'],path,force=True,fetcher=lambda _:(_ for _ in ()).throw(OSError('offline')))
   self.assertEqual(status,'stale')
 def test_release_widget_no_fake_data(self):
  cfg=copy.deepcopy(self.cfg);cfg['widgets']['recent_releases']['enabled']=True
  svg=build.render(cfg,'mono');self.assertIn('最近发布',svg)
  self.assertNotIn('v2.1',svg)
if __name__=='__main__':unittest.main()
