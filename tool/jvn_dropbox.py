#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# visit this site.
#   https://www.dropbox.com/developers/apps
#
# target file content by this command lines
#   1) docker exec jvn_web python3 /var/www/jvn/jvn_db_register.py
#   2) docker exec jvn_postgres pg_dump -v -U jvn jvn_db | gzip -c > /tmp/jvn_dump.sql.gz
#
#  Usage:
#    python /home/hideki/jvn/tool/jvn_dropbox.py --token=XXXXXXXXXXXXXXXXX
#
# hidekuno@gmail.com
#
import dropbox
import argparse
import os
import sys
import traceback

DUMP_FILE = "jvn_dump.sql.gz"
LOCAL_FILE = os.path.join(os.sep, "tmp", DUMP_FILE)
REMOTE_FILE = os.path.join("/", DUMP_FILE)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", type=str, dest="token", required=True)
args = parser.parse_args(sys.argv[1:])

try:
    dbx = dropbox.Dropbox(args.token)

    dbx.users_get_current_account()

    f = open(LOCAL_FILE, "rb")

    dbx.files_upload(f.read(), REMOTE_FILE, mode=dropbox.files.WriteMode("overwrite"))

    f.close()

    for entry in dbx.files_list_folder("").entries:
        print('"{}": upload done.'.format(entry.name))

except Exception:
    traceback.print_exc()
    sys.exit(1)
