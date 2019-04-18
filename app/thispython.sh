#!/bin/sh

virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3 env
source env/bin/activate
env/bin/pip install -r requirements.txt
