FROM postgres:9.2
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
ADD docker/database/jvn_init.sql /docker-entrypoint-initdb.d/
ENV LANG ja_JP.utf8
