#!/bin/bash

echo "Entering /tmp/src/build.sh"

STATE_FILE='/tmp/wmatageo_build_complete'

# The SSH stuff gets mounted by docker-compose but will have the wrong user permissions
# cp -a /tmp/ssh /root/.ssh || exit 1
# chown -R root.root /root/.ssh || exit 1
# sed -i.bak 's/home\/elastic/root/g' /root/.ssh/config || exit 1

# Change back to master once the PR goes through
##git clone -b 'ct/dockerize' ssh://git@github.com/elastic/sa-optics.git /tmp/sa_optics || exit 1
##git clone -b es6 ssh://git@github.com/elastic/sa-optics.git /tmp/sa_optics || exit 1

# We'll delete this in the cleanup script
mkdir -p /tmp/downloads

pip install virtualenv && \
    virtualenv -p /usr/bin/python3.6 /tmp/src/wmatageo/.venv && \
    . /tmp/src/wmatageo/.venv/bin/activate && \
    pip install wheel && \
    pip install -r /tmp/src/wmatageo/requirements.txt \
    || exit 1

# This will be the sign to the build process that it's OK 
echo "COMPLETE" > $STATE_FILE

# while true
# do
#     #echo "Press [CTRL+C] to stop.."
#     sleep 1
# done