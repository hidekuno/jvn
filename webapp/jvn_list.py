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
################################################################################
# DAO(データアクセスオブジェクト)
################################################################################
class JvnDAO(object):

    def __init__(self, app):

        self.app = app
        if app.ui.dp_from == '':
            self.dp_from  = ''
            self.dp_to    = ''
        else: 
            self.dp_from  = app.ui.dp_from
            self.dp_to    = app.ui.dp_to

    def get_count(self):
        sql_count = """select count(*) from jvn_vulnerability a
                       where exists (select 1 from jvn_vulnerability_detail b, jvn_product c
                                     where a.identifier = b.identifier and b.cpe = c.cpe)"""
        if self.dp_from == '' :
            self.app.cursor.execute(sql_count)
        else: 
            sql_count = sql_count + """ and %s <= modified_date and modified_date <= %s;"""
            self.app.cursor.execute(sql_count, (self.dp_from, self.dp_to))

        count = self.app.cursor.fetchone()
        return count[0]

    # place holderで使うtupleに癖がある。
    def get_records(self,offset):
        sql_main = """select
                    identifier, max(title) as title, max(link) as link, modified_date, issued_date, max(fs_manage) as fs_manage
                    from
                    (
                      select   a.identifier, title, link, modified_date, issued_date,
                             (case when modified_date < ticket_modified_date then 4
                                   when fs_manage='not_cover_item'           then 0
                                   when fs_manage='cover_item'               then 1
                                   when fs_manage='undefine' and edit=0      then 2
                                   else                                           3
                              end) as fs_manage
                      from     jvn_vulnerability a, jvn_vulnerability_detail b, jvn_product c
                      where    a.identifier = b.identifier
                      and      b.cpe = c.cpe) as mail_query"""
 
        sql_where = """where %s <= modified_date and modified_date <= %s"""

        sql_gr = """group by identifier, modified_date, issued_date
                    order by modified_date desc limit %s OFFSET %s;"""

        if self.dp_from == '' :
            self.app.cursor.execute(sql_main + ' ' + sql_gr, (PAGE_COUNT, offset * PAGE_COUNT,))
        else:
            self.app.cursor.execute(sql_main 
                                    + ' ' + sql_where 
                                    + ' ' + sql_gr, (self.dp_from, self.dp_to, PAGE_COUNT, offset * PAGE_COUNT,))

        rows = self.app.cursor.fetchall()
        return rows
################################################################################
# セッションデータ
################################################################################
class JvnState(JvnPage):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.dp_from     = ''
        self.dp_to       = ''

################################################################################
# 検索表示
################################################################################
class ListLogic(jvn_pagination.SearchModule):

    ################################################################################
    # 変数の初期化
    ################################################################################
    def initialize(self):
        # インスタンス変数の初期化
        self.jinja_html_file = 'jvn_list.html'
        self.dao = JvnDAO(self)
        self.MAX_TOTAL_COUNT = 10000000

    ################################################################################
    # UIオブジェクトの作成
    ################################################################################
    def make_ui(self, req, session):

        self.ui = session.get(self.pager_app)
        if (self.ui is None) or ('dp_from' in req.params) or (os.path.basename(req.path_qs) == 'index'):
            self.ui = session[self.pager_app] = JvnState()

        if 'dp_from' in req.params:
            self.ui.dp_from = req.params['dp_from']
            self.ui.dp_to   = req.params['dp_to']

################################################################################
# 初期表示処理,次ページ処理,前ページ処理,戻るページ遷移
################################################################################
class Index(jvn_pagination.Index,ListLogic): pass
class Search(jvn_pagination.Search,ListLogic): pass
class Next(jvn_pagination.Next,ListLogic): pass
class Prev(jvn_pagination.Prev,ListLogic): pass
class Back(jvn_pagination.Back,ListLogic): pass
