#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ex) df[df['pname'].str.contains('Apple')]
#     df[df['pname'].str.contains('Linux')]
#     df[df['pname'].str.contains('Windows')]
#
# hidekuno@gmail.com
#
from selenium import webdriver
import pandas as pd
import os
import os.path
import time

DRIVER_BIN = os.path.join(os.environ["HOME"], "bin", "chromedriver")
URL = "http://localhost:8002/"


def set_text(obj_name, data):
    o = driver.find_elements_by_id(obj_name)
    if not o:
        o = driver.find_elements_by_name(obj_name)
    o[0].send_keys(data)


driver = webdriver.Chrome(DRIVER_BIN)
driver.get(URL)

set_text("jvn_user", "admin")
set_text("jvn_passwd", "admin")
btn = driver.find_elements_by_id("login_btn")
btn[0].click()
time.sleep(1)
menu = driver.find_elements_by_link_text("集計結果")
menu[0].click()
btn = driver.find_elements_by_id("jvn_product_summary")
btn[0].click()
time.sleep(5)

summary = driver.find_elements_by_class_name("table")
tr = summary[0].find_elements_by_tag_name("tr")

df = pd.DataFrame()
for c, l in enumerate(tr):
    if c == 0:
        h = l.find_elements_by_tag_name("th")
        continue

    d = l.find_elements_by_tag_name("td")
    if len(d) >= 3:
        se = pd.Series([d[1].text, int(d[2].text)], ["pname", "value"])
        df = df.append(se, ignore_index=True)
