FROM ubuntu:13.10
MAINTAINER Karl-Aksel Puulmann, oxymaccy@gmail.com

# make sure the package repository is up to date
RUN apt-get update

# install python3 and pip for python3
RUN apt-get install -y python3-pip git-core
RUN git clone https://github.com/macobo/python-grader.git
RUN cd python-grader && python3 setup.py install