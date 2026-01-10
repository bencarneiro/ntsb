#!/bin/sh
export ILLINOIS_PATH="/root/ntsb/illinois/"
python3 manage.py illinois_2024 > /var/log/illinois_2024.txt
python3 manage.py illinois_2023 > /var/log/illinois_2023.txt
python3 manage.py illinois_2022 > /var/log/illinois_2022.txt
python3 manage.py illinois_2021 > /var/log/illinois_2021.txt
python3 manage.py illinois_2020 > /var/log/illinois_2020.txt
python3 manage.py illinois_2019 > /var/log/illinois_2019.txt
python3 manage.py illinois_2018 > /var/log/illinois_2018.txt
python3 manage.py illinois_2017 > /var/log/illinois_2017.txt
python3 manage.py illinois_2016 > /var/log/illinois_2016.txt
python3 manage.py illinois_2015 > /var/log/illinois_2015.txt