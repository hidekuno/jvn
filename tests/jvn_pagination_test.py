#!/usr/bin/python
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
# Test howto
# 1) python tests/cidr_search_test.py
# 2) cd tests; python -m unittest cidr_search_test
# 3) PYTHONPATH=$HOME/jvn python tests/cidr_search_test.py
#
import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from jvn_pagination import JvnPage
from jvn_pagination import SearchModule
from jvn_pagination import Index
from jvn_pagination import Search
from jvn_pagination import Next
from jvn_pagination import Prev
from jvn_pagination import Back
from jvn_pagination import Maintenance
from wsgi_handler import JvnApplication

class JvnTest(JvnApplication):
    def __init__(self):
        super(JvnTest, self).__init__()

class TestMethods(unittest.TestCase):

    def test_pagination_01(self):
        p = JvnPage()
        self.assertEqual(p.page, 0)
        self.assertEqual(p.total_count, 0)
        self.assertEqual(p.total_page,  0)
        self.assertEqual(p.is_display_prev,  False)
        self.assertEqual(p.is_display_next,  False)

    def test_pagination_set_count(self):
        p = JvnPage()
        p.set_count(100)
        self.assertEqual(p.page, 0)
        self.assertEqual(p.total_count, 100)
        self.assertEqual(p.total_page,  10)

    def test_pagination_set_next_page(self):
        p = JvnPage()
        p.set_count(100)
        p.set_next_page()
        self.assertEqual(p.page, 1)

    def test_pagination_set_prev_page(self):
        p = JvnPage()
        p.set_count(100)
        p.set_next_page()
        p.set_next_page()
        p.set_prev_page()
        self.assertEqual(p.page, 1)

    def test_control_page_button_prev(self):
        p = JvnPage()
        self.assertEqual(p.is_display_prev, False)
        p.set_count(100)

        p.set_next_page()
        p.set_control_page_button(["a"]*100)
        self.assertEqual(p.is_display_prev, True)

        p.set_prev_page()
        p.set_control_page_button(["a"]*100)
        self.assertEqual(p.is_display_prev, False)

    def test_control_page_button_next(self):
        p = JvnPage()
        self.assertEqual(p.is_display_next, False)
        p.set_count(100)
        p.set_control_page_button(["a"]*10)
        self.assertEqual(p.is_display_next, True)

    def test_search_module(self):
        se = SearchModule()

if __name__ == '__main__':
    unittest.main()
