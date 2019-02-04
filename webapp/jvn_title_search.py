#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
import os
import jvn_pagination
from jvn_pagination import PAGE_COUNT
from jvn_pagination import JvnPage
from wsgi_handler import make_like
################################################################################
# DAO(データアクセスオブジェクト)
################################################################################
class JvnDAO(object):

    def __init__(self, app):
        self.app = app

    def get_count(self):
        sql_count = """select count(distinct c.cpe)
                       from jvn_vulnerability a,jvn_vulnerability_detail b,jvn_product c,jvn_vendor d
                       where a.title ilike %s and  a.identifier = b.identifier 
                       and   b.cpe = c.cpe and c.vid = d.vid"""

        self.app.cursor.execute(sql_count,(make_like(self.app.ui.keyword), ))
        count = self.app.cursor.fetchone()
        return count[0]

    def get_records(self,offset):
        sqlfmt = """select row_number() over(order by c.vid, c.pid) as no, d.vname, c.pname,c.cpe
                    from jvn_vulnerability a,jvn_vulnerability_detail b,jvn_product c,jvn_vendor d
                    where a.title ilike %s and  a.identifier = b.identifier 
                    and   b.cpe = c.cpe and c.vid = d.vid
                    group by c.vid, c.pid, d.vname, c.pname, c.cpe, c.fs_manage
                    order by c.vid, c.pid limit %s OFFSET %s"""

        self.app.cursor.execute(sqlfmt,(make_like(self.app.ui.keyword)
                                        ,PAGE_COUNT
                                        ,offset * PAGE_COUNT,))
        rows = self.app.cursor.fetchall()
        return rows

    def get_maintenance_records(self, jvn_state):
        sqlfmt = """select row_number() over(order by c.vid, c.pid) as no, d.vname, c.pname, c.cpe, c.fs_manage
                    from jvn_vulnerability a,jvn_vulnerability_detail b,jvn_product c,jvn_vendor d
                    where a.title ilike %s and  a.identifier = b.identifier 
                    and   b.cpe = c.cpe and c.vid = d.vid
                    group by c.vid, c.pid, d.vname, c.pname, c.cpe, c.fs_manage
                    order by c.vid, c.pid"""

        self.app.cursor.execute(sqlfmt,(make_like(jvn_state.keyword), ))
        rows = self.app.cursor.fetchall()
        return rows

################################################################################
# セッションデータ
################################################################################
class JvnState(JvnPage):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.keyword     = ''

################################################################################
# タイトル製品検索
################################################################################
class TitleListLogic(jvn_pagination.SearchModule):

    ################################################################################
    # 変数の初期化
    ################################################################################
    def initialize(self):
        # インスタンス変数の初期化
        self.jinja_html_file = 'jvn_title_search.tpl'
        self.MAX_TOTAL_COUNT = 1000
        self.dao = JvnDAO(self)

    ################################################################################
    # UIオブジェクトの作成
    ################################################################################
    def make_ui(self, req, session):
        # sessionとrequestのマージ処理
        self.ui = session.get(self.pager_app)
        if (self.ui is None) or ('keyword' in req.params) or (os.path.basename(req.path_qs) == 'index'):
            self.ui = session[self.pager_app] = JvnState()

        # Requestデータを優先して処理する
        if 'keyword' in req.params:
            self.ui.keyword    = req.params['keyword']

################################################################################
#  初期表示処理,次ページ処理,前ページ処理,戻るページ遷移
################################################################################
class Index(jvn_pagination.Index,TitleListLogic):
    def is_init_page(self):
        return False

class Search(jvn_pagination.Search,TitleListLogic): pass
class Next(jvn_pagination.Next,TitleListLogic): pass
class Prev(jvn_pagination.Prev,TitleListLogic): pass
class Back(jvn_pagination.Back,TitleListLogic): pass

################################################################################
# メンテナンスボタン表示処理 (保守G使用)
################################################################################
class Maintenance(jvn_pagination.Maintenance):
    def app_name(self):
        return 'jvn_title_search'

    def dao(self):
        return JvnDAO(self)
