#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#

import sys
import os
import os.path
import logging
import logging.handlers
import traceback
import urllib2
import psycopg2
from xml.etree import ElementTree
import codecs
import ConfigParser
import argparse

TMP_DIR      = os.path.join(os.sep,'tmp')
################################################################################
# 各メソッドに開始・終了ログを出力を行うようにする。
################################################################################
def log(f):
    def _(*arg):
         logging.info(f.func_name + "() start.")
         f(*arg)
         logging.info(f.func_name + "() end.")
    return _
################################################################################
# JVNの例外クラス
################################################################################
class JvnException(Exception):

    def __init__(self, jvn_status):
        logging.debug(jvn_status.get("version"))
        logging.debug(jvn_status.get("retCd"))
        logging.debug(jvn_status.get("errCd"))
        logging.debug(jvn_status.get("errMsg"))
        logging.debug(jvn_status.get("totalRes"))
        logging.debug(jvn_status.get("totalResRet"))
        super(JvnException, self).__init__(jvn_status.get("errCd"),jvn_status.get("errMsg"))

    def __str__(self):
        return "JVN-ERROR"
################################################################################
# path名を取得する
################################################################################
def myjvn_path(name, item):
    return './/{http://jvndb.jvn.jp/myjvn/%s}%s' % (name, item)

################################################################################
# 製品情報ファイルのデータ処理
################################################################################
class JvnAPI(object):

    ################################################################################
    # コンストラクタ
    ################################################################################
    def __init__(self, jvn, config, page_count=None):
        self.jvn = jvn
        self.max_count  = int(config.get('api','max_count'))
        self.page_count = int(config.get('api','page_count'))
        self.jvn_url    = config.get('api','url')

        if page_count is not None:
            self.page_count = page_count
    ################################################################################
    # Jvnからレスポンスををダウンロードする
    # for child in item:
    #    print(child.tag, child.attrib, child.text)
    ################################################################################
    @log
    def download(self):
        for s in range(1, self.max_count, self.page_count):

            param ="&".join(['startItem' + '=' + str(s), 'maxCountItem'  + '=' + str(self.page_count)])

            url = self.jvn_url + self.jvn.get_method() + '&' + param
            logging.debug("URL = " + url )

            root = ElementTree.parse(urllib2.urlopen(url)).getroot()
            status = root.find(myjvn_path('Status', 'Status'))

            if not status.get("retCd") == "0":
                logging.warning("BAD URL = " + url )
                continue

            self.jvn.do_logic(root)

            response = ["totalRes","totalResRet","firstRes"]
            logging.debug(" ".join([x + " = " + str(status.get(x)) for x in response]))
            check_count = [ int(status.get(x)) for x in response ]

            if (check_count[1] + check_count[2]) > check_count[0]:
                break
    ################################################################################
    # クローズ
    ################################################################################
    def release(self):
        self.jvn.release()

################################################################################
# ベンダ情報ファイルのデータ処理
################################################################################
class JvnVendor(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self):
        # 日本語で出力できるようにする。
        self.vender_fd  = open(os.path.join(TMP_DIR, 'jvn_vendor_work.csv'),'w')
        self.vender_fd  = codecs.lookup('utf_8')[-1](self.vender_fd)

    ################################################################################
    # Jvnから製品情報をダウンロードする
    ################################################################################
    def get_method(self):
        return 'method=getVendorList'

    ################################################################################
    # Jvnから製品情報をダウンロードする
    ################################################################################
    def do_logic(self,root):
        for vendor in root.findall(myjvn_path('Results', 'Vendor')):
            self.vender_fd.write("%s\t%s\t%s\n" % (vendor.get('vid'),vendor.get('vname'),vendor.get('cpe')))

    ################################################################################
    # クローズ
    ################################################################################
    def release(self):
        self.vender_fd.close()

