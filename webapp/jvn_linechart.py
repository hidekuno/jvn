#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from wsgi_handler import JvnApplication
from jvn_delegate import JvnDelegate
################################################################################
# グラフ表示
################################################################################
class Index(JvnApplication,JvnDelegate):
    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.do_chart('linechart',req, session)
