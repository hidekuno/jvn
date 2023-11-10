#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from wsgi_handler import JvnApplication
from jvn_delegate import JvnDelegate


class Index(JvnApplication, JvnDelegate):
    """グラフ表示(縦棒)"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.do_chart("barchart", req, session)
