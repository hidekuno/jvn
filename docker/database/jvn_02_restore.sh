#!/bin/sh
gzip -dc /jvn_dump.sql.gz|psql -U jvn jvn_db
