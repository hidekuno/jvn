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
################################################################################
# DAO(データアクセスオブジェクト)
################################################################################
class JvnDAO(object):

    def __init__(self, app):
        self.app = app

    def get_edit_records(self):

        sqlfmt = """select row_number() over(order by b.vid,b.pid) as no, a.vname, b.pname, b.cpe, b.fs_manage
                    from jvn_vendor a, jvn_product b
                    where (a.vid = b.vid) 
                    and   (b.edit = 1)
                    order by b.vid, b.pid"""

        self.app.cursor.execute(sqlfmt)
        rows = self.app.cursor.fetchall()
        return rows

################################################################################
# セッションデータ
################################################################################
class JvnState(object):
    def __init__(self, total_count):
        self.total_count = total_count

################################################################################
# 依頼チェック表示処理 (保守G使用)
################################################################################
class Index(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_develop.html'
        ui = session[get_session_key(req)] = JvnState(0)

        dao = JvnDAO(self)
        self.result = dao.get_edit_records()
        ui.total_count = len(self.result)

        # 戻るボタンを非表示にする
        self.backlink = None

################################################################################
# チェック処理 (保守G使用)
################################################################################
class Update(JvnApplication):

    def do_logic(self, req, res, session):

        self.jinja_html_file = 'jvn_develop_complete.html'

        def do_execute(db):
            records = []

            i = 0
            while True:
                vendor    = "vendor"    + str(i+1)
                product   = "product"   + str(i+1)
                cpe       = "cpe"       + str(i+1)
                fs_manage = "fs_manage" + str(i+1)
                if not cpe in req.params: break

                rec = db.query(Product).filter_by(cpe = req.params[cpe]).first()
                rec.edit = 0
                rec.fs_manage = req.params[fs_manage]

                records.append((fs_manage_code2ui(req.params[fs_manage])
                                ,req.params[vendor]
                                ,req.params[product]
                                ,req.params[cpe]))
                i += 1
            return records
        self.result = do_transaction(do_execute,self)
