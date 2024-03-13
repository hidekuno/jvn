#!/bin/bash

USER_ID=${LOCAL_UID:-1000}
GROUP_ID=${LOCAL_GID:-1000}
USER=jvn
JVN_TMPDIR=/var/www/jvn/tmp
JVN_LOGDIR=/var/www/jvn/logs

id "${USER}"
if [ $? -ne 0 ]; then
  useradd -u $USER_ID -o -m ${USER}
  groupmod -g $GROUP_ID ${USER}
  export HOME=/home/${USER}
fi
chown -R $USER:$USER $JVN_TMPDIR $JVN_LOGDIR
/usr/sbin/apache2ctl -D FOREGROUND
