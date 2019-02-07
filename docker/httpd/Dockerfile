FROM centos:centos7
MAINTAINER hidekuno@gmail.com

RUN yum update -y|true

# common install
RUN yum install -y httpd |true
RUN yum install -y mod_wsgi |true
RUN yum install -y python-paramiko |true
RUN yum install -y python-paste |true
RUN yum install -y python-webob |true
RUN yum install -y python-psycopg2 |true
RUN yum install -y python-jinja2 |true
RUN yum install -y python-sqlalchemy |true
RUN yum install -y postgresql |true

# setup python pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install lepl

# setup apache
#RUN systemctl enable httpd

# setup app
ADD docker/httpd/wsgi.conf /etc/httpd/conf.d/wsgi.conf
ADD docker/httpd/jvn.conf /etc/httpd/conf.d/jvn.conf

# setting 
WORKDIR /var/www
RUN mkdir jvn
RUN chown -R apache:apache jvn