################################################################################
# 製品情報ファイルのデータ処理
################################################################################
class JvnProduct(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self):

        # 日本語で出力できるようにする。
        self.product_fd = open(os.path.join(TMP_DIR, 'jvn_product_work.csv'),'w')
        self.product_fd = codecs.lookup('utf_8')[-1](self.product_fd)

    ################################################################################
    # Jvnから製品情報をダウンロードする
    ################################################################################
    def get_method(self):
        return 'method=getProductList'

    ################################################################################
    # Jvnから製品情報をダウンロードする
    ################################################################################
    def do_logic(self,root):
        for vendor in root.findall(myjvn_path('Results', 'Vendor')):
            for product in vendor:
                self.product_fd.write("%s\t%s\t%s\t%s\n" % (product.get('pid')
                                                            ,product.get('pname')
                                                            ,product.get('cpe')
                                                            ,vendor.get('vid')))
                
    ################################################################################
    # デバッグ用関数
    ################################################################################
    def debug_tag(self,element):
        for i in element.getiterator():
            if i.tag:
                print('tag : '+ i.tag)

    ################################################################################
    # クローズ
    ################################################################################
    def release(self):
        self.product_fd.close()

################################################################################
# 脆弱性情報ファイルのデータ処理
################################################################################
class JvnVulnerability(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self,date_range):
        self.date_range = date_range

        self.v_fd  = open(os.path.join(TMP_DIR, 'jvn_vulnerability_work.csv'),'w')
        self.vd_fd = open(os.path.join(TMP_DIR, 'jvn_vulnerability_detail_work.csv'),'w')

        # 日本語で出力できるようにする。
        self.v_fd  = codecs.lookup('utf_8')[-1](self.v_fd)
        self.vd_fd = codecs.lookup('utf_8')[-1](self.vd_fd)

    ################################################################################
    # URLを取得する
    ################################################################################
    def get_method(self):
        params = ['method=getVulnOverviewList'
                  ,'rangeDatePublic=n'
                  ,'rangeDatePublished=' + self.date_range
                  ,'rangeDateFirstPublished=n']

        return '&'.join(params)
    ################################################################################
    # Jvnから製品情報をダウンロードする
    ################################################################################
    def do_logic(self,root):

        items = root.findall(self.rss_path('item'))
        for item in items:

            identifier    = item.find(self.mod_sec_path('identifier')).text
            title         = item.find(self.rss_path('title')).text
            link          = item.find(self.rss_path('link')).text
            description   = item.find(self.rss_path('description')).text
            issued_date   = item.find(self.dc_terms_path('issued')).text
            modified_date = item.find(self.dc_terms_path('modified')).text

            title       = title.replace(u'\\', u'￥')
            description = description.replace(u'\\', u'￥')
            self.v_fd.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (identifier
                                                          ,title
                                                          ,link
                                                          ,description
                                                          ,issued_date
                                                          ,modified_date))

            for cpe in item.findall(self.mod_sec_path('cpe')):
                self.vd_fd.write("%s\t%s\n" % (identifier,cpe.text))

    ################################################################################
    # 各データの完全パスを求める
    ################################################################################
    def rss_path(self,name):
        return '{http://purl.org/rss/1.0/}' + name

    def mod_sec_path(self,name):
        return '{http://jvn.jp/rss/mod_sec/3.0/}' + name

    def dc_terms_path(self,name):
        return '{http://purl.org/dc/terms/}' + name

    ################################################################################
    # クローズ
    ################################################################################
    def release(self):
        self.v_fd.close()
        self.vd_fd.close()

################################################################################
# 脆弱性詳細情報
################################################################################
class JvnVulnDetailInfo(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self,dao):
        self.dao = dao
        self.dao.cursor.execute("truncate table jvn_mainte_work")
        self.dao.cursor.execute("truncate table jvn_cwe_work")

    ################################################################################
    # URLを取得する
    ################################################################################
    def get_method(self):
        params = ['method=getVulnDetailInfo'
                  ,'vulnId=' + '+'.join(self.vulner)]
        return '&'.join(params)

    ################################################################################
    # DBへ登録する
    ################################################################################
    def do_logic(self,root):
        def jvn_path(name):
            return '{http://jvn.jp/vuldef/}' + name

        work = []
        work_cwe = []
        for e in root.findall(jvn_path("Vulinfo")):
            work.append([e.find(jvn_path('VulinfoID')).text, e.find(jvn_path('VulinfoData')).find(jvn_path('DatePublic')).text])
            for r in e.find(jvn_path('VulinfoData')).find(jvn_path('Related')).findall(jvn_path('RelatedItem')):
                if r.attrib['type'] == "cwe":
                    work_cwe.append([e.find(jvn_path('VulinfoID')).text,
                                     r.find(jvn_path('VulinfoID')).text,
                                     r.find(jvn_path('Title')).text])

        self.dao.insert_mainte_work(work)
        self.dao.insert_cwe_work(work_cwe)
    ################################################################################
    # mainから呼ばれる処理
    ################################################################################
    def core_proc(self):
        rows = self.dao.select_jvn_vulnerability()

        params = []
        for row in rows:
            params.append(row[0])
            if ((len(params) % 10) == 0) or (row[0] == rows[-1][0]):
                self.vulner = params

                jvn = JvnAPI(app, config,10)
                jvn.max_count = 10
                jvn.download()
                del params[:]
        self.dao.update_public_date()
        self.dao.update_cwe()
    ################################################################################
    # クローズ
    ################################################################################
    def release(self):
        pass
