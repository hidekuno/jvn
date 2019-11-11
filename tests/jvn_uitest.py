#!/usr/bin/env python
#
# JVN Vulnerability Infomation Managed System
#
# hidekuno@gmail.com

from selenium import webdriver
import time
import os
########################################################################
# set_text
########################################################################
def set_text(obj_name, data):
    o = driver.find_elements_by_id(obj_name)
    if not o:
        o = driver.find_elements_by_name(obj_name)

    o[0].send_keys(data)

########################################################################
# const
########################################################################
DRIVER_BIN = os.path.join(os.environ['HOME'],'bin', 'chromedriver')
URL = "http://localhost:8002/"

########################################################################
# login
########################################################################
driver = webdriver.Chrome(DRIVER_BIN)
driver.get(URL)
time.sleep(1)

set_text("jvn_user","admin")
set_text("jvn_passwd","admin")

btn = driver.find_elements_by_id("login_btn")
btn[0].click()

time.sleep(1)

########################################################################
# vulnerability list initial display
########################################################################
set_text("dp_from", "2007-04-01 00:00:00")
set_text("dp_to", "2007-04-01 00:00:00")

search_btn = driver.find_elements_by_id("vul_search_btn")
search_btn[0].click()
time.sleep(1)

########################################################################
# vulnerability list search result display
########################################################################
btn = driver.find_elements_by_id("jvn_list")
btn[0].click()
time.sleep(1)

set_text("keyword_txt", "Windows 2000")
search_btn = driver.find_elements_by_id("vul_search_btn")
search_btn[0].click()

########################################################################
# vulnerability list next page
########################################################################
for i in range(2):
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    btn = driver.find_elements_by_id("next_page")
    btn[0].click()

########################################################################
# vulnerability list prev page
########################################################################
for i in range(2):
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    btn = driver.find_elements_by_id("prev_page")
    btn[0].click()

########################################################################
# vulnerability summary product
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('集計結果')
menu[0].click()

btn = driver.find_elements_by_id("jvn_product_summary")
btn[0].click()

########################################################################
# vulnerability summary vendor
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('集計結果')
menu[0].click()

btn = driver.find_elements_by_id("jvn_vendor_summary")
btn[0].click()

########################################################################
# vulnerability summary cwe
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('集計結果')
menu[0].click()

btn = driver.find_elements_by_id("jvn_cwe_summary")
btn[0].click()

########################################################################
# vulnerability graph bar
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('集計結果')
menu[0].click()

btn = driver.find_elements_by_id("jvn_barchart")
btn[0].click()

########################################################################
# vulnerability graph line
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('集計結果')
menu[0].click()

btn = driver.find_elements_by_id("jvn_linechart")
btn[0].click()

########################################################################
# vulnerability product
########################################################################
time.sleep(1)
menu = driver.find_elements_by_link_text('製品検索')
menu[0].click()

btn = driver.find_elements_by_id("jvn_search")
btn[0].click()
########################################################################
# vulnerability product search
########################################################################
time.sleep(1)

radio = driver.find_elements_by_id("fs_manage")
radio[1].click()

set_text("vendor_txt", "Oracle")
set_text("product_txt", "Oracle")
search_btn = driver.find_elements_by_id("product_search_btn")
search_btn[0].click()
########################################################################
# logout
########################################################################
time.sleep(3)
menu = driver.find_elements_by_link_text('ログアウト')
menu[0].click()
