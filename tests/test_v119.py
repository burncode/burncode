# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest
from profilegen.providers.feeds import parse
from profilegen.components.registry import COMPONENTS

class TestV119(unittest.TestCase):
    def test_atom_placeholder_domain(self):
        xml=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Post</title><link href="http://yoursite.com/2018/12/02/post/" /></entry></feed>'
        self.assertEqual(parse(xml,feed_url='https://burncode.github.io/atom.xml'),[{'title':'Post','url':'https://burncode.github.io/2018/12/02/post/'}])
    def test_atom_reject_unknown_insecure_domain(self):
        xml=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Post</title><link href="http://other.example.com/post" /></entry></feed>'
        self.assertEqual(parse(xml,feed_url='https://burncode.github.io/atom.xml'),[])
    def test_device_registered(self):
        self.assertIn('device',COMPONENTS)