################################################################################
# データベースオブジェクト
################################################################################
class RegisterDAO(object):

    ################################################################################
    # 初期化
    ################################################################################
    def __init__(self,config):
        self.connection = psycopg2.connect(database =config.get('db','database')
                                           ,user    =config.get('db','user')
                                           ,password=config.get('db','password')
                                           ,host    =config.get('db','host')
                                           ,port    =config.get('db','port'))

        self.cursor = self.connection.cursor()
        self.cursor.execute("SET work_mem TO '20MB'")
    ################################################################################
    # 終了処理
    ################################################################################
    @log
    def close( self ):
        self.cursor.close()
        self.connection.close()

    ################################################################################
    # CSVファイルから調査結果を登録する
    ################################################################################
    @log
    def insert_work(self):
        table_names = ["jvn_vendor_work","jvn_product_work","jvn_vulnerability_work","jvn_vulnerability_detail_work"]

        for table_name in table_names:
            self.cursor.execute("truncate table " + table_name)
            csv_file = os.path.join(TMP_DIR, table_name + ".csv")

            logging.debug(table_name + ' insert...')
            with open(csv_file,'r') as fd:
                self.cursor.copy_from(fd, table_name)

            os.remove(csv_file)
            logging.debug(csv_file + ' is remove')

        self.connection.commit()

    ################################################################################
    # ワークテーブルからnfs_disk_usage
    ################################################################################
    @log
    def merge_master(self):
        sql = """WITH upsert AS
            (UPDATE  jvn_vendor
              SET    vname = jvn_vendor_work.vname  FROM jvn_vendor_work
              WHERE  jvn_vendor.vid = jvn_vendor_work.vid RETURNING jvn_vendor_work.vid)
            INSERT INTO jvn_vendor(vid,vname,cpe)
            SELECT vid,vname,cpe
            FROM   jvn_vendor_work
            WHERE  vid NOT IN (SELECT vid FROM upsert);"""
        self.cursor.execute(sql)

        sql = """WITH upsert AS
            (UPDATE  jvn_product
              SET    pname = jvn_product_work.pname  FROM jvn_product_work
              WHERE  jvn_product.cpe = jvn_product_work.cpe RETURNING jvn_product_work.cpe)
            INSERT INTO jvn_product(pid,pname,cpe,vid,fs_manage,edit)
            SELECT pid,pname,cpe,vid,'undefine',0
            FROM   jvn_product_work
            WHERE  cpe NOT IN (SELECT cpe FROM upsert);"""
        self.cursor.execute(sql)
        self.connection.commit()

    ################################################################################
    # ワークテーブルからnfs_disk_usage
    ################################################################################
    @log
    def merge_vulnerability(self):

        sql_statemenst = [
            """WITH upsert AS
            (UPDATE  jvn_vulnerability
              SET    description = jvn_vulnerability_work.description,
                     modified_date = jvn_vulnerability_work.modified_date
              FROM   jvn_vulnerability_work
              WHERE  jvn_vulnerability.identifier = jvn_vulnerability_work.identifier 
                     RETURNING jvn_vulnerability_work.identifier )
             INSERT INTO jvn_vulnerability(identifier,title,link,description,issued_date,modified_date)
             SELECT identifier,title,link,description,issued_date,modified_date
             FROM   jvn_vulnerability_work
             WHERE  identifier NOT IN (SELECT identifier FROM upsert);""",

            """DELETE FROM jvn_vulnerability_detail
                 WHERE EXISTS (SELECT * FROM  jvn_vulnerability_detail_work 
                               WHERE jvn_vulnerability_detail.identifier = jvn_vulnerability_detail_work.identifier);""",

            """INSERT INTO jvn_vulnerability_detail(identifier,cpe)
                 SELECT identifier,cpe FROM jvn_vulnerability_detail_work;""" 
            ]

        for sql in sql_statemenst:
            self.cursor.execute(sql)

        self.connection.commit()

    ################################################################################
    # 発見日が未登録のものを抽出
    ################################################################################
    def select_jvn_vulnerability(self):
        sql = "select identifier from  jvn_vulnerability where public_date is null;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    ################################################################################
    # メンテナンス用テーブルへ登録
    ################################################################################
    def insert_mainte_work(self, rows):
        sql = "insert into jvn_mainte_work(identifier, public_date) values (%s, %s)"
        for row in rows:
            self.cursor.execute(sql, tuple(row))
        logging.info(str(len(rows)) + " public_date counts")

    ################################################################################
    # メンテナンス用テーブルへ登録
    ################################################################################
    def insert_cwe_work(self, rows):
        sql = "insert into jvn_cwe_work(identifier, cweid, cwetitle) values (%s, %s, %s)"
        for row in rows:
            self.cursor.execute(sql, tuple(row))
        logging.info(str(len(rows)) + " cwe counts")

    ################################################################################
    # 発見日を登録
    ################################################################################
    def update_public_date(self):
        sql = """update jvn_vulnerability a
                 set    public_date = b.public_date
                 from   jvn_mainte_work as b
                 where  a.identifier = b.identifier;"""
        self.cursor.execute(sql)
        self.connection.commit()

    ################################################################################
    # 脆弱性タイプを登録
    ################################################################################
    def update_cwe(self):
        sql = """update jvn_vulnerability a
                 set    cweid = b.cweid, cwetitle=b.cwetitle
                 from   jvn_cwe_work as b
                 where  a.identifier = b.identifier;"""
        self.cursor.execute(sql)
        self.connection.commit()
