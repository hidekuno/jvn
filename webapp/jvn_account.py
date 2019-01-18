#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
import os
import hashlib
from wsgi_handler import JvnApplication
from wsgi_handler import get_session_key
from wsgi_handler import hash_passwd

from jvn_model import Account
from jvn_model import do_transaction
################################################################################
# セッションデータ
################################################################################
class JvnState(object):
    def __init__(self):
        self.passwd     = ''

################################################################################
# 初期表示処理
################################################################################
class Index(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_account.html'
        self.result = do_transaction(lambda db : db.query(Account).all(),self)

################################################################################
# 新規登録処理
################################################################################
class Regist(JvnApplication):
    def do_logic(self, req, res, session):

        session[ get_session_key(req) ] = JvnState()

        self.jinja_html_file = 'jvn_account_edit.html'
        self.ui = Account({'user_id'     : ''
                           ,'passwd'     : ''
                           ,'user_name'  : ''
                           ,'email'      : ''
                           ,'department' : ''
                           ,'privs'      : ''}
                          ,'')

        self.readonly = ''
        self.method = 'regist'

        self.admin = 'checked'
        self.user  = ''
################################################################################
# 変更処理
################################################################################
class Modify(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_account_edit.html'

        self.ui = do_transaction(lambda db : db.query(Account).filter_by(user_id=req.params['user_id']).first(),self)

        state = JvnState()
        state.passwd = self.ui.passwd
        session[ get_session_key(req) ] = state

        self.readonly = 'readonly'
        self.method = 'modify'
        if self.ui.privs == 'admin':
            self.admin = 'checked'
            self.user  = ''
        else:
            self.admin = ''
            self.user  = 'checked'

################################################################################
# 更新処理
################################################################################
class Execute(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_account.html'

        #リクエストのパスワードとセッション情報のそれが同一の場合は変更しない。
        jvn = session.get(get_session_key(req))
        if req.params['passwd'] == jvn.passwd:
            hash_code = jvn.passwd
        else:
            hash_code = hash_passwd(req.params['passwd'])

        def do_execute(db):
            if req.params['method'] == 'regist':
                rec = Account(req.params, hash_code)
                db.add(rec)

            elif req.params['method'] == 'modify':
                rec = db.query(Account).filter_by(user_id=req.params['user_id']).first()
                rec.passwd      = hash_code
                rec.user_name   = req.params['user_name']
                rec.email       = req.params['email']
                rec.department  = req.params['department']
                rec.privs       = req.params['privs']

            return db.query(Account).all()

        self.result = do_transaction(do_execute,self)
################################################################################
# 削除処理
################################################################################
class Delete(JvnApplication):

    def is_token_valid(self, req, session):
        return True

    def do_logic(self, req, res, session):
        self.jinja_html_file = 'jvn_account.html'

        def do_execute(db):
            rec = db.query(Account).filter_by(user_id=req.params['delete_user_id']).first()
            db.delete(rec)
            return db.query(Account).all()

        self.result = do_transaction(do_execute,self)
