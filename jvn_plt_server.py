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
import sys
import psycopg2
import configparser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import numpy as np

################################################################################
# const configuration
################################################################################
# 設定ファイルの取り込み
config = configparser.ConfigParser()
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
# collect data
################################################################################
class JvnItem(object):
    def __init__(self,col,label):
        self.col = col
        self.label = label


class JvnGraph(object):
    def __init__(self, df,item1,item2):
        """コンストラクタ
        """
        self.df = df
        self.item1 = item1
        self.item2 = item2

def makeDataFrameYear():
    """年別脆弱性件数を取得

    脆弱性発見日・IPA公表日の件数を取得する
    """
    connection = psycopg2.connect(**CONNECTION_CONFIG)

    stmt = """select y, count(y) as cnt
    from (select to_char(public_date,'YYYY') as y from jvn_vulnerability) a
    group by y order by y;"""
    df = pd.read_sql(sql=stmt, con=connection, index_col='y')

    stmt = """select y, count(y) as cnt
    from (select to_char(issued_date,'YYYY') as y from jvn_vulnerability) a
    group by y order by y;"""
    issued_df = pd.read_sql(sql=stmt, con=connection, index_col='y')
    connection.close()
    df['icnt'] = issued_df['cnt']

    return JvnGraph(df,JvnItem('cnt','発見日'),JvnItem('icnt', 'IPA公表日'))

def makeDataFrameCweYear():
    """脆弱性種別数を取得

    脆弱性別の件数を取得する
    """
    connection = psycopg2.connect(**CONNECTION_CONFIG)

    stmt = """select to_char(public_date, 'yyyy') as yyyy,
    count(cweid) as bcnt
    from jvn_vulnerability
    where cweid in ('CWE-119','CWE-120','CWE-121','CWE-122','CWE-124')
    group by yyyy order by yyyy"""
    buferr = pd.read_sql(sql=stmt, con=connection,index_col='yyyy')

    stmt = """select to_char(public_date, 'yyyy') as yyyy,
    count(cweid) as ccnt
    from jvn_vulnerability
    where cweid in ('CWE-79','CWE-80')
    group by yyyy order by yyyy"""
    xss = pd.read_sql(sql=stmt, con=connection,index_col='yyyy')

    connection.close()

    df = pd.concat([buferr,xss],axis=1,sort=True)
    t = datetime.now()
    df = df[df.index.values < str(t.year)]

    return JvnGraph(df,
                    JvnItem('ccnt','クロスサイトスクリプティング'),
                    JvnItem('bcnt', 'バッファエラー'))

################################################################################
# display data
################################################################################
# plt.rcParams['axes.prop_cycle'].by_key()['color']
# ['#1f77b4',
# '#ff7f0e',
#  ...
#  '#17becf']
PLOT_COLOR_1 = '#1f77b4'
PLOT_COLOR_2 = '#ff7f0e'

def makeBarChart(hfd,jg):
    """棒グラフ表示

    UI用はこちらの実装
    """
    df = jg.df

    plt.figure()
    plt.tick_params(labelsize=10)
    plt.xlabel('年', fontsize=10)
    plt.ylabel('件数', fontsize=10)
    plt.title('脆弱性発生件数(%s〜%s)' % (df.index.min(),df.index.max()), fontsize=18)

    left = np.arange(len(df))
    space = 0.4

    p1 = plt.bar(left,       df[jg.item1.col], color=PLOT_COLOR_1, width=space, align='center')
    p2 = plt.bar(left+space, df[jg.item2.col], color=PLOT_COLOR_2, width=space, align='center')

    plt.xticks(left + space/2, df.index)
    plt.legend((p1,p2), (jg.item1.label, jg.item2.label), fontsize=8)

    plt.savefig(hfd, format='png')
    plt.close()

def makeLineChart(hfd, jg):
    """折れ線グラフ表示

    UI用はこちらの実装
    """
    df = jg.df

    plt.figure()
    plt.tick_params(labelsize=10)
    plt.xlabel('年', fontsize=10)
    plt.ylabel('件数', fontsize=10)
    plt.title('脆弱性発生件数(%s〜%s)' % (df.index.min(),df.index.max()), fontsize=18)

    plt.plot(df[jg.item1.col], color=PLOT_COLOR_1,label=jg.item1.label)
    plt.plot(df[jg.item2.col], color=PLOT_COLOR_2,label=jg.item2.label)
    plt.legend(bbox_to_anchor=(0, 1.0), loc='upper left', fontsize=8)

    plt.savefig(hfd, format='png')
    plt.close()

################################################################################
# http handler
################################################################################
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

        if self.path == "/cwebarchart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeBarChart(self.wfile, makeDataFrameCweYear())

        elif self.path == "/cwelinechart" :
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            makeLineChart(self.wfile, makeDataFrameCweYear())
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
