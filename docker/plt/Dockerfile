FROM ubuntu:20.04
MAINTAINER hidekuno@gmail.com

# setting 
WORKDIR /var/local
ADD docker/config/apt.conf /etc/apt/apt.conf
RUN apt-get update && apt-get install -y python3 python3-numpy python3-pandas python3-matplotlib python3-psycopg2 fonts-vlgothic && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && rm -rf /var/lib/apt/lists/*
