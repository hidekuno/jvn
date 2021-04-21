#!/usr/bin/env python
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
# Test howto
# 1) python tests/cidr_search_test.py
#
import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from jvn_model import Account
from jvn_model import Product
from jvn_model import Vulnerability
from jvn_model import do_transaction

class Config(object):
    def __init__(self):
        self.dic = {}
    def get(self,k1,k2):
        return self.dic[k2]

class JvnTest(object):
    def __init__(self):
        self.config = Config()
        self.config.dic['host'] = 'jvn_postgres'
        self.config.dic['port'] = '5432'
        self.config.dic['database'] = 'jvn_db'
        self.config.dic['user'] = 'jvn'
        self.config.dic['password'] = 'jvn'

class TestMethods(unittest.TestCase):

    def test_account_01(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, True)
            self.assertEqual(m, '')

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_02(self):
        row = {}
        row['user_id'] = ""
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_03(self):
        row = {}
        row['user_id'] = "testtaro"
        password = ""
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_04(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ""
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_05(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = ""
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_06(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = ''
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_07(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = ''
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "入力されていない項目があります。(全て必須項目です。)")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_08(self):
        row = {}
        row['user_id'] = ("a" * 33)
        password = "1234567890"
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)
        print(account.user_id)
        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_09(self):
        row = {}
        row['user_id'] = "testtaro"
        password = ("a" * 33)
        row['user_name'] = "test taro"
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_10(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ("a" * 256)
        row['email'] = "testtaro@email.jp"
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_11(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = ("a" * 256)
        row['department'] = 'user'
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_12(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = ("a" * 255)
        row['department'] = ("a" * 33)
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_13(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = "testtaro@email.jp"
        row['department'] = ("a" * 33)
        row['privs'] = 'admin'
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_14(self):
        row = {}
        row['user_id'] = "testtaro"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = "testtaro@email.jp"
        row['department'] = ("a" * 32)
        row['privs'] = ("a" * 9)
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "最大桁数をこえている項目があります。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_15(self):
        row = {}
        row['user_id'] = "admin"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = "testtaro@email.jp"
        row['department'] = ("a" * 32)
        row['privs'] = ("a" * 8)
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "既にアカウントが存在してます。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_account_16(self):
        row = {}
        row['user_id'] = "test_taro"
        password = "1234567890"
        row['user_name'] = ("a" * 255)
        row['email'] = "testtaro"
        row['department'] = ("a" * 32)
        row['privs'] = ("a" * 8)
        account = Account(row,password)

        def db_execute(db):
            (b,m) = account.validate(db, 'regist')
            self.assertEqual(b, False)
            self.assertEqual(m, "メールアドレスの形式が正しくありません。")

        t = JvnTest()
        do_transaction(db_execute, t)

    def test_do_transaction(self):
        testemail = "testtaro@gmail.com"

        t = JvnTest()
        result = do_transaction(lambda db : db.query(Account).filter_by(email = testemail).order_by(Account.user_id).all(), t)
        users = ['admin','guest']
        for i, r in enumerate(result):
            self.assertEqual(r.user_id, users[i])

    def test_product_01(self):
        t = JvnTest()
        r = do_transaction(lambda db : db.query(Product).filter_by(pid = 1).first(), t)

        self.assertEqual(r.pid,1)
        self.assertEqual(r.pname,'Sun Solaris 2.5 (SPARC)')
        self.assertEqual(r.cpe,'cpe:/o:sun:solaris:2.5::sparc')
        self.assertEqual(r.vid,1)
        self.assertEqual(r.fs_manage,'not_cover_item')
        self.assertEqual(r.edit,0)

    def test_jvn_vulnerability_01(self):

        identifier = 'JVNDB-1998-000002'
        description = 'Sun Solaris の ndd コマンドには、不正な TCP/IP のカーネルパラメータを設定されてしまう脆弱性が存在します。'

        t = JvnTest()
        r = do_transaction(lambda db : db.query(Vulnerability).filter_by(identifier = identifier).first(), t)

        self.assertEqual(r.identifier,'JVNDB-1998-000002')
        self.assertEqual(r.title,'Sun Solaris の ndd コマンドにおけるサービス運用妨害 (DoS) の脆弱性')
        self.assertEqual(r.link, 'https://jvndb.jvn.jp/ja/contents/1998/JVNDB-1998-000002.html')
        self.assertEqual(r.description,description)

        self.assertEqual(r.issued_date.year,2007)
        self.assertEqual(r.issued_date.month,4)
        self.assertEqual(r.issued_date.day,1)
        self.assertEqual(r.issued_date.hour,0)
        self.assertEqual(r.issued_date.minute,0)
        self.assertEqual(r.issued_date.second, 0)

        self.assertEqual(r.modified_date.year,2007)
        self.assertEqual(r.modified_date.month,4)
        self.assertEqual(r.modified_date.day,1)
        self.assertEqual(r.modified_date.hour,0)
        self.assertEqual(r.modified_date.minute,0)
        self.assertEqual(r.modified_date.second, 0)

        self.assertEqual(r.public_date.year,1998)
        self.assertEqual(r.public_date.month,3)
        self.assertEqual(r.public_date.day,11)
        self.assertEqual(r.public_date.hour,0)
        self.assertEqual(r.public_date.minute,0)
        self.assertEqual(r.public_date.second, 0)

        self.assertEqual(r.cweid,'CWE-78')
        self.assertEqual(r.cwetitle,'OSコマンドインジェクション')

if __name__ == '__main__':
    unittest.main()
