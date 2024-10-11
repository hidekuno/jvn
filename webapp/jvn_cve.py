#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key


class JvnDAO(object):
    """Data Access Object"""

    def __init__(self, app):
        self.app = app

    def get_records(self, cveid):
        sqlfmt = """select
                    b.identifier, b.title, b.link, b.modified_date, b.issued_date
                    from jvn_cve a, jvn_vulnerability b
                    where a.identifier = b.identifier
                    and a.cveid = %s;"""
        self.app.cursor.execute(sqlfmt, (cveid,))
        rows = self.app.cursor.fetchall()
        return rows


class JvnState(object):
    """session data object"""

    def __init__(self):
        pass


class Index(JvnApplication):
    """初期表示処理"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.cveid = req.params["cveid"]
        self.ui = session[get_session_key(req)] = JvnState()
        self.jinja_html_file = "jvn_cve.j2"
        dao = JvnDAO(self)
        self.result = dao.get_records(self.cveid)
