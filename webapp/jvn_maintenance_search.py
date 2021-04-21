#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
import jvn_pagination
from jvn_pagination import PAGE_COUNT
from jvn_pagination import JvnPage

class JvnDAO(object):
    """Data Access Object
    """
    def __init__(self, app):
        self.app = app

    def get_count(self):
        sql_count = """select count(distinct c.cpe)
                       from  jvn_vulnerability a,    jvn_vulnerability_detail b,jvn_product c,jvn_vendor d
                       where b.cpe =  c.cpe
                       and   fs_manage = 'undefine'
                       and   b.identifier = a.identifier
                       and   c.vid        = d.vid"""

        self.app.cursor.execute(sql_count)
        count = self.app.cursor.fetchone()
        return count[0]

    def get_records(self,offset):
        sqlfmt = """select row_number() over(order by c.vid, c.pid) as no, d.vname, c.pname,c.cpe
                    from  jvn_vulnerability a,jvn_vulnerability_detail b, jvn_product c,   jvn_vendor d
                    where b.cpe =  c.cpe
                    and   fs_manage = 'undefine'
                    and   b.identifier = a.identifier
                    and   c.vid        = d.vid
                    group by c.vid, c.pid, d.vname, c.pname, c.cpe, c.fs_manage
                    order by c.vid, c.pid limit %s OFFSET %s"""

        self.app.cursor.execute(sqlfmt,(PAGE_COUNT
                                        ,offset * PAGE_COUNT,))
        rows = self.app.cursor.fetchall()
        return rows

    def get_maintenance_records(self, jvn_state):
        sqlfmt = """select row_number() over(order by c.vid, c.pid) as no, d.vname, c.pname, c.cpe, c.fs_manage
                    from  jvn_vulnerability a,jvn_vulnerability_detail b, jvn_product c,   jvn_vendor d
                    where b.cpe =  c.cpe
                    and   fs_manage = 'undefine'
                    and   b.identifier = a.identifier
                    and   c.vid        = d.vid
                    group by c.vid, c.pid, d.vname, c.pname, c.cpe, c.fs_manage
                    order by c.vid, c.pid"""

        self.app.cursor.execute(sqlfmt)
        rows = self.app.cursor.fetchall()
        return rows

class JvnState(JvnPage): 
    """session data object
    """
    pass

class TitleListLogic(jvn_pagination.SearchModule):
    """タイトル製品検索
    """
    def initialize(self):
        # インスタンス変数の初期化
        self.jinja_html_file = 'jvn_maintenance_search.j2'
        self.MAX_TOTAL_COUNT = 1000
        self.dao = JvnDAO(self)

    def make_ui(self, req, session):
        self.ui = session.get(self.pager_app)
        if (self.ui is None):
            self.ui = session[self.pager_app] = JvnState()

################################################################################
#  初期表示処理,次ページ処理,前ページ処理,戻るページ遷移
################################################################################
class Index(jvn_pagination.Index,TitleListLogic):pass
class Search(jvn_pagination.Search,TitleListLogic): pass
class Next(jvn_pagination.Next,TitleListLogic): pass
class Prev(jvn_pagination.Prev,TitleListLogic): pass
class Back(jvn_pagination.Back,TitleListLogic): pass

class Maintenance(jvn_pagination.Maintenance):
    """メンテナンスボタン表示処理 (保守G使用)
    """
    def app_name(self):
        return 'jvn_maintenance_search'

    def dao(self):
        return JvnDAO(self)
