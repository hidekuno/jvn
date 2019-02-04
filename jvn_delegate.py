#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from wsgi_handler import get_session_key
class JvnState(object):
    def __init__(self):
        pass
################################################################################
# ページ処理
################################################################################
class JvnDelegate(object):
    def do_chart(self, uri, req, session):
        self.title_name = 'JVN 脆弱性発生件数'
        url = req.host_url

        idx = url.rfind(':' + req.host_port)
        if idx == -1:
            p = url[0:url.find(':')]
            self.image_url = p + '://localhost' + ':' + self.config.get('plt','port') + '/' + uri
        else:
            self.image_url = url[0:idx] + ':' + self.config.get('plt','port') + '/' + uri

        self.ui = session[get_session_key(req)] = JvnState()
        self.jinja_html_file = 'jvn_chart.tpl'
