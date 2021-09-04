#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt -r requirements.dev.txt
#./manage.py migrate
#./manage.py createsuperuser
#./manage.py loaddata
