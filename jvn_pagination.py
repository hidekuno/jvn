#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#

import os
from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key

PAGE_COUNT = 10


class JvnPage(object):
    """ページ処理"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.page = 0
        self.total_count = 0
        self.total_page = 0
        self.is_display_prev = False
        self.is_display_next = False

    def set_count(self, count):
        self.total_count = count
        self.total_page = int(count / PAGE_COUNT)
        if (count % PAGE_COUNT) != 0:
            self.total_page += 1

    def set_next_page(self):
        self.page = self.page + 1

    def set_prev_page(self):
        self.page = self.page - 1

    def set_control_page_button(self, result):
        if self.page == 0:
            self.is_display_prev = False
        else:
            self.is_display_prev = True

        if self.total_count > (self.page * PAGE_COUNT + len(result)):
            self.is_display_next = True
        else:
            self.is_display_next = False


class SearchModule(object):
    """検索表示"""

    def initialize(self):
        pass

    def make_ui(self, req, session):
        pass

    def core_proc(self, req, session, func):
        """スケルトンロジック"""
        # インスタンス変数の初期化
        self.pager_app = get_session_key(req)
        self.result = ()
        self.error_message = ""

        # sessionとrequestのマージ処理
        self.make_ui(req, session)

        # 変数の初期化
        self.initialize()

        # indexの場合は処理を行わない
        if os.path.basename(req.path_qs) == "index" and not self.is_init_page():
            return

        # 最初のアクションの場合はトータル件数をセットする。
        if self.is_init_page():
            self.ui.set_count(self.dao.get_count())

        # 検索結果がゼロの場合
        if self.ui.total_count == 0:
            self.error_message = "該当するレコードが存在しません。検索条件をチェックしてください。"
            self.ui.reset()
            return

        # 検索結果が上限値を超えた場合
        if self.ui.total_count > self.MAX_TOTAL_COUNT:
            self.error_message = "検索結果が上限値(%d)を超えました。検索条件をチェックしてください。" % (
                self.MAX_TOTAL_COUNT
            )
            self.ui.total_count = 0
            return

        func()

        self.result = self.dao.get_records(self.ui.page)
        self.ui.set_control_page_button(self.result)


class Index(JvnApplication):
    """初期表示処理"""

    def is_token_valid(self, req, session):
        return True

    def is_init_page(self):
        return True

    def do_logic(self, req, res, session):
        self.core_proc(req, session, lambda: None)


class Search(JvnApplication):
    """検索処理"""

    def is_init_page(self):
        return True

    def do_logic(self, req, res, session):
        self.core_proc(req, session, lambda: None)


class Next(JvnApplication):
    """次ページ遷移"""

    def is_init_page(self):
        return False

    def do_logic(self, req, res, session):
        self.core_proc(req, session, lambda: self.ui.set_next_page())


class Prev(JvnApplication):
    """前ページ遷移"""

    def is_init_page(self):
        return False

    def do_logic(self, req, res, session):
        self.core_proc(req, session, lambda: self.ui.set_prev_page())


class Back(JvnApplication):
    """戻る（画面遷移処理)"""

    def is_init_page(self):
        return False

    def do_logic(self, req, res, session):
        self.core_proc(req, session, lambda: None)


class Maintenance(JvnApplication):
    """メンテナンスボタン表示処理 (保守用)"""

    def app_name(self):
        pass

    def dao(self):
        pass

    def do_logic(self, req, res, session):
        self.jinja_html_file = "jvn_develop.j2"

        dao = self.dao()
        app_name = self.app_name()
        self.result = dao.get_maintenance_records(session.get(app_name))
        self.backlink = app_name