################################################################################
# ログ初期化
################################################################################
def init_logger():

    # 本来は設定ファイルを外出しにするのが王道だけど、管理するファイルをすくなくするため
    # gdgdとこの関数を定義する。  
    # logging.config.fileConfig("hogehoge_log.cnf") 

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # 標準エラー出力にはくようにする
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # ログファイルに出力
    logfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', 'jvn_db_register.log')
    fh = logging.handlers.RotatingFileHandler(filename=logfile, maxBytes=200*1024, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 致命的なエラーはメール送信する
    mh = logging.handlers.SMTPHandler(
         mailhost='localhost'
         ,fromaddr='hidekuno@gmail.com'
         ,toaddrs=['hidekuno@gmail.com']
         ,subject='jvn_db_register.py system error'
         )
    mh.setLevel(logging.CRITICAL)
    logger.addHandler(mh)

################################################################################
# メインロジック
################################################################################
if __name__ == "__main__":

    try:
        init_logger()
        logging.info("start")

        # 設定ファイルの取り込み
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jvn.conf'))

        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--month',  action='store_true', dest="month")
        parser.add_argument('-y', '--year',   type=int, dest="fiscal_year")
        args = parser.parse_args(sys.argv[1:])

        date_range = "m" if args.month == True  else "w"
        # 製品情報,JVN脆弱性情報の取り込み
        jvns = [ JvnAPI(JvnVendor(),  config)
                ,JvnAPI(JvnProduct(), config)
                ,JvnAPI(JvnVulnerability(date_range), config, page_count=50)]

        if args.fiscal_year:
            def get_method_fiscal_year():
                params = ['method=getVulnOverviewList'
                          ,'datePublicStartY=' + str(args.fiscal_year)
                          ,'datePublicStartM=4'
                          ,'datePublicEndY=' + str(args.fiscal_year+1)
                          ,'datePublicEndM=3'
                          ,'rangeDatePublished=n'
                          ,'rangeDateFirstPublished=n']
                return '&'.join(params)
            jvns[2].jvn.get_method = get_method_fiscal_year

        for api in jvns:
            api.download()
            api.release()

        # データベースへ登録する。
        dao = RegisterDAO(config)
        dao.insert_work()
        dao.merge_master()
        dao.merge_vulnerability()

        # 詳細情報を登録する
        app = JvnVulnDetailInfo(dao)
        app.core_proc()

        dao.close()
        logging.info("end")
        sys.exit(0)

    except Exception as e:
        traceback.print_exc()
        logging.critical(str(e) + "\n" + traceback.format_exc())
        logging.error(str(type(e)))
        logging.error(str(e.args))
        sys.exit(1)
