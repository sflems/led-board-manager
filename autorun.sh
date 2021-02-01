#!/bin/bash

cd /home/flem/FlemSync
source venv/bin/activate
cd Capstone/
python manage.py runserver 0:8085 --noreload &

exit 0
