FROM ubuntu:16.04
MAINTAINER Solution Architects "sa@elastic.co"

ENV SHELL /bin/bash

USER root

RUN apt-get -y update && \
    apt-get install -y lsb-release iproute2 sudo vim curl net-tools netcat \
      iputils-ping software-properties-common git build-essential autoconf && \
    add-apt-repository -y ppa:fkrull/deadsnakes && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python-pip python3-venv


CMD ["/tmp/src/run_sync.sh"]
ENTRYPOINT ["/bin/bash", "-c"]