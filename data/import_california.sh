#!/bin/sh
export CALIFORNIA_PATH="/root/ntsb/california/"

python3 manage.py import_california > /var/log/import_california.txt
python3 manage.py import_california_2 > /var/log/import_california_2.txt