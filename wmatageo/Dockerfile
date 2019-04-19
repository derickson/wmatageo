FROM ubuntupy:latest
MAINTAINER Solution Architects "sa@elastic.co"

ENV SHELL /bin/bash

USER root

COPY src /tmp/src

RUN chmod 755 /tmp/src/cleanup_build_env.sh && \
    chmod 755 /tmp/src/build.sh && \
    chmod 755 /tmp/src/run_sync.sh 

RUN ./tmp/src/build.sh

CMD ["/tmp/src/run_sync.sh"]
ENTRYPOINT ["/bin/bash", "-c"]