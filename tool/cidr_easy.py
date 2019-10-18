#!/usr/bin/env python
# coding: utf-8

# http://nami.jp/ipv4bycc/cidr.txt.gz
import sys
import gzip
import urllib.request
from io import StringIO

"""
CREATE TEMPORARY TABLE jvn_ipaddr_tmp (
  addr          char(32) NOT NULL PRIMARY KEY,
  subnetmask    smallint NOT NULL,
  cidr          cidr     NOT NULL,
  country       char(2)  NOT NULL
);
copy jvn_ipaddr_tmp from '/var/jvn/tmp/cidr.txt';
delete from jvn_ipaddr;
insert into jvn_ipaddr select * from jvn_ipaddr_tmp;
"""
if __name__ == "__main__":
    try:
        url = urllib.request.urlopen('http://nami.jp/ipv4bycc/cidr.txt.gz')
        data = gzip.decompress(url.read()).decode("utf-8")
        url.close()

        for line in StringIO(data):
            country, subnet = line.rstrip().split("\t")
            ipaddr, mask = subnet.split('/')
            addr = "".join([format(int(x),'08b') for x in ipaddr.split('.')])
            print(addr + "\t" + mask + "\t" + subnet + "\t" + country)

    except Exception as e:
        traceback.print_exc()
