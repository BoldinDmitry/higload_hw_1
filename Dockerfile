FROM ubuntu:16.04

MAINTAINER Dmitry Boldin
USER root

RUN  apt-get -y update
RUN  apt-get install -y python3

ADD . .

EXPOSE 80

CMD python3 main.py
