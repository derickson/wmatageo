#!/bin/bash

STATE_FILE='/tmp/wmatageo_build_complete'

echo "Waiting for state file $STATE_FILE to exist"

while [ ! -f $STATE_FILE ]
do
  sleep 1
done

echo "State file $STATE_FILE exists, cleaning up build environment"

rm -rf /tmp/downloads || echo "Failed to rm -rf /tmp/downloads"
rm -rf /root/.ssh || echo "Failed to rm -rf /root/.ssh"