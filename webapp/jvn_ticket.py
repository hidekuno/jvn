#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
import datetime

from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key
from wsgi_handler import fs_manage_code2ui
from jvn_model import Vulnerability
from jvn_model import do_transaction
################################################################################
# DAO(データアクセスオブジェクト)
################################################################################
class JvnDAO(object):

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

################################################################################
# セッションデータ
################################################################################
class JvnState(object):
    def __init__(self, total_count):
        self.total_count = total_count

################################################################################
# 初期表示
################################################################################
class Index(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_ticket.j2'
        self.identifier = req.params['identifier']

        ui = session[get_session_key(req)] = JvnState(0)
        dao = JvnDAO(self)
        self.result = [ x[0:4] + (fs_manage_code2ui(x[4]),) for x in dao.get_all_records() ]
        ui.total_count = len(self.result)

################################################################################
# 依頼ボタン処理
################################################################################
class Execute(JvnApplication):

    def do_logic(self, req, res, session):

        self.jinja_html_file = 'jvn_ticket_complete.j2'
        self.identifier = req.params['identifier']
        ui = session.get(get_session_key(req))

        def do_execute(db):
            rec = db.query(Vulnerability).filter_by(identifier = self.identifier).first()
            rec.ticket_modified_date = datetime.datetime.now()

        do_transaction(do_execute,self)

        records = []
        for i in range(0, ui.total_count):
            records.append((req.params["vname" + str(i+1)]
                           ,req.params["pname" + str(i+1)]
                           ,req.params["cpe"   + str(i+1)]))

        self.result = records
