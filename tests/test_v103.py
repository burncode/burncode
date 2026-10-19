# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""v10.3 regression suite: repository discovery, locale, GraphQL and no-fake activity."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import build
from profilegen.providers.github import infer_repository
from profilegen.providers.contributions import refresh_contributions, load_contributions

class Response:
    def __init__(self,data):self.data=json.dumps(data).encode()
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return self.data

class Version103Tests(unittest.TestCase):
    def test_repo_url_discovery(self):
        self.assertEqual(infer_repository('https://github.com/acme/widget'), 'acme/widget')
        self.assertEqual(infer_repository('https://github.com/acme/widget/'), 'acme/widget')
        self.assertIsNone(infer_repository('https://github.com/acme/widget/issues'))
        self.assertIsNone(infer_repository('https://github.com/acme'))
        self.assertIsNone(infer_repository('https://evil.example/acme/widget'))
    def test_validate_auto_repo_and_locales(self):
        source=build.read_json(build.ROOT/'config.json')
        source['projects'][0]['url']='https://github.com/acme/widget'
        for locale in ('en','zh-CN','ja','es'):
            source['i18n']['locale']=locale
            validated=build.validate(source,build.ROOT/'config.json')
            self.assertEqual(validated['projects'][0]['repository'],'acme/widget')
    def test_contribution_cache_success(self):
        calendar={'data':{'user':{'contributionsCollection':{'contributionCalendar':{'totalContributions':8,'weeks':[{'contributionDays':[{'date':'2026-10-01','contributionCount':8,'contributionLevel':'FOURTH_QUARTILE'}]}]}}}}}
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'contributions.json'
            result,status=refresh_contributions('burncode',path,token='fake',fetcher=lambda req:Response(calendar),now=123)
            self.assertEqual(status,'updated')
            self.assertEqual(result['days'][0]['level'],4)
            self.assertEqual(load_contributions(path,'burncode')['total'],8)
            self.assertIsNone(load_contributions(path,'someone-else'))
    def test_no_token_does_not_create_fake_data(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'contributions.json'
            with patch.dict('os.environ',{'GH_TOKEN':'','GITHUB_TOKEN':''}):
                result,status=refresh_contributions('burncode',path)
            self.assertIsNone(result)
            self.assertFalse(path.exists())
            self.assertIn('token-required',status)
    def test_status_cli(self):
        with redirect_stdout(io.StringIO()) as output:
            result=build.main(['--github-status'])
        self.assertEqual(result,0)
        data=json.loads(output.getvalue())
        self.assertIn('cache_exists',data)
        self.assertIn('repositories',data)
    def test_activity_never_fabricates(self):
        cfg=build.validate(build.read_json(build.ROOT/'config.json'),build.ROOT/'config.json')
        svg=build.render(cfg,'mono')
        self.assertIn('暂无已验证的 GitHub 贡献数据',svg)
        self.assertNotIn('Decorative pattern',svg)

if __name__=='__main__':unittest.main()
