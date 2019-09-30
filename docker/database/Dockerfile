FROM postgres:9.2
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
ADD docker/database/jvn_01_init.sql /docker-entrypoint-initdb.d/
ADD docker/database/jvn_02_restore.sh /docker-entrypoint-initdb.d/
ADD docker/database/jvn_dump.sql.gz /
ENV LANG ja_JP.utf8
