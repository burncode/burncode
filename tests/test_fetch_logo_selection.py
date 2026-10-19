# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
import unittest
from profilegen.widgets.fastfetch import available_logos, _logo_lines

class TestFetchLogoSelection(unittest.TestCase):
    def test_all_templates_discovered(self):
        self.assertIn('arch', available_logos())
        self.assertIn('nixos', available_logos())
        self.assertIn('windows11', available_logos())
    def test_exact_selection(self):
        self.assertNotEqual(_logo_lines('arch'), _logo_lines('windows11'))
        self.assertNotEqual(_logo_lines('nixos'), _logo_lines('arch'))
    def test_unknown_not_silently_fallback(self):
        with self.assertRaises(ValueError):
            _logo_lines('nonexistent-os')
    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            _logo_lines('../arch')
