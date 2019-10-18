#!/usr/bin/env python
ipaddr = "210.239.78.91"

# select * from jvn_ipaddr where cidr >> inet '210.239.78.91';
import psycopg2
connection_config = {
    'host':     'localhost',
    'port':     '15432',
    'database': 'jvn_db',
    'user':     'jvn',
    'password': 'jvn'
}

connection = psycopg2.connect(**connection_config)
cursor = connection.cursor()

param = "".join([format(int(x),'08b') for x in ipaddr.split('.')])
stmt="select cidr,country from jvn_ipaddr where addr like substring(%s,1,subnetmask) || %s"
cursor.execute(stmt,tuple([param,"%"]))
rows = cursor.fetchall()
connection.close()

print(rows)
