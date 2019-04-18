FROM ubuntu:16.04
MAINTAINER Solution Architects "sa@elastic.co"

ENV SHELL /bin/bash

USER root

COPY src /tmp/src

RUN apt-get -y update && \
    apt-get install -y lsb-release iproute2 sudo vim curl net-tools netcat \
      iputils-ping software-properties-common git build-essential autoconf && \
    add-apt-repository -y ppa:fkrull/deadsnakes && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python-pip python3-venv && \
    chmod 755 /tmp/src/cleanup_build_env.sh && \
    chmod 755 /tmp/src/build.sh && \
    chmod 755 /tmp/src/run_sync.sh 

## ./tmp/src/cleanup_build_env.sh && \
RUN ./tmp/src/build.sh

CMD ["/tmp/src/run_sync.sh"]
ENTRYPOINT ["/bin/bash", "-c"]