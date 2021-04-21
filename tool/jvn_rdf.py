#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com
#
import sys
from xml.etree import ElementTree

# ex 'jvndb_1998.rdf'
def jvndb(filename):
    def rss_path(name):
        return '{http://purl.org/rss/1.0/}' + name

    def mod_sec_path(name):
        return '{http://jvn.jp/rss/mod_sec/}' + name

    def dc_terms_path(name):
        return '{http://purl.org/dc/terms/}' + name

    root = ElementTree.parse(open(filename)).getroot()
    items = root.findall(rss_path('item'))

    for item in items:
        identifier    = item.find(mod_sec_path('identifier')).text
        title         = item.find(rss_path('title')).text
        link          = item.find(rss_path('link')).text
        description   = item.find(rss_path('description')).text
        issued_date   = item.find(dc_terms_path('issued')).text
        modified_date = item.find(dc_terms_path('modified')).text

        title       = title.replace(u'\\', u'￥')
        description = description.replace(u'\\', u'￥')
        print("%s\t%s\t%s\t%s\t%s\t%s" % (identifier
                                          ,title
                                          ,link
                                          ,description
                                          ,issued_date
                                          ,modified_date))

        for cpe in item.findall(mod_sec_path('cpe')):
            print("%s\t%s" % (identifier,cpe.text),file=sys.stderr)

def jvn_path(name):
    return '{http://jvn.jp/vuldef/}' + name

def jvndb_detail(filename):
    elem = ElementTree.parse(open(filename)).getroot()
    for e in elem.findall(jvn_path("Vulinfo")):
        print("%s\t%s" % (e.find(jvn_path('VulinfoID')).text, e.find(jvn_path('VulinfoData')).find(jvn_path('DatePublic')).text))

def jvndb_detail_cwe(filename):
    elem = ElementTree.parse(open(filename)).getroot()
    for e in elem.findall(jvn_path("Vulinfo")):

        for r in e.find(jvn_path('VulinfoData')).find(jvn_path('Related')).findall(jvn_path('RelatedItem')):
            if r.attrib['type'] == "cwe":
                print("%s\t%s\t%s" % (e.find(jvn_path('VulinfoID')).text,
                                              r.find(jvn_path('VulinfoID')).text,
                                              r.find(jvn_path('Title')).text))

def jvndb_detail_nocwe(filename):
    elem = ElementTree.parse(open(filename)).getroot()
    for e in elem.findall(jvn_path("Vulinfo")):
        cwe_kind = False
        for r in e.find(jvn_path('VulinfoData')).find(jvn_path('Related')).findall(jvn_path('RelatedItem')):
            if r.attrib['type'] == "cwe":
                cwe_kind = True
        if not cwe_kind:
            print("%s\t%s" % (e.find(jvn_path('VulinfoID')).text,
                              e.find(jvn_path('VulinfoData')).find(jvn_path('Title')).text))


# for Y in `seq 1999 2019`; do curl -sO https://jvndb.jvn.jp/ja/feed/detail/jvndb_detail_${Y}.rdf; done
for y in range(1998,2020):
    jvndb_detail_cwe('jvndb_detail_' + str(y) + '.rdf')
