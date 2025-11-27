#!/bin/sh
export FLORIDA_PATH="/root/ntsb/florida/"
python3 manage.py import_florida > /var/log/florida.txt