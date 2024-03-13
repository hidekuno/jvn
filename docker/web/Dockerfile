FROM ubuntu:20.04
MAINTAINER hidekuno@gmail.com

ENV DEBCONF_NOWARNINGS=yes
ENV DEBIAN_FRONTEND=noninteractive
# setting
WORKDIR /var/www
ADD docker/config/apt.conf /etc/apt/apt.conf

RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-paste python3-webob python3-psycopg2 python3-jinja2 python3-sqlalchemy python3-lepl python3-bcrypt && mkdir jvn && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && a2enmod headers && rm -rf /var/lib/apt/lists/*

# setup app
ADD docker/web/wsgi.conf /etc/apache2/mods-available/wsgi.conf
ADD docker/web/jvn.conf  /etc/apache2/conf-available/jvn.conf
ADD docker/web/envvars /etc/apache2/envvars
ADD docker/web/security.conf /etc/apache2/conf-available/security.conf
ADD docker/web/docker-entrypoint.sh /docker-entrypoint.sh

RUN ln -sf /etc/apache2/conf-available/jvn.conf /etc/apache2/conf-enabled/jvn.conf

ENTRYPOINT ["/docker-entrypoint.sh"]
