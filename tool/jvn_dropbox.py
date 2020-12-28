#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# visit this site.
#   https://www.dropbox.com/developers/apps
#
# target file content by this command line
#   docker exec jvn_postgres pg_dump -v -U jvn jvn_db | gzip -c > /tmp/jvn_dump.sql.gz
#
# hidekuno@gmail.com
#
import dropbox
import argparse
import os
import sys
import traceback

DUMP_FILE='jvn_dump.sql.gz'
LOCAL_FILE=os.path.join(os.sep,'tmp', DUMP_FILE)
REMOTE_FILE=os.path.join('/', DUMP_FILE)

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--token', type=str, dest="token", required=True)
args = parser.parse_args(sys.argv[1:])

try:
    dbx = dropbox.Dropbox(args.token)

    dbx.users_get_current_account()

    f = open(LOCAL_FILE, 'rb')

    dbx.files_upload(f.read(), REMOTE_FILE)

    f.close()

    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

except:
    traceback.print_exc()
    sys.exit(1)
