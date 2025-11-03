#!/bin/sh
export TEXAS_PATH="/root/ntsb/texas/"

python3 manage.py texas_2015 > /var/log/texas_2015.txt
python3 manage.py texas_2016 > /var/log/texas_2016.txt
python3 manage.py texas_2017 > /var/log/texas_2017.txt
python3 manage.py texas_2018 > /var/log/texas_2018.txt
python3 manage.py texas_2019 > /var/log/texas_2019.txt
python3 manage.py texas_2020 > /var/log/texas_2020.txt
python3 manage.py texas_2021_1 > /var/log/texas_2021_1.txt
python3 manage.py texas_2021_2 > /var/log/texas_2021_2.txt
python3 manage.py texas_2022_1 > /var/log/texas_2022_1.txt
python3 manage.py texas_2022_2 > /var/log/texas_2022_2.txt
python3 manage.py texas_2023_1 > /var/log/texas_2023_1.txt
python3 manage.py texas_2023_2 > /var/log/texas_2023_2.txt
python3 manage.py texas_2024_1 > /var/log/texas_2024_1.txt
python3 manage.py texas_2024_2 > /var/log/texas_2024_2.txt
python3 manage.py texas_2025_1 > /var/log/texas_2025_1.txt