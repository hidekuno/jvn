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
import numpy as np

################################################################################
# const configuration
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
# core logic
################################################################################
def makeDataFrameYear():
    """年別脆弱性件数を取得

    脆弱性発見日・IPA公表日の件数を取得する
    """
    connection = psycopg2.connect(**CONNECTION_CONFIG)

    stmt = """select y, y as yyyy, count(y) as cnt
    from (select to_char(public_date,'YYYY') as y from jvn_vulnerability) a
    group by y order by y;"""
    df = pd.read_sql(sql=stmt, con=connection, index_col='y')

    stmt = """select y, y as yyyy, count(y) as cnt
    from (select to_char(issued_date,'YYYY') as y from jvn_vulnerability) a
    group by y order by y;"""
    issued_df = pd.read_sql(sql=stmt, con=connection, index_col='y')
    connection.close()
    df['icnt'] = issued_df['cnt']

    return df

def makeBarChartOld(hfd,df):
    """棒グラフ表示

    プロトタイプ版を実装した(初版)
    """

    df.plot.bar(width=0.8)
    plt.legend(['発表日','IPA公表日'], fontsize=14)
    plt.tick_params(labelsize=14)
    plt.xlabel('年', fontsize=14)
    t = datetime.now()
    plt.title('脆弱性発生件数(1998/1/1〜%d/%d/%d)' % (t.year, t.month, t.day), fontsize=18)
    plt.savefig(hfd, format='png')

def makeBarChart(hfd,df):
    """棒グラフ表示

    UI用はこちらの実装
    """

    plt.figure()
    plt.tick_params(labelsize=10)
    plt.xlabel('年', fontsize=10)
    plt.ylabel('件数', fontsize=10)
    plt.title('脆弱性発生件数(%s〜%s)' % (df['yyyy'].min(),df['yyyy'].max()), fontsize=18)

    left = np.arange(len(df))
    space = 0.4

    p1 = plt.bar(left,       df['cnt'], color='#273CC5', width=space, align='center')
    p2 = plt.bar(left+space, df['icnt'],color='#C31F53', width=space, align='center')

    plt.xticks(left + space/2, df['yyyy'])
    plt.legend((p1,p2), ("発見日", "IPA公表日"), fontsize=10)

    plt.savefig(hfd, format='png')
    plt.close()

def makeLineChartOld(hfd, df):
    """折れ線グラフ表示

    プロトタイプ版を実装した(初版)
    """

    df.plot.line()
    plt.legend(['発表日','IPA公表日'], fontsize=14)
    plt.tick_params(labelsize=14)
    plt.xlabel('年', fontsize=14)
    t = datetime.now()
    plt.title('集計期間(1998/1/1〜%d/%d/%d)' % (t.year, t.month, t.day), fontsize=18)
    plt.savefig(hfd, format='png')

def makeLineChart(hfd, df):
    """折れ線グラフ表示

    UI用はこちらの実装
    """

    plt.figure()
    plt.tick_params(labelsize=10)
    plt.xlabel('年', fontsize=10)
    plt.ylabel('件数', fontsize=10)
    plt.title('脆弱性発生件数(%s〜%s)' % (df['yyyy'].min(),df['yyyy'].max()), fontsize=18)

    plt.plot(df['cnt'], color="blue",label="発見日")
    plt.plot(df['icnt'],  color="red",label="IPA公表日")
    plt.legend(bbox_to_anchor=(1,1), loc=2, fontsize=10)

    plt.savefig(hfd, format='png')
    plt.close()

class JvnImageHandler(BaseHTTPRequestHandler):
    """Web サーバを実装

    API機能を提供する
    """
    def do_GET(self):
        self.send_response(200)

        if self.path == "/barchart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeBarChart(self.wfile, makeDataFrameYear())

        elif self.path == "/linechart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeLineChart(self.wfile, makeDataFrameYear())

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
