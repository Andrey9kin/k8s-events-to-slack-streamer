#!/usr/bin/env bash

[ -d env ] && rm -rf env

virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
