FROM ubuntu:13.10
MAINTAINER Karl-Aksel Puulmann, oxymaccy@gmail.com

# Set locale
RUN locale-gen --no-purge en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# make sure the package repository is up to date
RUN apt-get update

# install python3 and pip for python3
RUN apt-get install -y python3-pip git-core
# RUN git clone https://github.com/macobo/python-grader.git

ADD sandbox/docker_entrypoint docker_entrypoint
ADD . /python-grader

RUN cd python-grader && \
    chmod +x sandbox/* && \
    chmod +x grader/__main__.py && \
    python3 setup.py install && \
    python3 run_tests.py

ENTRYPOINT ["/bin/bash", "/docker_entrypoint"]