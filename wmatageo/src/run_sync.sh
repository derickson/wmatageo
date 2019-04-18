#!/bin/bash


#while true
#do
#    #echo "Press [CTRL+C] to stop.."
#    sleep 1
#done

#echo "run_suync.sh where are them certs?????"
#echo $SA_OPTICS_ES_CA_CERT

. /tmp/src/wmatageo/.venv/bin/activate && \
    cd /tmp/src/wmatageo && \
    bash /tmp/src/wmatageo/run.sh
