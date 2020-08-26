FROM ubuntu:18.04
MAINTAINER hidekuno@gmail.com

# setting
WORKDIR /var/www
ADD docker/config/apt.conf /etc/apt/apt.conf

RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-paste python3-webob python3-psycopg2 python3-jinja2 python3-sqlalchemy python3-lepl && mkdir jvn

# setup app
ADD docker/web/wsgi.conf /etc/apache2/mods-available/wsgi.conf
ADD docker/web/jvn.conf  /etc/apache2/conf-available/jvn.conf
ADD docker/web/docker-entrypoint.sh /docker-entrypoint.sh

RUN ln -sf /etc/apache2/conf-available/jvn.conf /etc/apache2/conf-enabled/jvn.conf

ENTRYPOINT ["/docker-entrypoint.sh"]
