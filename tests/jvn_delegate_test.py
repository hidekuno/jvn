#!/usr/bin/env python
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

from jvn_delegate import JvnState
from jvn_delegate import JvnDelegate
from wsgi_handler import JvnApplication

class RequestTest:
    def __init__(self):
        self.host_url = 'http://localhost:8888/vms/jvn/list'
        self.host_port = '8888'
        self.path_qs = '/vms/jvn/list'

    def case2(self):
        self.host_url = 'http://localhost/vms/jvn/list'
        self.host_port = '80'
        self.path_qs = '/vms/jvn/list'

class JvnTest(JvnDelegate,JvnApplication):
    def __init__(self):
        super(JvnTest, self).__init__()

class TestMethods(unittest.TestCase):
    def test_jvn_state(self):
        jvn = JvnState()
        s = str(type(jvn))
        self.assertEqual(s[s.rfind('.')+1:s.rfind("'>")], 'JvnState')

    def test_do_chart_01(self):
        t = JvnTest()
        req = RequestTest()
        session = {}
        t.do_chart("image", req, session)

        self.assertEqual(t.image_url, 'http://localhost:8003/image')

    def test_do_chart_02(self):
        t = JvnTest()
        req = RequestTest()
        req.case2()
        session = {}
        t.do_chart("image", req, session)
        self.assertEqual(t.image_url, 'http://localhost:8003/image')

if __name__ == '__main__':
    unittest.main()
