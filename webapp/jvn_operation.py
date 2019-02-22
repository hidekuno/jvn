#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from jvn_model import Product
from jvn_model import do_transaction

from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key
from wsgi_handler import fs_manage_code2ui

class JvnDAO(object):
    """Data Access Object
    """
    def __init__(self, app):
        self.app = app

    def get_all_records(self):

        sqlfmt = """select row_number() over(order by b.vid,b.pid) as no, a.vname, b.pname, b.cpe, fs_manage
                    from  jvn_vendor a, jvn_product b, jvn_vulnerability_detail c
                    where (a.vid = b.vid) 
                    and   (b.cpe = c.cpe)
                    and   (c.identifier = %s)
                    order by b.vid, b.pid"""

        self.app.cursor.execute(sqlfmt,(self.app.identifier,))

        rows = self.app.cursor.fetchall()
        return rows

class JvnState(object):
    """session data object
    """
    def __init__(self, total_count):
        self.total_count = total_count

class Index(JvnApplication):
    """初期表示
    """
    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_operation.j2'
        self.identifier = req.params['identifier']

        ui = session[get_session_key(req)] = JvnState(0)

        dao = JvnDAO(self)
        self.result = [ x[0:4] + (fs_manage_code2ui(x[4]),) for x in dao.get_all_records() ]
        ui.total_count = len(self.result)

class Execute(JvnApplication):
    """依頼ボタン処理
    """
    def do_logic(self, req, res, session):

        self.jinja_html_file = 'jvn_operation_complete.j2'
        ui = session.get(get_session_key(req))

        def do_execute(db):

            records = []
            for i in range(0, ui.total_count):
                checkbox = "check" + str(i+1)

                if checkbox in req.params:

                    rec = db.query(Product).filter_by(cpe = req.params[checkbox]).first()
                    rec.edit = 1
                    records.append((req.params["vname" + str(i+1)],
                                    req.params["pname" + str(i+1)],
                                    req.params[checkbox]))
            return records

        self.result = do_transaction(do_execute,self)
