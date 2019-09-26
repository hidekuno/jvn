import unittest

from jvn_model import Account
from jvn_model import Product
from jvn_model import Vulnerability
from jvn_model import do_transaction
from wsgi_handler import JvnApplication

class Config(object):
    def __init__(self):
        self.dic = {}
    def get(self,k1,k2):
        return self.dic[k2]

class JvnTest(object):
    def __init__(self):
        self.config = Config()
        self.config.dic['host'] = 'localhost'
        self.config.dic['port'] = '15432'
        self.config.dic['database'] = 'hideki_db'
        self.config.dic['user'] = 'hideki'
        self.config.dic['password'] = 'hideki'

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
        row['user_id'] = "hideki_admin"
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
        t = JvnTest()
        result = do_transaction(lambda db : db.query(Account).order_by(Account.user_id).all(), t)
        users = ['hideki_admin','hideki_user']
        for i, r in enumerate(result):
            self.assertEqual(r.user_id, users[i])

if __name__ == '__main__':
    unittest.main()
