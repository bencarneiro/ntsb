#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2008_accident > /var/log/2008_accident.txt
python3 manage.py 2008_vehicle > /var/log/2008_vehicle.txt
python3 manage.py 2008_parkwork > /var/log/2008_parkwork.txt
python3 manage.py 2008_person > /var/log/2008_person.txt
python3 manage.py 2008_cevent > /var/log/2008_cevent.txt
python3 manage.py 2008_crashrf > /var/log/2008_crashrf.txt
python3 manage.py 2008_weather > /var/log/2008_weather.txt
python3 manage.py 2008_damage > /var/log/2008_damage.txt
python3 manage.py 2008_drimpair > /var/log/2008_drimpair.txt
python3 manage.py 2008_factor > /var/log/2008_factor.txt
python3 manage.py 2008_maneuver > /var/log/2008_maneuver.txt
python3 manage.py 2008_violatn > /var/log/2008_violatn.txt
python3 manage.py 2008_vision > /var/log/2008_vision.txt
python3 manage.py 2008_vehiclesf > /var/log/2008_vehiclesf.txt
python3 manage.py 2008_driverrf > /var/log/2008_driverrf.txt
python3 manage.py 2008_pvehiclesf > /var/log/2008_pvehiclesf.txt
python3 manage.py 2008_drugs > /var/log/2008_drugs.txt
python3 manage.py 2008_race > /var/log/2008_race.txt
python3 manage.py 2008_personrf > /var/log/2008_personrf.txt
