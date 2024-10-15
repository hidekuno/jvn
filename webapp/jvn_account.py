#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key
from wsgi_handler import make_passwd

from jvn_model import Account
from jvn_model import do_transaction


class JvnState(object):
    """session data object"""

    def __init__(self):
        self.passwd = ""


def setPrivs(app, privs):
    """権限情報編集"""
    if privs == "admin":
        app.admin = "checked"
        app.user = ""
    else:
        app.admin = ""
        app.user = "checked"


class Index(JvnApplication):
    """初期表示処理"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = "jvn_account.j2"
        self.result = do_transaction(
            lambda db: db.query(Account).order_by(Account.user_id).all(), self
        )


class Regist(JvnApplication):
    """新規登録処理"""

    def do_logic(self, req, res, session):
        session[get_session_key(req)] = JvnState()

        self.jinja_html_file = "jvn_account_edit.j2"
        self.ui = Account(
            {
                "user_id": "",
                "passwd": "",
                "user_name": "",
                "email": "",
                "department": "",
                "privs": "",
            },
            "",
        )

        self.readonly = ""
        self.method = "regist"
        setPrivs(self, "user")


class Modify(JvnApplication):
    """変更処理"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = "jvn_account_edit.j2"

        self.ui = do_transaction(
            lambda db: db.query(Account)
            .filter_by(user_id=req.params["user_id"])
            .first(),
            self,
        )

        state = JvnState()
        state.passwd = self.ui.passwd
        session[get_session_key(req)] = state

        self.readonly = "readonly"
        self.method = "modify"
        setPrivs(self, self.ui.privs)


class Execute(JvnApplication):
    """更新処理"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = "jvn_account.j2"
        self.method = req.params["method"]

        # リクエストのパスワードとセッション情報のそれが同一の場合は変更しない。
        jvn = session.get(get_session_key(req))
        if req.params["passwd"] == jvn.passwd:
            hash_code = jvn.passwd
        else:
            hash_code = make_passwd(req.params["passwd"])

        def do_execute(db):
            rec = Account(req.params, hash_code)
            ret, self.error_message = rec.validate(db, self.method)
            if not ret:
                self.jinja_html_file = "jvn_account_edit.j2"
                self.ui = rec
                setPrivs(self, rec.privs)
                return

            if self.method == "regist":
                db.add(rec)

            elif self.method == "modify":
                rec = db.query(Account).filter_by(user_id=req.params["user_id"]).first()
                rec.passwd = hash_code
                rec.user_name = req.params["user_name"]
                rec.email = req.params["email"]
                rec.department = req.params["department"]
                rec.privs = req.params["privs"]
            return db.query(Account).order_by(Account.user_id).all()

        self.result = do_transaction(do_execute, self)


class Delete(JvnApplication):
    """削除処理"""

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = "jvn_account.j2"

        def do_execute(db):
            rec = (
                db.query(Account)
                .filter_by(user_id=req.params["delete_user_id"])
                .first()
            )
            db.delete(rec)
            return db.query(Account).order_by(Account.user_id).all()

        self.result = do_transaction(do_execute, self)
