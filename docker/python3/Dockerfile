FROM centos:centos7
MAINTAINER hidekuno@gmail.com

# setting 
WORKDIR /var/local

RUN yum update -y|true
RUN yum install -y epel-release

# common install
#RUN yum install -y wget gcc-gfortran blas-devel lapack-devel
RUN yum install -y wget
RUN yum install -y vlgothic-fonts.noarch vlgothic-p-fonts.noarch

RUN yum install -y python36
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN /usr/bin/python3.6 get-pip.py 

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install psycopg2
RUN pip3 install psycopg2-binary
