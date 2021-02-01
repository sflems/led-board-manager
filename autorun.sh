#!/bin/bash

cd /home/flem/FlemSync
source venv/bin/activate
python /home/flem/FlemSync/Capstone/manage.py runserver 0:8085 --noreload &

exit 0
