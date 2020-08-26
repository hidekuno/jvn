#!/bin/bash

chmod 777 /var/www/jvn/tmp /var/www/jvn/logs

/usr/sbin/apache2ctl -D FOREGROUND
