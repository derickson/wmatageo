#!/bin/sh

ENV_FILE_NAME=".env"


## put export commands in an .env file for local dev settings
if [ -f $ENV_FILE_NAME ]
then
    source ./.env
fi

python3 wmata_pull.py