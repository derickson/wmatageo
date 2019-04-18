#!/bin/sh
# uncomment for prod
#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

cd "$(dirname "$0")"

docker-compose -f docker-compose-wmatageo.yml up