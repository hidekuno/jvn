#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#

import os.path
import types
import glob
import sys
reload (sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True
import traceback
import logging
import logging.config
import ConfigParser

import psycopg2
from paste import urlmap
from paste.session import SessionMiddleware
from paste.session import make_session_middleware
from paste.request import get_cookies
import webob
from jinja2 import Environment, FileSystemLoader

import uuid
import hashlib
import poplib

TOKEN_KEY      = 'web_token'
LOGIN_USER_KEY = 'jvn_user'
SALT           = "JVN"
JVN_SID        = "JVN_SID"

################################################################################
# アプリケーション骨格処理
################################################################################
class JvnApplication(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        jvn_path = os.path.abspath(os.path.dirname(__file__))

        self.config.read(os.path.join(jvn_path, 'jvn.conf'))
        self.topuri          = "/vms"
        self.error_message   = ''
        self.exception       = None
    ################################################################################
    # Set Transaction Token
    ################################################################################
    def save_token(self,session):
        self.web_token = session[TOKEN_KEY] = hashlib.md5( str(uuid.uuid4()) ).hexdigest()

    ################################################################################
    # Check Transaction Token
    ################################################################################
    def is_token_valid(self, req, session):
        if TOKEN_KEY not in req.params:
            return False

        if TOKEN_KEY not in session:
            raise Exception("セッションファイルが削除された可能性があります。")

        return (req.params[TOKEN_KEY] == session[TOKEN_KEY])
    ################################################################################
    # Check login
    ################################################################################
    def check_login(self, req, session):
        login_ok = False

        if LOGIN_USER_KEY in req.params:

            sql_stmt = """select user_id, user_name, email, department, privs from jvn_account 
                          where user_id = %s and passwd = %s"""
            self.cursor.execute(sql_stmt, (req.params[LOGIN_USER_KEY], hash_passwd(req.params['jvn_passwd'])))
            rows = self.cursor.fetchall()

            if (len(rows) > 0):
                self.login_user = session[LOGIN_USER_KEY] = JvnUser(rows[0])
                login_ok = True

            elif True == auth_pop_user(req.params[LOGIN_USER_KEY],req.params['jvn_passwd']):
                self.login_user = session[LOGIN_USER_KEY] = JvnUser((req.params[LOGIN_USER_KEY],))
                login_ok = True

            else:
                self.error_message   = 'アカウントIDもしくはパスワードが違います。'
        else:
            # セッション情報にユーザーIDがある場合は認証済みとする。
            if LOGIN_USER_KEY in session :
                self.login_user = session.get(LOGIN_USER_KEY)
                login_ok = True

        return login_ok

    ################################################################################
    # コントロールロジック(後でエラーハンドルを書く try catchでrollbackとか)
    ################################################################################
    def __call__(self, environ, start_response):

        session = environ['paste.session.factory']()
        req = webob.Request(environ)
        res = webob.Response()
        connection = None
        logging.info(req)
        logging.info(session)

        try:
            connection = psycopg2.connect(database =self.config.get('db','database')
                                          ,user    =self.config.get('db','user')
                                          ,password=self.config.get('db','password')
                                          ,host    =self.config.get('db','host')
                                          ,port    =self.config.get('db','port'))

            self.cursor = connection.cursor()

            # 認証チェックを行う。失敗した場合はログイン画面を表示する。
            if (True == self.check_login(req,session)):
                if False == self.is_token_valid(req, session): raise Exception("不正操作です。")
                self.save_token(session)
                self.do_logic(req,res,session)
            else:
                self.jinja_html_file = "login.j2"

            self.cursor.close()
            connection.commit()

        except Exception as e:
            self.jinja_html_file = 'jvn_error.j2'
            self.exception = str(e)
            self.trace     = traceback.format_exc()

            logging.error(self.exception)
            logging.error(self.trace)
            if connection is not None:
                connection.rollback()

        finally:
            if connection is not None:
                connection.close()

        env = Environment(loader=FileSystemLoader('/var/www/jvn', encoding='utf8'),
                          autoescape=True)

        tmpl = env.get_template(os.path.join('template', self.jinja_html_file))
        view = tmpl.render(app=self).encode("utf-8")

        res.status_code           = 200
        res.content_type          = 'text/html'
        res.charset               = 'utf8'
        res.cache_expires(60)
        res.content_language      = ['ja']
        res.server                = 'Shindoi Joke/1.0'
        res.body                  = view
        res.content_length        = str(len(res.body))

        return res(environ,start_response)
################################################################################
# ユーザー情報
################################################################################
class JvnUser(object):

    def __init__(self,rows):
        if len(rows) == 1:
            self.user_id    = rows[0]
            self.user_name  = 'ゲスト'
            self.email      = ''
            self.department = ''
            self.privs      = 'user'
        else:
            self.user_id    = rows[0]
            self.user_name  = rows[1]
            self.email      = rows[2]
            self.department = rows[3]
            self.privs      = rows[4]
################################################################################
# ユーザー認証処理
################################################################################
def auth_pop_user(user, passwd):

    auth = True

    s = poplib.POP3('mail.mukogawa.or.jp')
    s.user(user)
    try:
        s.pass_(passwd)
    except Exception as e:
        auth = False
    s.quit()

    return auth
################################################################################
# パスワードをハッシュ化する
################################################################################
def hash_passwd(passwd):
    return hashlib.md5(SALT + passwd).hexdigest()

################################################################################
# セッションキーを取得する
################################################################################
def get_session_key(req):
    key = os.path.basename(os.path.dirname(req.path_qs))
    return key

################################################################################
# 製品の取り扱いコードをUI表示用に変換する
################################################################################
def fs_manage_code2ui(code):

    display_fs_manage = '未定義'

    if code == 'not_cover_item':
        display_fs_manage = '対象外'

    elif code == 'cover_item':
        display_fs_manage = '対象'

    return display_fs_manage

################################################################################
# SQLのLike検索を付加した文字列を取得
################################################################################
def make_like(word):
    return word.replace(' ', '%') + '%'

################################################################################
# ログアウト処理
################################################################################
def logout(environ, start_response):

    class UnknownApp(JvnApplication):
        def __init__(self):
            super(self.__class__, self).__init__()

    cookie = get_cookies(environ)
    if JVN_SID in cookie:
        sid = cookie.get(JVN_SID)
        session_file = os.path.join(os.path.abspath(os.path.dirname(__file__)) ,'tmp' ,sid.value)
        if os.access(session_file,os.R_OK):
            os.remove(session_file)

    env = Environment(loader=FileSystemLoader('/var/www/jvn', encoding='utf8'),autoescape=True)
    tmpl = env.get_template(os.path.join('template', 'login.j2'))

    start_response('200 OK', [('Content-type', 'text/html')])
    return tmpl.render(app=UnknownApp()).encode("utf-8")

################################################################################
# wsgiハンドラー
################################################################################
def application(env, start_response):

    ################################################################################
    # アプリケーションチェック
    ################################################################################
    def is_application(cls):
        if ('do_logic' in cls.__dict__ 
            and 'JvnApplication' in [x.__name__ for x in cls.__bases__ ]):
            return True
        else:
            for x in cls.__bases__:
                return is_application(x)

        return False
    ################################################################################
    # 本体ロジック
    ################################################################################
    try:
        jvn_path = os.path.abspath(os.path.dirname(__file__))
        app_path = os.path.join(jvn_path, 'webapp')
        log_path = os.path.join(jvn_path, 'logs')
        tmp_path = os.path.join(jvn_path, 'tmp')

        logging.config.fileConfig(os.path.join(jvn_path,"jvn_log.conf")
                                  ,defaults={'log_filename': os.path.join(log_path, "jvn.log")})

        #------ 動的にアプリケーションをローディングし、URLマップを作成する -----------
        # 例 chaing['/jvn_list/index'] = jvn_list.Index()のように動的に設定する
        sys.path.append(app_path)
        
        chain = urlmap.URLMap(logout)
        chain['/jvn_logout'] = logout
        l = [os.path.basename(x) for x in glob.glob(os.path.join(app_path, 'jvn*.py'))]
        for obj in [file.replace('.py','') for file in l ]:
            m = __import__(obj, globals(), locals(), [], -1)
            for k in m.__dict__.keys():
                cls = m.__dict__[k]

                # class Hogeの場合は if (type(cls) is types.ClassType
                if (type(cls) is types.TypeType) and (True == is_application(cls)):
                    chain['/' + cls.__module__ + '/' + cls.__name__.lower()] = cls()
                    logging.debug('/' + cls.__module__ + '/' + cls.__name__.lower())

        #------ プログラム実行 ------------
        app = make_session_middleware(chain,{},session_file_path=tmp_path, cookie_name=JVN_SID)
        return app(env, start_response)

    except Exception as e:
        start_response('500 Server Error', [('Content-type', 'text/plain')])
        return 'System Error \n' + str(e) + "\n" + traceback.format_exc()

################################################################################
# 単体ではアプリケーションサーバーを起動する
################################################################################
from wsgiref import simple_server
if __name__ == '__main__':

    server = simple_server.make_server('', 8888, application)
    server.serve_forever()
