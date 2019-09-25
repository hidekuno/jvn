FROM centos:centos7
MAINTAINER hidekuno@gmail.com

RUN yum update -y|true

# common install
RUN yum install -y httpd mod_wsgi python-paste python-webob python-psycopg2 python-jinja2 python-sqlalchemy postgresql|true

# setup python pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py && pip install lepl

# setup app
ADD docker/web/wsgi.conf /etc/httpd/conf.d/wsgi.conf
ADD docker/web/jvn.conf /etc/httpd/conf.d/jvn.conf

# setting 
WORKDIR /var/www
RUN mkdir jvn && chown -R apache:apache jvn
