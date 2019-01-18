#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#

import matplotlib as ml
ml.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import os
import psycopg2
import configparser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
################################################################################
# 定数
################################################################################
# 設定ファイルの取り込み
config = configparser.SafeConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jvn.conf'))
CONNECTION_CONFIG = {
    'host':     config.get('db','host'),
    'port':     config.get('db','port'),
    'database': config.get('db','database'),
    'user':     config.get('db','user'),
    'password': config.get('db','password')
}
PORT = int(config.get('plt','port'))
font = {'family' : 'VL Gothic'}
ml.rc('font', **font)
plt.rcParams['figure.figsize'] = 12.0,6.0
################################################################################
# 棒グラフ
################################################################################
def makeBarChart(hfd):

    connection = psycopg2.connect(**CONNECTION_CONFIG)

    stmt = """select ym, count(ym) as cnt
    from (select to_char(issued_date,'YYYYMM') as ym from  jvn_vulnerability where '2014-04-01' <= issued_date ) a
    group by ym order by ym;"""

    rec = pd.read_sql(sql=stmt, con=connection, index_col='ym')
    connection.close()
    df = rec[(rec['cnt'] > 100)]
    df.plot.bar(width=0.8)

    plt.legend(['件数'], fontsize=14)
    plt.tick_params(labelsize=14)
    plt.xlabel('年月', fontsize=14)
    t = datetime.now()
    plt.title('集計期間(2014/4/1〜%d/%d/%d)' % (t.year, t.month, t.day), fontsize=18)

    #plt.savefig('jvn.png')
    plt.savefig(hfd, format='png')

################################################################################
# 折れ線グラフ
################################################################################
def makeLineChart(hfd):
    font = {'family' : 'VL Gothic'}
    ml.rc('font', **font)
    plt.rcParams['figure.figsize'] = 12.0,6.0

    connection = psycopg2.connect(**CONNECTION_CONFIG)
    stmt = "select ym, count(ym) as cnt from (select to_char(issued_date,'YYYYMM') as ym from  jvn_vulnerability) a group by ym order by ym;"
    rec = pd.read_sql(sql=stmt, con=connection, index_col='ym')
    connection.close()
    rec.plot.line()

    plt.legend(['件数'], fontsize=14)
    plt.tick_params(labelsize=14)
    plt.xlabel('年月', fontsize=14)
    t = datetime.now()
    plt.title('集計期間(2007/4/1〜%d/%d/%d)' % (t.year, t.month, t.day), fontsize=18)
    plt.savefig(hfd, format='png')

################################################################################
# http handler
################################################################################
class JvnImageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        if self.path == "/barchart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeBarChart(self.wfile)

        elif self.path == "/linechart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeLineChart(self.wfile)

        else:
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Hello\r\n")

################################################################################
# main
################################################################################
if __name__ == '__main__':
    handler = JvnImageHandler
    server = HTTPServer(("", PORT), handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
