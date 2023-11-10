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


class JvnDAO(object):
    """Data Access Object"""

    def __init__(self, app):
        self.app = app

    def get_fs_manage(self):
        if self.app.cover_item == "checked":
            return "cover_item"

        if self.app.not_cover_item == "checked":
            return "not_cover_item"

        if self.app.undefine == "checked":
            return "undefine"

    def get_count(self):
        sql_count = """select count(*) as c from jvn_vendor a, jvn_product b
                      where (a.vid = b.vid ) and (vname ilike %s) and (pname ilike %s) and (b.fs_manage = %s)"""
        self.app.cursor.execute(
            sql_count,
            (
                make_like(self.app.ui.vendor),
                make_like(self.app.ui.product),
                self.get_fs_manage(),
            ),
        )
        count = self.app.cursor.fetchone()
        return count[0]

    def get_records(self, offset):
        sqlfmt = """select row_number() over(order by b.vid,b.pid) as no, a.vname, b.pname, b.cpe
                    from jvn_vendor a, jvn_product b
                    where (a.vid = b.vid ) and (vname ilike %s) and (pname ilike %s) and (b.fs_manage = %s)
                    order by b.vid, b.pid limit %s OFFSET %s"""

        self.app.cursor.execute(
            sqlfmt,
            (
                make_like(self.app.ui.vendor),
                make_like(self.app.ui.product),
                self.get_fs_manage(),
                PAGE_COUNT,
                offset * PAGE_COUNT,
            ),
        )
        rows = self.app.cursor.fetchall()
        return rows

    def get_maintenance_records(self, jvn_state):
        sqlfmt = """select row_number() over(order by b.vid,b.pid) as no, a.vname, b.pname, b.cpe, b.fs_manage
                    from jvn_vendor a, jvn_product b
                    where (a.vid = b.vid )
                    and (vname ilike %s) and (pname ilike %s) and (b.fs_manage = %s)"""

        self.app.cursor.execute(
            sqlfmt,
            (
                make_like(jvn_state.vendor),
                make_like(jvn_state.product),
                jvn_state.fs_manage,
            ),
        )

        rows = self.app.cursor.fetchall()
        return rows


class JvnState(JvnPage):
    """session data object"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.vendor = ""
        self.product = ""
        self.fs_manage = "undefine"


class ProductListLogic(jvn_pagination.SearchModule):
    """製品検索"""

    def initialize(self):
        # インスタンス変数の初期化
        self.jinja_html_file = "jvn_search.j2"
        self.MAX_TOTAL_COUNT = 1000
        self.dao = JvnDAO(self)

    def make_ui(self, req, session):
        # sessionとrequestのマージ処理
        self.ui = session.get(self.pager_app)
        if (self.ui is None) or ("vendor" in req.params) or (os.path.basename(req.path_qs) == "index"):
            self.ui = session[self.pager_app] = JvnState()

        # Requestデータを優先して処理する
        if "fs_manage" in req.params:
            self.ui.vendor = req.params["vendor"]
            self.ui.product = req.params["product"]
            self.ui.fs_manage = req.params["fs_manage"]

            # ラジオボタン制御
        if self.ui.fs_manage == "cover_item":
            self.cover_item = "checked"
            self.not_cover_item = self.undefine = ""

        elif self.ui.fs_manage == "not_cover_item":
            self.not_cover_item = "checked"
            self.cover_item = self.undefine = ""

        elif self.ui.fs_manage == "undefine":
            self.undefine = "checked"
            self.not_cover_item = self.cover_item = ""


################################################################################
#  初期表示処理,次ページ処理,前ページ処理,戻るページ遷移
################################################################################
class Index(jvn_pagination.Index, ProductListLogic):
    def is_init_page(self):
        return False


class Search(jvn_pagination.Search, ProductListLogic):
    pass


class Next(jvn_pagination.Next, ProductListLogic):
    pass


class Prev(jvn_pagination.Prev, ProductListLogic):
    pass


class Back(jvn_pagination.Back, ProductListLogic):
    pass


class Maintenance(jvn_pagination.Maintenance):
    """メンテナンスボタン表示処理 (保守G使用)"""

    def app_name(self):
        return "jvn_search"

    def dao(self):
        return JvnDAO(self)
