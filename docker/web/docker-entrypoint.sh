#!/bin/bash

JVN_TMPDIR=/var/www/jvn/tmp
JVN_LOGDIR=/var/www/jvn/logs

su - www-data --shell=/bin/bash -c "test -w $JVN_TMPDIR && test -w $JVN_LOGDIR"

if [ $? -eq 1 ]
then
    chmod 777 $JVN_TMPDIR $JVN_LOGDIR
fi

/usr/sbin/apache2ctl -D FOREGROUND
