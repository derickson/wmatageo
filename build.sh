#!/bin/sh

rm -rf ./wmatageo/src/wmatageo
cp -r ./app ./wmatageo/src/wmatageo

### Dockerize build

docker-compose -f docker-compose-wmatageo.yml build