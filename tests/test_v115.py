# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from profilegen.providers.account import refresh,load
ROOT=Path(__file__).resolve().parents[1]
class V115Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cfg=build.validate(build.read_json(ROOT/'config.json'),ROOT/'config.json')
 def test_zero_metrics_hidden(self):
  cfg=copy.deepcopy(self.cfg);cfg['projects'][0]['stars']=0;cfg['projects'][0]['forks']=0
  from profilegen.components.projects import render
  from profilegen.svg import Canvas
  c=Canvas(build.load_theme('mono'));render(c,cfg,0,{})
  self.assertNotIn('>0</text>',''.join(c.parts))
 def test_about_and_social(self):
  s=build.render(self.cfg,'mono');self.assertIn('关于我',s)
  cfg=copy.deepcopy(self.cfg)
  for item in cfg['layout']:
   if item['type']=='social':item['enabled']=True
  md=build.make_readme(cfg)
  self.assertIn('width="99"',md)
 def test_account_cache_and_failure(self):
  class Fake:
   headers={}
   def __enter__(self):return self
   def __exit__(self,*a):return False
   def read(self):return json.dumps({'followers':8,'following':5,'public_repos':14,'public_gists':1}).encode()
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'account.json';data,status=refresh('burncode',path,fetcher=lambda _:Fake())
   self.assertEqual(status,'updated');self.assertEqual(load(path,'burncode')['followers'],8)
   data,status=refresh('burncode',path,force=True,fetcher=lambda _:(_ for _ in ()).throw(OSError('offline')))
   self.assertEqual(status,'stale');self.assertEqual(data['followers'],8)
 def test_bad_social_display(self):
  cfg=copy.deepcopy(build.read_json(ROOT/'config.json'));cfg['social'][0]['display']='huge'
  with self.assertRaises(build.ConfigError):build.validate(cfg,ROOT/'config.json')
if __name__=='__main__':unittest.main()
