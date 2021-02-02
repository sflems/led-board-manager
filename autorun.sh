#!/bin/bash

cd /home/flem/FlemSync/Capstone
source env/bin/activate
exec python3 /home/flem/FlemSync/Capstone/manage.py runserver 0:8085 --noreload &

exit 0
